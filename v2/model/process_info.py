#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : process_info.py
# @Software: PyCharm
# @Description:
#   进程详细信息数据模型，对应 Java 版 com.portmanager.web.model.ProcessInfo。
#   用于「关闭进程 / 查看进程详情」时承载单条进程的完整信息。
# ======================================================================

from dataclasses import dataclass
from typing import Optional


@dataclass
class ProcessInfo:
    """
    进程详细信息。

    与 PortInfo 的区别：PortInfo 侧重「端口视角」，ProcessInfo 侧重
    「进程视角」。例如关闭进程前，可用 ProcessInfo 展示该进程的完整命令行
    与所属用户，供用户确认。
    """

    pid: int = 0
    process_name: str = ""
    process_path: Optional[str] = ""
    command_line: str = ""
    is_development_process: bool = False
    start_time: str = ""  # 进程启动时间（当前未填充，预留）
    user: str = ""  # 进程所属用户
