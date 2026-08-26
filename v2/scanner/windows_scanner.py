#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : windows_scanner.py
# @Software: PyCharm
# @Description:
#   Windows 平台端口扫描器，对应 Java 版 WindowsPortScanner。
#
#   实现原理：
#     1. 执行 netstat -ano 获取所有监听端口和对应PID
#     2. 批量执行 tasklist /FO CSV /NH 获取所有进程名（比逐个PID查询高效）
#     3. 使用PowerShell Get-CimInstance批量获取进程命令行（替代已弃用的wmic）
#     4. 调用 port_type_identifier 识别端口类型和进程类型
#
#   性能优化：批量获取进程信息，而不是每个PID单独执行命令。
# ======================================================================

import re
from typing import Dict, List, Optional

from v2.model.port_info import PortInfo
from v2.scanner.port_scanner import PortScanner
from v2.utils.cmd_util import run_command, run_powershell
from v2.utils.port_type_identifier import (identify_port_type,
                                           identify_process_type,
                                           is_development_process)

# netstat输出正则：协议  本地地址  外部地址  状态  PID
# 示例行: TCP    0.0.0.0:135            0.0.0.0:0              LISTENING       1192
NETSTAT_PATTERN = re.compile(
    r'^\s*(TCP|UDP)\s+(\S+?):(\d+)\s+\S+:\d+\s+(\S+)?\s*(\d+)\s*$',
    re.MULTILINE
)


class WindowsPortScanner(PortScanner):
    """Windows 平台端口扫描器。"""

    def scan_ports(self) -> List[PortInfo]:
        """
        扫描所有监听端口。
        """
        # 第一步：netstat获取端口-PID映射
        netstat_data = self._get_netstat_output()
        if not netstat_data:
            return []

        # 解析netstat，收集所有PID
        port_pid_map: Dict[int, dict] = {}  # port -> {protocol, pid, status, local_addr}
        pids = set()

        for match in NETSTAT_PATTERN.finditer(netstat_data):
            protocol = match.group(1)
            local_addr = match.group(2)
            port = int(match.group(3))
            status = match.group(4) or ""
            pid = int(match.group(5))

            # 只保留LISTENING状态的TCP端口（UDP没有状态，也保留）
            if protocol == "TCP" and status.upper() != "LISTENING":
                continue

            if port in port_pid_map:
                continue  # 同端口多个PID时取第一个（后续可以支持多PID）

            # 过滤掉PID 0（System Idle Process，不是真正的监听进程）
            if pid == 0:
                continue

            port_pid_map[port] = {
                "protocol": protocol,
                "pid": pid,
                "status": status.upper() or "",
                "local_addr": local_addr
            }
            pids.add(pid)

        if not port_pid_map:
            return []

        # 第二步：批量获取进程名（tasklist）
        process_names = self._get_all_process_names()

        # 第三步：批量获取命令行（PowerShell）
        command_lines = self._get_all_command_lines()

        # 第四步：组装PortInfo并进行类型识别
        result = []
        for port, info in port_pid_map.items():
            pid = info["pid"]
            proc_name = process_names.get(pid, f"PID_{pid}" if pid > 0 else "System")
            cmd_line = command_lines.get(pid, "")

            # 识别类型
            proc_type = identify_process_type(proc_name, cmd_line)
            port_type = identify_port_type(port, proc_name, cmd_line)
            is_dev = is_development_process(proc_name, cmd_line)

            port_info = PortInfo(
                port=port,
                protocol=info["protocol"],
                status=info["status"],
                pid=pid,
                process_name=proc_name,
                command_line=cmd_line,
                is_development_process=is_dev,
                user="",  # Windows netstat/tasklist不直接显示用户，暂不填充
                local_address=info["local_addr"],
                port_type=port_type,
                process_type=proc_type
            )
            result.append(port_info)

        return result

    def scan_port(self, port: int) -> Optional[PortInfo]:
        """扫描指定端口。"""
        success, stdout, _ = run_command(
            ["cmd", "/c", f"netstat -ano | findstr :{port} | findstr LISTENING"],
            timeout=5
        )
        if not success or not stdout.strip():
            return None

        for p in self.scan_ports():
            if p.port == port:
                return p
        return None

    # ------------------------------------------------------------------
    # 内部辅助方法
    # ------------------------------------------------------------------

    @staticmethod
    def _get_netstat_output() -> str:
        """执行netstat -ano获取原始输出。"""
        # -a: 所有连接和监听端口
        # -n: 数字形式显示地址和端口
        # -o: 显示拥有的与每个连接关联的进程ID
        success, stdout, stderr = run_command(
            ["netstat", "-ano"],
            timeout=10
        )
        return stdout if success else ""

    @staticmethod
    def _get_all_process_names() -> Dict[int, str]:
        """
        批量获取所有进程名，返回 {pid: process_name}。
        使用tasklist /FO CSV格式解析。
        """
        result = {}
        success, stdout, _ = run_command(
            ["tasklist", "/FO", "CSV", "/NH"],
            timeout=10
        )
        if not success:
            return result

        # CSV格式: "进程名","PID","会话名","会话#","内存使用"
        # 示例: "svchost.exe","1192","Services","0","14,240 K"
        for line in stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            # 简单CSV解析（处理引号）
            parts = []
            current = ""
            in_quotes = False
            for ch in line:
                if ch == '"':
                    in_quotes = not in_quotes
                elif ch == ',' and not in_quotes:
                    parts.append(current)
                    current = ""
                else:
                    current += ch
            parts.append(current)

            if len(parts) >= 2:
                try:
                    pid = int(parts[1])
                    name = parts[0].strip('"')
                    # 去掉.exe后缀
                    if name.lower().endswith(".exe"):
                        name = name[:-4]
                    result[pid] = name
                except (ValueError, IndexError):
                    continue

        return result

    @staticmethod
    def _get_all_command_lines() -> Dict[int, str]:
        """
        使用PowerShell批量获取所有进程的命令行，返回 {pid: command_line}。
        使用Get-CimInstance替代已弃用的wmic命令。
        """
        result = {}

        ps_script = '''
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -ne $null } | 
Select-Object ProcessId, CommandLine | 
ForEach-Object { "{0}`t{1}" -f $_.ProcessId, $_.CommandLine }
'''

        success, output = run_powershell(ps_script, timeout=15)
        if not success:
            return result

        for line in output.splitlines():
            line = line.strip()
            if not line:
                continue
            # PID和CommandLine用tab分隔
            if "\t" in line:
                pid_str, cmd = line.split("\t", 1)
                try:
                    pid = int(pid_str.strip())
                    result[pid] = cmd.strip()
                except ValueError:
                    continue

        return result
