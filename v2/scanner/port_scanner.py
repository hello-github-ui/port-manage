#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : port_scanner.py
# @Software: PyCharm
# @Description:
#   端口扫描器抽象基类，对应 Java 版 com.portmanager.web.scanner.PortScanner 接口。
#   定义统一的扫描契约，由 WindowsPortScanner / MacPortScanner 分别实现，
#   上层（ScanService）只依赖抽象，不依赖具体平台实现 —— 面向接口编程。
# ======================================================================

from abc import ABC, abstractmethod
from typing import List, Optional

from v2.model.port_info import PortInfo


class PortScanner(ABC):
    """
    端口扫描器抽象基类。

    子类需实现两个方法：
      - scan_ports():  扫描所有处于监听状态的端口
      - scan_port():   扫描指定端口（未占用返回 None）
    """

    @abstractmethod
    def scan_ports(self) -> List[PortInfo]:
        """扫描本机所有监听端口，返回 PortInfo 列表。"""
        raise NotImplementedError

    @abstractmethod
    def scan_port(self, port: int) -> Optional[PortInfo]:
        """扫描指定端口，未占用返回 None。"""
        raise NotImplementedError
