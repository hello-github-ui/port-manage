#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : mock_util.py
# @Software: PyCharm
# @Description:
#   模拟数据生成器。在真实扫描器尚未接入前，为界面提供占位数据，
#   覆盖前端/后端/数据库/IDE/系统等多种类型，便于验证界面展示效果。
#   待 scanner 接入后，本模块仅作开发调试用途。
# ======================================================================

from typing import List

from v2.model.port_info import PortInfo


def generate_mock_ports() -> List[PortInfo]:
    """生成一组覆盖多类型的模拟端口数据。"""
    return [
        PortInfo(
            port=3306, protocol="TCP", status="LISTENING", pid=24883,
            process_name="mysqld.exe",
            command_line="C:\\Program Files\\MySQL\\mysqld.exe --defaults-file=my.ini",
            is_development_process=False, user="",
            local_address="0.0.0.0",
            port_type="DATABASE", process_type="DATABASE",
        ),
        PortInfo(
            port=6379, protocol="TCP", status="LISTENING", pid=19876,
            process_name="redis-server.exe",
            command_line="C:\\Redis\\redis-server.exe --port 6379",
            is_development_process=False, user="",
            local_address="0.0.0.0",
            port_type="DATABASE", process_type="DATABASE",
        ),
        PortInfo(
            port=5432, protocol="TCP", status="LISTENING", pid=21034,
            process_name="postgres.exe",
            command_line="C:\\PostgreSQL\\bin\\postgres.exe -D data",
            is_development_process=False, user="",
            local_address="127.0.0.1",
            port_type="DATABASE", process_type="DATABASE",
        ),
        PortInfo(
            port=3000, protocol="TCP", status="LISTENING", pid=5120,
            process_name="node.exe",
            command_line="node C:\\project\\frontend\\node_modules\\vite\\bin\\vite.js",
            is_development_process=True, user="",
            local_address="0.0.0.0",
            port_type="FRONTEND", process_type="NODE",
        ),
        PortInfo(
            port=8080, protocol="TCP", status="LISTENING", pid=33445,
            process_name="java.exe",
            command_line="java -jar springboot-demo.jar --server.port=8080",
            is_development_process=True, user="",
            local_address="0.0.0.0",
            port_type="BACKEND", process_type="JAVA",
        ),
        PortInfo(
            port=8000, protocol="TCP", status="LISTENING", pid=28891,
            process_name="python.exe",
            command_line="python manage.py runserver 0.0.0.0:8000",
            is_development_process=True, user="",
            local_address="0.0.0.0",
            port_type="BACKEND", process_type="PYTHON",
        ),
        PortInfo(
            port=63342, protocol="TCP", status="LISTENING", pid=47036,
            process_name="pycharm64.exe",
            command_line="C:\\Program Files\\JetBrains\\PyCharm\\bin\\pycharm64.exe",
            is_development_process=True, user="",
            local_address="127.0.0.1",
            port_type="OTHER", process_type="IDE",
        ),
        PortInfo(
            port=135, protocol="TCP", status="LISTENING", pid=1192,
            process_name="svchost.exe",
            command_line="C:\\WINDOWS\\system32\\svchost.exe -k RPCSS -p",
            is_development_process=False, user="",
            local_address="0.0.0.0",
            port_type="OTHER", process_type="SYSTEM",
        ),
        PortInfo(
            port=9527, protocol="TCP", status="LISTENING", pid=55612,
            process_name="java.exe",
            command_line="java -jar port-manage-web.jar --server.port=9527",
            is_development_process=True, user="",
            local_address="0.0.0.0",
            port_type="BACKEND", process_type="JAVA",
        ),
    ]
