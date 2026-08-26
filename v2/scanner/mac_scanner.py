#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : mac_scanner.py
# @Software: PyCharm
# @Description:
#   macOS / Linux 平台端口扫描器，对应 Java 版 MacPortScanner。
#
#   实现原理：
#     1. 使用 lsof -nP -iTCP -sTCP:LISTEN 获取TCP监听端口
#     2. 使用 lsof -nP -iUDP 获取UDP端口
#     3. 一次性获取所有进程的命令行：ps -eo pid,user,comm=,args=
#     4. 调用 port_type_identifier 识别类型
#
#   lsof输出格式：
#     COMMAND   PID  USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
#     node    12345  user   23u  IPv4  ...   0t0  TCP *:5173 (LISTEN)
# ======================================================================

import re
from typing import Dict, List, Optional

from v2.model.port_info import PortInfo
from v2.scanner.port_scanner import PortScanner
from v2.utils.cmd_util import run_command
from v2.utils.port_type_identifier import (identify_port_type,
                                           identify_process_type,
                                           is_development_process)

# lsof输出解析正则：COMMAND PID USER ... NAME部分包含地址和端口
# NAME示例: *:8080 (LISTEN)、127.0.0.1:3000 (LISTEN)、[::]:5432
LSOF_PATTERN = re.compile(
    r'^(\S+)\s+(\d+)\s+(\S+)\s+.*\s+(TCP|UDP)\s+(\S+?):(\d+)\s*(?:\(LISTEN\))?\s*$'
)


