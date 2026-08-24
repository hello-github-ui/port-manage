#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : port_info.py
# @Software: PyCharm
# @Description:
#   端口信息数据模型，对应 Java 版 com.portmanager.web.model.PortInfo。
#   使用 dataclass 简化定义，自动生成 __init__ / __repr__ 等方法。
#   该类只承载「数据」，不包含业务逻辑，便于在各层之间传递。
# ======================================================================

from dataclasses import dataclass
from typing import Optional


@dataclass
class PortInfo:
    """
    单条端口占用信息。

    字段与 Java PortInfo 一一对应：
      - port:                  端口号
      - protocol:              协议（TCP / UDP）
      - status:                状态（如 LISTENING）
      - pid:                   占用端口的进程 ID
      - process_name:          进程名（如 mysqld.exe / java）
      - process_path:          进程可执行文件路径（当前未填充，预留）
      - command_line:          进程完整命令行（用于类型识别与展示）
      - is_development_process:是否为开发进程（命中 DEV_PROCESS_KEYWORDS）
      - user:                  进程所属用户（仅 Mac 填充，Windows 暂为空）
      - local_address:         本地监听地址（如 0.0.0.0 / 127.0.0.1 / *）
      - port_type:             端口类型 FRONTEND/BACKEND/DATABASE/OTHER
      - process_type:          进程类型 JAVA/NODE/PYTHON/WEB_SERVER/
                               DATABASE/IDE/BROWSER/SYSTEM/OTHER
    """

    port: int = 0
    protocol: str = ""
    status: str = ""
    pid: int = 0
    process_name: str = ""
    process_path: Optional[str] = ""
    command_line: str = ""
    is_development_process: bool = False
    user: str = ""
    local_address: str = ""
    port_type: str = "OTHER"
    process_type: str = "OTHER"
