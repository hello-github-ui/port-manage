#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : scan_service.py
# @Software: PyCharm
# @Description:
#   扫描服务，对应 Java 版 PortScanService。
#   职责：调用扫描器获取端口数据、维护缓存、提供查询/搜索/统计能力。
#   当前为占位实现 —— 真实扫描器尚未接入，先用模拟数据让界面跑通。
#
#   TODO（迁移要点）：
#     1. 接入 scanner_factory.get_scanner() 获取真实端口
#     2. 用 QTimer 周期触发 scan_all()（对应 @Scheduled(fixedDelay=5000)）
#     3. 扫描放入 QThread / QProcess，避免阻塞 UI
#     4. 缓存 key 改为 (port, pid)，修复 Java 版同端口多 PID 覆盖问题
# ======================================================================

from datetime import datetime
from typing import List

from v2.model.port_info import PortInfo
from v2.utils.mock_util import generate_mock_ports


class ScanService:
    """
    端口扫描与数据查询服务。

    当前 get_all_ports() 返回模拟数据，待真实扫描器接入后替换。
    界面层只通过本服务访问数据，不直接接触扫描器 / 模拟数据，
    这样后续切换数据源时界面无需改动。
    """

    def __init__(self):
        # 上次扫描时间（字符串展示用）
        self._last_scan_time: str = ""

    def scan_all(self) -> List[PortInfo]:
        """
        触发一次完整扫描并刷新缓存。

        TODO: 调用 scanner_factory.get_scanner().scan_ports()
        当前用模拟数据代替。
        """
        # TODO: ports = get_scanner().scan_ports()
        ports = generate_mock_ports()
        self._last_scan_time = datetime.now().strftime("%H:%M:%S")
        return ports

    def get_all_ports(self) -> List[PortInfo]:
        """获取全部端口（触发一次扫描）。"""
        return self.scan_all()

    def get_statistics(self, ports: List[PortInfo]) -> dict:
        """
        计算统计信息，返回 dict：
          - total:                总端口数
          - development_processes:开发进程数
          - tcp:                  TCP 端口数
          - udp:                  UDP 端口数
        """
        return {
            "total": len(ports),
            "development_processes": sum(1 for p in ports if p.is_development_process),
            "tcp": sum(1 for p in ports if p.protocol.upper() == "TCP"),
            "udp": sum(1 for p in ports if p.protocol.upper() == "UDP"),
        }

    def search_ports(self, ports: List[PortInfo], keyword: str) -> List[PortInfo]:
        """
        模糊搜索：匹配端口号 / PID / 进程名 / 命令行。
        对应 Java 版 PortScanService.searchPorts。
        """
        if not keyword:
            return ports
        kw = keyword.lower()
        result = []
        for p in ports:
            if (kw in str(p.port) or
                    kw in str(p.pid) or
                    kw in p.process_name.lower() or
                    kw in p.command_line.lower()):
                result.append(p)
        return result

    @property
    def last_scan_time(self) -> str:
        """上次扫描时间（HH:MM:SS）。"""
        return self._last_scan_time
