#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/26
# @Author  : 19921224
# @File    : scan_worker.py
# @Software: PyCharm
# @Description:
#   后台端口扫描工作线程。
#
#   设计要点：
#     1. 继承 QThread，在独立线程执行扫描，不阻塞UI主线程
#     2. 扫描完成通过 scan_completed 信号发送结果给UI
#     3. 扫描出错通过 scan_error 信号发送错误信息
#     4. 支持单次扫描和定时自动刷新
#     5. 线程安全：只在run()方法中执行扫描，UI更新通过信号槽机制
# ======================================================================

import time
import traceback

from PyQt5.QtCore import QThread, pyqtSignal

from v2.model.port_info import PortInfo
from v2.scanner.scanner_factory import get_scanner


class ScanWorker(QThread):
    """
    后台端口扫描工作线程。

    信号：
      scan_completed(list, float): 扫描完成，参数为(端口列表, 耗时秒数)
      scan_error(str):              扫描出错，参数为错误消息
    """

    scan_completed = pyqtSignal(list, float)  # List[PortInfo], elapsed_seconds
    scan_error = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._scanner = get_scanner()
        self._running = False

    def run(self):
        """线程入口：执行一次扫描。"""
        self._running = True
        start_time = time.time()

        try:
            ports = self._scanner.scan_ports()
            elapsed = time.time() - start_time
            self.scan_completed.emit(ports, elapsed)
        except Exception as e:
            error_msg = f"扫描端口失败: {str(e)}\n{traceback.format_exc()}"
            self.scan_error.emit(error_msg)
        finally:
            self._running = False

    def stop(self):
        """停止扫描线程。"""
        self._running = False
        self.wait(3000)

    @property
    def is_scanning(self) -> bool:
        return self._running
