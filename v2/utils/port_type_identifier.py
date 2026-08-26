#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : port_type_identifier.py
# @Software: PyCharm
# @Description:
#   端口 / 进程类型识别工具，对应 Java 版 PortTypeIdentifier（纯静态工具类）。
#   提供三个识别方法，供扫描器在构造 PortInfo 时统一调用。
#
#   跨平台说明：本模块只做字符串匹配，不依赖平台特定命令，
#   Windows/Mac/Linux 扫描器均可安全调用。
# ======================================================================

from v2.config import settings


def identify_process_type(process_name: str, command_line: str = "") -> str:
    """
    识别进程类型，返回以下之一：
      JAVA / NODE / PYTHON / WEB_SERVER / DATABASE /
      IDE / BROWSER / SYSTEM / OTHER

    判定规则（转小写后匹配 process_name 或 command_line）：
    """
    name = (process_name or "").lower()
    cmd = (command_line or "").lower()
    combined = name + " " + cmd

    # SYSTEM 系统进程（优先判断）
    system_keywords = ["systemd", "launchd", "init", "sshd", "cupsd", "cron", "svchost",
                       "lsass", "services", "wininit", "csrss", "smss", "winlogon"]
    if name in system_keywords or "kernel" in name:
        return "SYSTEM"

    # DATABASE 数据库进程
    db_keywords = ["mysql", "postgres", "redis", "mongo", "mongod", "oracle",
                   "sqlserver", "mariadb", "clickhouse", "elastic", "cassandra",
                   "influx", "memcached", "rabbitmq", "kafka"]
    if any(kw in combined for kw in db_keywords):
        return "DATABASE"

    # WEB_SERVER Web服务器
    web_keywords = ["nginx", "httpd", "apache", "apache2", "caddy", "lighttpd", "iisexpress"]
    if any(kw in name for kw in web_keywords):
        return "WEB_SERVER"

    # IDE 开发工具
    ide_keywords = ["idea", "intellij", "pycharm", "webstorm", "vscode", "code",
                    "eclipse", "netbeans", "sublime", "atom", "android studio",
                    "clion", "goland", "phpstorm", "rubymine", "datagrip", "rider"]
    if any(kw in name for kw in ide_keywords):
        return "IDE"

    # BROWSER 浏览器
    browser_keywords = ["chrome", "firefox", "safari", "msedge", "edge", "opera", "brave"]
    if any(kw in name for kw in browser_keywords):
        return "BROWSER"

    # JAVA 进程
    if "java" in name or "javaw" in name:
        return "JAVA"

    # NODE 进程
    node_keywords = ["node", "npm", "yarn", "pnpm"]
    if any(kw == name or name.startswith(kw + ".") or name.startswith(kw + "-") for kw in node_keywords):
        # 排除node被包含在其他词里的情况，进一步检查命令行
        if any(kw in name for kw in node_keywords):
            return "NODE"

    # PYTHON 进程
    if name.startswith("python"):
        return "PYTHON"

    return "OTHER"


def identify_port_type(port: int, process_name: str = "",
                       command_line: str = "") -> str:
    """
    识别端口类型，返回以下之一：
      FRONTEND / BACKEND / DATABASE / OTHER
    """
    name = (process_name or "").lower()
    cmd = (command_line or "").lower()
    combined = name + " " + cmd

    # DATABASE: 进程名含数据库关键字 或 端口是常见数据库端口
    db_keywords = ["mysql", "postgres", "redis", "mongo", "mongod", "oracle",
                   "sqlserver", "mariadb", "clickhouse", "elasticsearch"]
    db_ports = set(settings.DATABASE_PORTS.keys())
    if any(kw in combined for kw in db_keywords) or port in db_ports:
        return "DATABASE"

    # FRONTEND: 常见前端进程关键字 或 前端常用端口
    frontend_keywords = ["webpack", "vite", "react", "vue", "angular", "next",
                         "nuxt", "gatsby", "svelte", "parcel", "rollup", "esbuild"]
    frontend_ports = {3000, 3001, 4200, 5173, 5174, 8081, 9000, 9090, 8082, 8889}
    if any(kw in combined for kw in frontend_keywords) or port in frontend_ports:
        return "FRONTEND"

    # BACKEND: 常见后端进程关键字 或 后端常用端口
    backend_keywords_java = ["spring", "tomcat", "jetty", ".jar", "springboot"]
    backend_keywords_python = ["django", "flask", "fastapi", "uvicorn", "gunicorn", "tornado"]
    backend_keywords_go = ["gin", "beego", "echo", "fiber"]
    backend_keywords_node = ["express", "koa", "nest", "fastify", "hapi"]
    backend_ports = {8080, 8000, 8888, 9527, 7001, 7002, 5000, 80, 443, 9001, 3000}

    is_backend = False
    if "java" in name and any(kw in combined for kw in backend_keywords_java):
        is_backend = True
    elif name.startswith("python") and any(kw in combined for kw in backend_keywords_python):
        is_backend = True
    elif any(kw in combined for kw in backend_keywords_node) and "node" in name:
        is_backend = True
    elif port in backend_ports:
        # 端口匹配但要排除已判定为前端/数据库的情况
        if port not in frontend_ports and port not in db_ports:
            is_backend = True

    if is_backend:
        return "BACKEND"

    return "OTHER"


def is_development_process(process_name: str, command_line: str = "") -> bool:
    """
    判断是否为开发进程：将进程名与命令行拼接转小写后，
    命中 config.settings.DEV_PROCESS_KEYWORDS 任一关键字即为 True。
    对应 Java 版 isDevProcess。
    """
    name = (process_name or "").lower()
    cmd = (command_line or "").lower()
    combined = name + " " + cmd
    return any(kw in combined for kw in settings.DEV_PROCESS_KEYWORDS)
