#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : mac_scanner.py
# @Software: PyCharm
# @Description:
#   macOS / Linux 平台端口扫描器，对应 Java 版 MacPortScanner。
#   当前为占位实现。
#
#   TODO（迁移要点）：
#     1. 扫描所有端口：sh -c "lsof -i -P -n | grep LISTEN"
#        - 按空白分割：parts[0]=进程名 parts[1]=PID parts[2]=用户
#          parts[7]=协议 parts[8]=地址(如 *:8080)，正则提取端口
#     2. 扫描指定端口：sh -c "lsof -i :{port} -P -n | grep LISTEN"
#     3. 获取命令行：ps -p {pid} -o command=
#     4. 类型识别：调用 utils.port_type_identifier 填充 port_type/process_type
#     5. 状态硬编码为 LISTENING（与 Java 版一致）
# ======================================================================

from typing import List, Optional

from v2.model.port_info import PortInfo
from v2.scanner.port_scanner import PortScanner


class MacPortScanner(PortScanner):
    """macOS / Linux 平台端口扫描器（占位实现）。"""

    def scan_ports(self) -> List[PortInfo]:
        """扫描所有监听端口。TODO: 执行 lsof 并解析，当前返回空列表。"""
        # TODO: lsof -i -P -n | grep LISTEN
        return []

    def scan_port(self, port: int) -> Optional[PortInfo]:
        """扫描指定端口。TODO: 执行 lsof -i :{port}，当前返回 None。"""
        return None
