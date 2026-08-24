#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : scanner_factory.py
# @Software: PyCharm
# @Description:
#   扫描器工厂，对应 Java 版 PortScannerFactory。
#   根据当前操作系统返回对应的扫描器实例，屏蔽平台差异，
#   上层只需调用 get_scanner() 即可，无需关心具体平台。
# ======================================================================

import platform

from v2.scanner.mac_scanner import MacPortScanner
from v2.scanner.port_scanner import PortScanner
from v2.scanner.windows_scanner import WindowsPortScanner


def get_os_type() -> str:
    """
    返回当前操作系统类型字符串。
      - 包含 'mac' / 'darwin' -> 'Mac'
      - 包含 'win'            -> 'Windows'
      - 其他（Linux 等）      -> 'Linux'
    """
    name = platform.system().lower()
    if "mac" in name or "darwin" in name:
        return "Mac"
    if "win" in name:
        return "Windows"
    return "Linux"


def get_scanner() -> PortScanner:
    """
    根据操作系统返回对应扫描器实例。
    Linux 默认复用 MacPortScanner（lsof 在 Linux 通用）。
    """
    os_type = get_os_type()
    if os_type == "Windows":
        return WindowsPortScanner()
    # Mac 与 Linux 都使用基于 lsof 的扫描器
    return MacPortScanner()
