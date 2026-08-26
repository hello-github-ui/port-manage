#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : process_service.py
# @Software: PyCharm
# @Description:
#   进程管理服务（跨平台），对应 Java 版 ProcessManageService。
#
#   功能：
#     1. 强制杀死进程（Windows: taskkill /F；Mac/Linux: kill -9）
#     2. 检查进程是否存活
#     3. Windows: 永久停止系统服务（sc stop / PowerShell Stop-Service）
#     4. Mac: 永久停止brew/launchd服务
#     5. Linux: 永久停止systemd服务
# ======================================================================

import sys
from typing import List, Optional, Tuple

from v2.utils.cmd_util import run_command, run_powershell


class ProcessService:
    """跨平台进程管理服务。"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def kill_process(self, pid: int, force: bool = True) -> Tuple[bool, str]:
        """
        杀死指定PID的进程。

        :param pid: 进程ID
        :param force: 是否强制杀死（Windows: /F；Mac/Linux: -9）
        :return: (是否成功, 消息)
        """
        if pid <= 0:
            return False, "无效的进程ID"

        if sys.platform == "win32":
            return self._kill_process_windows(pid, force)
        else:
            return self._kill_process_unix(pid, force)

    def kill_processes(self, pids: List[int], force: bool = True) -> Tuple[int, List[str]]:
        """
        批量杀死多个进程。

        :return: (成功杀死的数量, 失败消息列表)
        """
        success_count = 0
        errors = []
        for pid in pids:
            ok, msg = self.kill_process(pid, force)
            if ok:
                success_count += 1
            else:
                errors.append(f"PID {pid}: {msg}")
        return success_count, errors

    def is_process_alive(self, pid: int) -> bool:
        """检查进程是否存活。"""
        if pid <= 0:
            return False

        if sys.platform == "win32":
            return self._is_alive_windows(pid)
        else:
            return self._is_alive_unix(pid)

    def stop_service_permanently(self, pid: int) -> Tuple[bool, str, Optional[str]]:
        """
        永久停止进程对应的系统服务（进程下次开机不会自动启动）。

        :param pid: 进程ID
        :return: (是否成功, 消息, 服务名)
                 如果不是系统服务，返回(False, "不是系统服务", None)
        """
        if sys.platform == "win32":
            return self._stop_windows_service(pid)
        elif sys.platform == "darwin":
            return self._stop_mac_service(pid)
        else:
            return self._stop_linux_service(pid)

    def get_service_name_for_pid(self, pid: int) -> Optional[str]:
        """
        查找PID对应的系统服务名，如果不是系统服务返回None。
        """
        if sys.platform == "win32":
            return self._find_windows_service_by_pid(pid)
        elif sys.platform == "darwin":
            return self._find_mac_service_by_pid(pid)
        else:
            return self._find_linux_service_by_pid(pid)

    # ------------------------------------------------------------------
    # Windows 平台实现
    # ------------------------------------------------------------------

    @staticmethod
    def _kill_process_windows(pid: int, force: bool) -> Tuple[bool, str]:
        """Windows: taskkill /F /PID {pid}"""
        cmd = ["taskkill"]
        if force:
            cmd.append("/F")
        cmd.extend(["/PID", str(pid)])

        success, stdout, stderr = run_command(cmd, timeout=10)
        output = (stdout + stderr).strip()

        if success:
            return True, f"成功杀死进程 {pid}"
        else:
            # 常见错误：进程不存在 / 权限不足
            if "not found" in output.lower() or "没有找到" in output:
                return False, f"进程 {pid} 不存在"
            elif "access is denied" in output.lower() or "拒绝访问" in output:
                return False, f"权限不足，无法杀死进程 {pid}（可能需要管理员权限）"
            else:
                return False, f"杀死进程失败: {output}"

    @staticmethod
    def _is_alive_windows(pid: int) -> bool:
        """Windows: tasklist /FI "PID eq {pid}" 检查进程是否存在。"""
        cmd = ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"]
        success, stdout, _ = run_command(cmd, timeout=5)
        if not success or not stdout.strip():
            return False
        # 如果有输出，且包含PID，说明进程存在
        return str(pid) in stdout

    @staticmethod
    def _find_windows_service_by_pid(pid: int) -> Optional[str]:
        """
        Windows: 使用PowerShell查找PID对应的Windows服务名。
        查询Win32_Service中ProcessId等于指定PID的服务。
        """
        ps_script = f'''
Get-CimInstance Win32_Service | Where-Object {{ $_.ProcessId -eq {pid} }} | 
Select-Object -First 1 -ExpandProperty Name
'''
        success, output = run_powershell(ps_script, timeout=10)
        if success and output.strip():
            return output.strip()
        return None

    @staticmethod
    def _stop_windows_service(pid: int) -> Tuple[bool, str, Optional[str]]:
        """
        Windows: 停止系统服务并禁用开机启动。
          1. 先查找PID对应的服务名
          2. 使用 sc stop 停止服务
          3. 使用 sc config 服务名 start= disabled 禁用开机启动
        """
        service_name = ProcessService._find_windows_service_by_pid(pid)
        if not service_name:
            return False, "该进程不是Windows系统服务", None

        # 第一步：停止服务
        stop_ok, stop_out, stop_err = run_command(
            ["sc", "stop", service_name], timeout=15
        )
        stop_output = (stop_out + stop_err).strip()

        # 第二步：禁用开机启动
        disable_ok, disable_out, disable_err = run_command(
            ["sc", "config", service_name, "start=", "disabled"], timeout=10
        )
        disable_output = (disable_out + disable_err).strip()

        if stop_ok or "STOP_PENDING" in stop_output:
            return True, f"已停止并禁用Windows服务: {service_name}", service_name
        else:
            return False, f"停止服务失败: {stop_output}", service_name

    # ------------------------------------------------------------------
    # macOS 平台实现
    # ------------------------------------------------------------------

    @staticmethod
    def _kill_process_unix(pid: int, force: bool) -> Tuple[bool, str]:
        """Mac/Linux: kill -9 {pid} 或 kill {pid}"""
        signal = "-9" if force else "-TERM"
        cmd = ["kill", signal, str(pid)]

        success, stdout, stderr = run_command(cmd, timeout=10)
        output = (stdout + stderr).strip()

        if success:
            return True, f"成功杀死进程 {pid}"
        else:
            if "No such process" in output or "没有那个进程" in output:
                return False, f"进程 {pid} 不存在"
            elif "Operation not permitted" in output or "不允许的操作" in output:
                return False, f"权限不足，无法杀死进程 {pid}（可能需要sudo）"
            else:
                return False, f"杀死进程失败: {output}"

    @staticmethod
    def _is_alive_unix(pid: int) -> bool:
        """Mac/Linux: kill -0 {pid} 检查进程是否存在（不发送实际信号）"""
        cmd = ["kill", "-0", str(pid)]
        success, _, _ = run_command(cmd, timeout=5)
        return success

    @staticmethod
    def _find_mac_service_by_pid(pid: int) -> Optional[str]:
        """
        macOS: 查找PID对应的launchd服务。
        使用 launchctl list 查找对应的服务标签。
        """
        # brew services 检查
        success, stdout, _ = run_command(["brew", "services", "list"], timeout=10)
        if success:
            for line in stdout.splitlines()[1:]:
                parts = line.split()
                if len(parts) >= 2 and parts[1].isdigit() and int(parts[1]) == pid:
                    return parts[0]

        # launchctl list 检查
        success, stdout, _ = run_command(["launchctl", "list"], timeout=10)
        if success:
            for line in stdout.splitlines()[1:]:
                parts = line.split()
                if len(parts) >= 3 and parts[0].isdigit() and int(parts[0]) == pid:
                    return parts[2]

        return None

    @staticmethod
    def _stop_mac_service(pid: int) -> Tuple[bool, str, Optional[str]]:
        """macOS: 停止brew/launchd服务。"""
        service_name = ProcessService._find_mac_service_by_pid(pid)
        if not service_name:
            return False, "该进程不是macOS服务", None

        # 先尝试brew services stop
        success, stdout, stderr = run_command(
            ["brew", "services", "stop", service_name], timeout=15
        )
        if success:
            return True, f"已停止brew服务: {service_name}", service_name

        # brew失败则尝试launchctl
        success, stdout, stderr = run_command(
            ["launchctl", "stop", service_name], timeout=10
        )
        if success:
            # launchctl stop只是停止，需要unload才能永久禁用
            run_command(["launchctl", "unload", "-w",
                         f"~/Library/LaunchAgents/{service_name}.plist"], timeout=10)
            return True, f"已停止launchd服务: {service_name}", service_name

        return False, f"停止服务失败: {stdout + stderr}", service_name

    # ------------------------------------------------------------------
    # Linux 平台实现
    # ------------------------------------------------------------------

    @staticmethod
    def _find_linux_service_by_pid(pid: int) -> Optional[str]:
        """Linux: 查找PID对应的systemd服务。"""
        # systemctl status {pid} --no-pager
        success, stdout, _ = run_command(
            ["systemctl", "status", str(pid), "--no-pager", "-l"],
            timeout=10
        )
        if success:
            for line in stdout.splitlines():
                if line.startswith("●") or ".service" in line:
                    # 提取服务名
                    if ".service" in line:
                        idx = line.index(".service")
                        start = max(0, idx - 30)
                        segment = line[start:idx]
                        # 从后往前找非单词字符
                        for i in range(len(segment) - 1, -1, -1):
                            if not segment[i].isalnum() and segment[i] not in "-_@.":
                                return segment[i + 1:] + ".service"
                        return segment + ".service"

        # 备选：ps -o unit= {pid}（部分systemd版本支持）
        success, stdout, _ = run_command(
            ["ps", "-o", "unit=", "-p", str(pid)], timeout=5
        )
        if success and stdout.strip() and ".service" in stdout:
            return stdout.strip()

        return None

    @staticmethod
    def _stop_linux_service(pid: int) -> Tuple[bool, str, Optional[str]]:
        """Linux: 停止并禁用systemd服务。"""
        service_name = ProcessService._find_linux_service_by_pid(pid)
        if not service_name:
            return False, "该进程不是systemd服务", None

        # 停止服务
        stop_ok, stop_out, stop_err = run_command(
            ["systemctl", "stop", service_name], timeout=15
        )

        # 禁用开机启动
        disable_ok, disable_out, disable_err = run_command(
            ["systemctl", "disable", service_name], timeout=10
        )

        if stop_ok and disable_ok:
            return True, f"已停止并禁用systemd服务: {service_name}", service_name
        else:
            msg = (stop_out + stop_err + disable_out + disable_err).strip()
            return False, f"停止服务失败: {msg}", service_name
