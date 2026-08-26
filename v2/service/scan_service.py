#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : scan_service.py
# @Software: PyCharm
# @Description:
#   端口扫描服务层，对应 Java 版 PortScanService。
#
#   职责：
#     1. 管理扫描缓存（self._cached_ports），UI直接读取缓存避免阻塞
#     2. 管理后台扫描线程（ScanWorker），自动定时刷新
#     3. 提供搜索/筛选/统计等业务逻辑
#     4. 信号通知UI数据更新
#
#   缓存设计说明（对应 Java 版 ConcurrentHashMap）：
#     - 桌面应用场景下不需要复杂的并发缓存，使用简单 List 即可
#     - 每次后台扫描完成后全量替换缓存
#     - UI线程只读取缓存，不直接执行系统命令
# ======================================================================

import time
from typing import Dict, List, Optional

from PyQt5.QtCore import QObject, QTimer, pyqtSignal

from v2.model.port_info import PortInfo
from v2.service.scan_worker import ScanWorker


class ScanService(QObject):
    """
    端口扫描服务。

    信号：
      ports_updated(List[PortInfo]): 端口列表更新（扫描完成时发射）
      scan_error(str):               扫描出错
      scan_started():                扫描开始
      scan_finished(float, int):     扫描完成（耗时秒数, 端口总数）
    """

    ports_updated = pyqtSignal(list)
    scan_error = pyqtSignal(str)
    scan_started = pyqtSignal()
    scan_finished = pyqtSignal(float, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._cached_ports: List[PortInfo] = []  # 扫描缓存
        self._scan_worker: Optional[ScanWorker] = None
        self._auto_refresh_enabled = True
        self._refresh_interval_ms = 5000  # 默认5秒
        self._last_scan_time: Optional[float] = None

        # 自动刷新定时器（控制何时启动下一次扫描）
        self._refresh_timer = QTimer(self)
        self._refresh_timer.setInterval(self._refresh_interval_ms)
        self._refresh_timer.timeout.connect(self._on_refresh_timer)

    # ------------------------------------------------------------------
    # 公共API
    # ------------------------------------------------------------------

    def start_auto_refresh(self):
        """启动自动刷新。立即执行一次扫描，然后按间隔定时刷新。"""
        self._auto_refresh_enabled = True
        if not self._refresh_timer.isActive():
            self._refresh_timer.start()
        # 立即扫描一次
        self.trigger_scan()

    def stop_auto_refresh(self):
        """停止自动刷新。"""
        self._auto_refresh_enabled = False
        self._refresh_timer.stop()
        # 如果正在扫描，等待结束
        if self._scan_worker and self._scan_worker.isRunning():
            self._scan_worker.wait(2000)

    def toggle_auto_refresh(self) -> bool:
        """切换自动刷新状态，返回新状态。"""
        if self._auto_refresh_enabled:
            self.stop_auto_refresh()
            return False
        else:
            self.start_auto_refresh()
            return True

    @property
    def is_auto_refresh_enabled(self) -> bool:
        return self._auto_refresh_enabled

    def trigger_scan(self):
        """触发一次手动扫描（刷新按钮点击）。"""
        # 如果已有扫描在进行，不重复启动
        if self._scan_worker and self._scan_worker.isRunning():
            return
        self._start_scan()

    def get_cached_ports(self) -> List[PortInfo]:
        """获取缓存中的端口列表（UI线程读取，快速返回）。"""
        return list(self._cached_ports)

    def search_ports(self, keyword: str, ports: List[PortInfo] = None) -> List[PortInfo]:
        """
        按关键字搜索端口/进程名/PID。
        :param keyword: 搜索关键字（不区分大小写）
        :param ports: 待搜索列表，为None时使用缓存
        """
        if ports is None:
            ports = self._cached_ports
        if not keyword:
            return list(ports)

        kw = keyword.lower().strip()
        return [
            p for p in ports
            if (str(p.port) in kw or
                kw in p.process_name.lower() or
                str(p.pid) in kw or
                kw in p.command_line.lower())
        ]

    def filter_ports(self,
                     port_type: str = "全部",
                     process_type: str = "全部",
                     protocol: str = "全部",
                     dev_only: bool = False,
                     ports: List[PortInfo] = None) -> List[PortInfo]:
        """
        筛选端口列表。
        """
        if ports is None:
            ports = self._cached_ports

        result = []
        for p in ports:
            if port_type != "全部" and p.port_type != port_type:
                continue
            if process_type != "全部" and p.process_type != process_type:
                continue
            if protocol != "全部" and p.protocol != protocol:
                continue
            if dev_only and not p.is_development_process:
                continue
            result.append(p)
        return result

    def get_statistics(self, ports: List[PortInfo] = None) -> Dict[str, int]:
        """
        统计端口数据：
          total: 总端口数
          dev:   开发进程数
          tcp:   TCP端口数
          udp:   UDP端口数
        """
        if ports is None:
            ports = self._cached_ports

        return {
            "total": len(ports),
            "dev": sum(1 for p in ports if p.is_development_process),
            "tcp": sum(1 for p in ports if p.protocol == "TCP"),
            "udp": sum(1 for p in ports if p.protocol == "UDP"),
        }

    @property
    def last_scan_time_str(self) -> str:
        """上次扫描时间的格式化字符串，如 10:06:10。"""
        if self._last_scan_time is None:
            return "--:--:--"
        return time.strftime("%H:%M:%S", time.localtime(self._last_scan_time))

    def get_port_by_number(self, port: int) -> Optional[PortInfo]:
        """根据端口号获取端口信息。"""
        for p in self._cached_ports:
            if p.port == port:
                return p
        return None

    # ------------------------------------------------------------------
    # 内部实现
    # ------------------------------------------------------------------

    def _start_scan(self):
        """启动后台扫描线程。"""
        if self._scan_worker and self._scan_worker.isRunning():
            return

        self.scan_started.emit()

        self._scan_worker = ScanWorker()
        self._scan_worker.scan_completed.connect(self._on_scan_completed)
        self._scan_worker.scan_error.connect(self._on_scan_error)
        self._scan_worker.start()

    def _on_refresh_timer(self):
        """定时器触发：如果自动刷新开启，执行扫描。"""
        if self._auto_refresh_enabled:
            self._start_scan()

    def _on_scan_completed(self, ports: List[PortInfo], elapsed: float):
        """扫描完成回调（在主线程执行，通过信号槽自动切换线程）。"""
        self._cached_ports = ports
        self._last_scan_time = time.time()
        self.ports_updated.emit(list(ports))
        self.scan_finished.emit(elapsed, len(ports))

    def _on_scan_error(self, error_msg: str):
        """扫描出错回调。"""
        self.scan_error.emit(error_msg)