class MacPortScanner(PortScanner):
    """macOS / Linux 平台端口扫描器。"""

    def scan_ports(self) -> List[PortInfo]:
        """扫描所有监听端口（TCP LISTEN + UDP）。"""
        # 获取进程信息缓存（一次性获取，提高性能）
        process_info = self._get_all_process_info()

        result = []
        seen_ports = set()  # (protocol, port, pid) 去重

        # 第一步：扫描TCP监听端口
        tcp_ports = self._run_lsof_tcp()
        for port, pid, proc_name, user, local_addr in tcp_ports:
            key = ("TCP", port, pid)
            if key in seen_ports:
                continue
            seen_ports.add(key)
            cmd_line = process_info.get(pid, {}).get("cmd", "")
            if not proc_name:
                proc_name = process_info.get(pid, {}).get("name", f"PID_{pid}")

            # 识别类型
            proc_type = identify_process_type(proc_name, cmd_line)
            port_type = identify_port_type(port, proc_name, cmd_line)
            is_dev = is_development_process(proc_name, cmd_line)

            result.append(PortInfo(
                port=port,
                protocol="TCP",
                status="LISTENING",
                pid=pid,
                process_name=proc_name,
                command_line=cmd_line,
                is_development_process=is_dev,
                user=user,
                local_address=local_addr,
                port_type=port_type,
                process_type=proc_type
            ))

        # 第二步：扫描UDP端口
        udp_ports = self._run_lsof_udp()
        for port, pid, proc_name, user, local_addr in udp_ports:
            key = ("UDP", port, pid)
            if key in seen_ports:
                continue
            seen_ports.add(key)
            cmd_line = process_info.get(pid, {}).get("cmd", "")
            if not proc_name:
                proc_name = process_info.get(pid, {}).get("name", f"PID_{pid}")

            proc_type = identify_process_type(proc_name, cmd_line)
            port_type = identify_port_type(port, proc_name, cmd_line)
            is_dev = is_development_process(proc_name, cmd_line)

            result.append(PortInfo(
                port=port,
                protocol="UDP",
                status="",
                pid=pid,
                process_name=proc_name,
                command_line=cmd_line,
                is_development_process=is_dev,
                user=user,
                local_address=local_addr,
                port_type=port_type,
                process_type=proc_type
            ))

        return result

    def scan_port(self, port: int) -> Optional[PortInfo]:
        """扫描指定端口。"""
        for p in self.scan_ports():
            if p.port == port:
                return p
        return None

    # ------------------------------------------------------------------
    # 内部辅助方法
    # ------------------------------------------------------------------

    @staticmethod
    def _run_lsof_tcp() -> List[tuple]:
        """
        执行 lsof 获取TCP监听端口，返回 [(port, pid, name, user, addr), ...]
        参数说明：
          -n: 不解析主机名（更快）
          -P: 不解析端口名（显示数字端口）
          -iTCP: 只显示TCP
          -sTCP:LISTEN: 只显示LISTEN状态
        """
        result = []
        success, stdout, _ = run_command(
            ["lsof", "-nP", "-iTCP", "-sTCP:LISTEN"],
            timeout=10
        )
        if not success:
            # 某些Linux发行版可能需要sudo，但尽量不使用
            # 尝试不带-s参数
            success, stdout, _ = run_command(
                ["lsof", "-nP", "-i", "|", "grep", "LISTEN"],
                timeout=10
            )
            if not success:
                return result

        return MacPortScanner._parse_lsof_output(stdout, is_tcp=True)

    @staticmethod
    def _run_lsof_udp() -> List[tuple]:
        """执行 lsof 获取UDP端口。"""
        result = []
        success, stdout, _ = run_command(
            ["lsof", "-nP", "-iUDP"],
            timeout=10
        )
        if not success:
            return result
        return MacPortScanner._parse_lsof_output(stdout, is_tcp=False)

    @staticmethod
    def _parse_lsof_output(output: str, is_tcp: bool) -> List[tuple]:
        """解析lsof输出。"""
        result = []
        lines = output.splitlines()
        # 跳过第一行（表头）
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue

            # 使用split按空白分割，但限制分割次数避免命令行中有空格的问题
            parts = line.split(None, 8)
            if len(parts) < 9:
                continue

            try:
                comm = parts[0]
                pid = int(parts[1])
                user = parts[2]
                name_part = parts[8]

                # NAME部分格式: 地址:端口 (状态) 或 地址:端口
                # 例如: *:8080 (LISTEN)、localhost:3000、[::]:5432 (LISTEN)
                # 提取地址和端口
                addr_port = name_part
                # 去掉末尾的 (LISTEN)
                if "(" in addr_port:
                    addr_port = addr_port[:addr_port.index("(")].strip()

                # 找最后一个冒号分离地址和端口
                if ":" in addr_port:
                    # 处理IPv6地址 [::]:port 的情况
                    if addr_port.startswith("["):
                        bracket_end = addr_port.index("]")
                        local_addr = addr_port[1:bracket_end]
                        port_str = addr_port[bracket_end + 2:]
                    else:
                        colon_pos = addr_port.rfind(":")
                        local_addr = addr_port[:colon_pos]
                        port_str = addr_port[colon_pos + 1:]

                    port = int(port_str)
                    result.append((port, pid, comm, user, local_addr))

            except (ValueError, IndexError):
                continue

        return result

    @staticmethod
    def _get_all_process_info() -> Dict[int, dict]:
        """
        批量获取所有进程信息，返回 {pid: {"name": ..., "user": ..., "cmd": ...}}。
        使用 ps 命令一次性获取：ps -eo pid,user,comm=,args=
        """
        result = {}
        success, stdout, _ = run_command(
            ["ps", "-eo", "pid,user,comm,args"],
            timeout=10
        )
        if not success:
            return result

        lines = stdout.splitlines()
        # 跳过表头
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            parts = line.split(None, 3)
            if len(parts) < 4:
                # 没有命令行参数的情况
                if len(parts) >= 3:
                    try:
                        pid = int(parts[0])
                        result[pid] = {
                            "name": parts[2],
                            "user": parts[1],
                            "cmd": ""
                        }
                    except ValueError:
                        pass
                continue

            try:
                pid = int(parts[0])
                result[pid] = {
                    "name": parts[2],
                    "user": parts[1],
                    "cmd": parts[3]
                }
            except ValueError:
                continue

        return result
