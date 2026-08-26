#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/26
# @Author  : 19921224
# @File    : cmd_util.py
# @Software: PyCharm
# @Description:
#   跨平台命令执行工具类。封装subprocess调用，统一处理Windows/Mac/Linux差异。
#   所有需要执行系统命令的地方（扫描器、进程管理）都通过本工具调用，
#   避免代码中散落大量subprocess.Popen和平台判断。
# ======================================================================

import subprocess
import sys
from typing import List, Optional, Tuple


def run_command(cmd: List[str], timeout: int = 10, encoding: str = None) -> Tuple[bool, str, str]:
    """
    跨平台执行系统命令，返回(是否成功, stdout, stderr)。

    :param cmd: 命令参数列表，如 ["netstat", "-ano"] 或 ["cmd", "/c", "tasklist"]
    :param timeout: 超时时间（秒），默认10秒，避免命令挂死
    :param encoding: 输出编码，Windows默认gbk，Mac/Linux默认utf-8
    :return: (success, stdout_str, stderr_str)
    """
    if encoding is None:
        if sys.platform == "win32":
            encoding = "gbk"
        else:
            encoding = "utf-8"

    try:
        # startupinfo仅用于Windows，隐藏命令行窗口
        startupinfo = None
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0  # SW_HIDE

        proc = subprocess.run(
            cmd,
            capture_output=True,
            timeout=timeout,
            startupinfo=startupinfo,
            shell=False
        )

        stdout = proc.stdout.decode(encoding, errors="replace") if proc.stdout else ""
        stderr = proc.stderr.decode(encoding, errors="replace") if proc.stderr else ""
        return proc.returncode == 0, stdout, stderr

    except subprocess.TimeoutExpired:
        return False, "", f"Command timed out after {timeout}s: {' '.join(cmd)}"
    except Exception as e:
        return False, "", str(e)


def run_powershell(ps_command: str, timeout: int = 15) -> Tuple[bool, str]:
    """
    执行PowerShell命令（Windows专用），返回(是否成功, 输出)。
    Mac/Linux调用此函数会返回失败。

    :param ps_command: PowerShell命令字符串
    :param timeout: 超时时间
    """
    if sys.platform != "win32":
        return False, "PowerShell is only available on Windows"

    cmd = ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_command]
    success, stdout, stderr = run_command(cmd, timeout=timeout, encoding="utf-8")
    return success, stdout if success else stderr


def run_shell_command(shell_cmd: str, timeout: int = 10) -> Tuple[bool, str, str]:
    """
    使用系统shell执行命令（简单场景用，注意shell注入风险）。

    :param shell_cmd: shell命令字符串，如 "netstat -ano | findstr LISTENING"
    """
    try:
        startupinfo = None
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0

        proc = subprocess.run(
            shell_cmd,
            capture_output=True,
            timeout=timeout,
            startupinfo=startupinfo,
            shell=True
        )

        encoding = "gbk" if sys.platform == "win32" else "utf-8"
        stdout = proc.stdout.decode(encoding, errors="replace") if proc.stdout else ""
        stderr = proc.stderr.decode(encoding, errors="replace") if proc.stderr else ""
        return proc.returncode == 0, stdout, stderr

    except Exception as e:
        return False, "", str(e)
