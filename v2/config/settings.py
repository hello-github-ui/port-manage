#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : settings.py
# @Software: PyCharm
# @Description:
#   全局配置模块，集中管理应用运行参数。
#   对应 Java 版 application.yml 中的 port-manage.scan 配置项。
#   后续如需持久化，可改为读取 JSON / QSettings，此处先用常量集中托管。
# ======================================================================

# ----------------------------------------------------------------------
# 扫描相关配置
# ----------------------------------------------------------------------

# 自动刷新间隔（毫秒）。对应 Java 版 @Scheduled(fixedDelay = 5000)。
# 前端 PyQt5 通过 QTimer 触发后台扫描，避免阻塞 UI 线程。
SCAN_INTERVAL_MS = 5000

# 常用端口列表（对应 application.yml 中的 common-ports）。
# 用于筛选栏「常用端口」下拉框的快速定位。
COMMON_PORTS = [80, 443, 3000, 3306, 5432, 6379, 8000, 8080, 8888, 9000, 9527]

# 开发进程识别关键字（对应 application.yml 中的 dev-process-keywords）。
# 进程名/命令行命中任一关键字即判定为「开发进程」。
# 后续可扩展为正则匹配。
DEV_PROCESS_KEYWORDS = [
    "idea", "java", "tace", "claude", "springboot",
    "node", "v2", "maven", "gradle",
]

# ----------------------------------------------------------------------
# 端口类型识别用的端口集合（对应 Java PortTypeIdentifier 中的硬编码集合）
# ----------------------------------------------------------------------

# 前端端口：常见前端开发服务器端口
FRONTEND_PORTS = {3000, 3001, 4200, 5173, 8081, 9000, 9090}

# 后端端口：常见后端服务端口
BACKEND_PORTS = {8080, 8000, 8888, 9527, 7001, 7002, 5000, 80, 443}

# 数据库端口：port -> 服务名映射，便于在 UI 上展示可读标签
DATABASE_PORTS = {
    3306: "MySQL",
    5432: "PostgreSQL",
    6379: "Redis",
    27017: "MongoDB",
    1521: "Oracle",
    1433: "SQLServer",
    9200: "Elasticsearch",
    9300: "ES-Cluster",
    8086: "InfluxDB",
    9042: "Cassandra",
    33060: "MySQL-X",
}

# ----------------------------------------------------------------------
# 应用信息
# ----------------------------------------------------------------------

APP_TITLE = "端口管理工具"
APP_VERSION = "v1.0.0"
APP_AUTHOR = "QiYue"
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 750
ICON_PATH = "v2/icon.ico"
