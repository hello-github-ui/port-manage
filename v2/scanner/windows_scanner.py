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

# 本地地址:端口 匹配（支持IPv6 [::]:port格式）
LOCAL_ADDR_PATTERN = re.compile(r'\[?([^\s\]]+)\]?:(\d+)')
# PID 是行尾的数字
PID_PATTERN = re.compile(r'(\d+)\s*$')


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
        port_pid_map: Dict[tuple, dict] = {}  # (protocol, port, pid) -> {protocol, pid, status, local_addr}
        pids = set()

        for line in netstat_data.splitlines():
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) < 3:
                continue

            protocol = parts[0]
            if protocol not in ("TCP", "UDP"):
                continue

            # 解析本地地址:端口
            local_addr_port = parts[1]
            addr_match = LOCAL_ADDR_PATTERN.search(local_addr_port)
            if not addr_match:
                continue
            local_addr = addr_match.group(1)
            port = int(addr_match.group(2))

            # 外部地址（第3列）
            foreign_addr = parts[2] if len(parts) >= 3 else ""

            # 解析PID（最后一个字段）
            pid_match = PID_PATTERN.search(line)
            if not pid_match:
                continue
            pid = int(pid_match.group(1))

            # 解析状态：TCP有状态，UDP没有
            # TCP格式: parts = [TCP, 本地地址, 外部地址, 状态, PID] (至少5个字段)
            # UDP格式: parts = [UDP, 本地地址, 外部地址, PID] (只有4个字段，无状态列)
            status = ""
            if protocol == "TCP":
                # TCP需要至少5列：Proto Local Foreign State PID
                if len(parts) < 5:
                    continue
                status = parts[3]
                if status not in ("LISTENING", "ESTABLISHED", "TIME_WAIT", "CLOSE_WAIT", "SYN_SENT", "SYN_RECEIVED"):
                    continue
                # 只保留LISTENING状态的TCP端口
                if status != "LISTENING":
                    continue
            else:
                # UDP：只保留外部地址为 *:* 的条目（表示正在监听），
                # 外部地址是具体IP:port的是临时对外通信，不需要显示
                if not foreign_addr.startswith("*"):
                    continue
                status = ""

            # 过滤掉PID 0（System Idle Process，不是真正的监听进程）
            if pid == 0:
                continue

            # 按(protocol, port, pid)去重（同一个端口可能被多个进程/协议使用）
            key = (protocol, port, pid)
            if key in port_pid_map:
                continue

            port_pid_map[key] = {
                "protocol": protocol,
                "pid": pid,
                "status": status,
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
        for (proto, port_num, pid_key), info in port_pid_map.items():
            pid = info["pid"]
            proc_name = process_names.get(pid, f"PID_{pid}" if pid > 0 else "System")
            cmd_line = command_lines.get(pid, "")

            # 识别类型
            proc_type = identify_process_type(proc_name, cmd_line)
            port_type = identify_port_type(port_num, proc_name, cmd_line)
            is_dev = is_development_process(proc_name, cmd_line)

            port_info = PortInfo(
                port=port_num,
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
