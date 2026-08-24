#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : process_service.py
# @Software: PyCharm
# @Description:
#   进程管理服务，对应 Java 版 ProcessManageService。
#   职责：临时关闭进程、永久停止系统服务、检查进程存活、获取进程详情。
#   当前为占位实现，仅给出方法签名与待实现要点。
#
#   TODO（迁移要点）：
#     1. 临时关闭：
#        - Windows: cmd /c taskkill /F /PID {pid}
#        - Mac/Linux: sh -c "kill -9 {pid}"
#     2. 永久停止（Mac 独有 launchd 管理）：
#        - launchctl list 找 PID 对应服务 Label
#        - homebrew 服务: brew services stop {name}
#        - 普通服务: launchctl stop / launchctl unload
#     3. Windows 永久停止增强（Java 版缺失）：
#        - sc queryex type= service state= all 找 PID 对应服务名
#        - sc stop {service} 或 powershell Stop-Service
#     4. 进程是否存在：
#        - Windows: tasklist /FI "PID eq {pid}"
#        - Mac/Linux: ps -p {pid}
#     5. 所有外部命令建议用 QProcess 异步执行，结果通过信号回传 UI
# ======================================================================

from v2.scanner.scanner_factory import get_os_type


class ProcessService:
    """进程管理服务（占位实现）。"""

    def kill_process(self, pid: int) -> bool:
        """
        临时关闭进程。

        TODO: 按平台执行 taskkill / kill -9，当前仅返回 False。
        """
        # TODO: 实现真实关闭逻辑
        return False

    def kill_process_permanently(self, pid: int) -> bool:
        """
        永久停止进程（针对系统服务，避免自动重启）。

        TODO:
          - Mac: launchd 服务管理（brew services stop / launchctl stop/unload）
          - Windows: 增强 sc stop / Stop-Service
        当前仅返回 False。
        """
        # TODO: 实现永久停止逻辑
        return False

    def is_process_alive(self, pid: int) -> bool:
        """检查进程是否存在。TODO: tasklist / ps -p，当前返回 True。"""
        # TODO: 实现存活检查
        return True

    @staticmethod
    def get_os_type() -> str:
        """返回当前系统类型，供 UI 层展示与逻辑分支使用。"""
        return get_os_type()
