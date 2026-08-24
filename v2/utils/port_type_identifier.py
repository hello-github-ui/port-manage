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
#   注意：Java 版 WindowsPortScanner 未调用本逻辑，导致 Windows 下
#   port_type/process_type 为 null。本实现要求两个平台扫描器都调用，
#   统一修复该缺陷。
#
#   当前为占位实现（统一返回 OTHER / False），真实判定规则以注释给出，
#   后续按注释实现即可。
# ======================================================================

from v2.config import settings


def identify_process_type(process_name: str, command_line: str = "") -> str:
    """
    识别进程类型，返回以下之一：
      JAVA / NODE / PYTHON / WEB_SERVER / DATABASE /
      IDE / BROWSER / SYSTEM / OTHER

    判定规则（转小写后匹配 process_name 或 process_name+command_line）：
      JAVA       : 进程名 java；combined 含 spring/tomcat/jetty/.jar
      NODE       : 进程名 node/npm/yarn/pnpm；combined 含 webpack/vite/next/nuxt
      PYTHON     : 进程名 python/python3/python2；combined 含 django/flask/fastapi/uvicorn/gunicorn
      WEB_SERVER : 进程名 nginx/httpd/apache/apache2/caddy/lighttpd
      DATABASE   : 进程名含 mysql/postgres/redis/mongo/mongod/oracle/sqlserver/mariadb/
                   clickhouse/elastic/cassandra/influx
      IDE        : 进程名含 idea/intellij/pycharm/webstorm/vscode/code/eclipse/
                   netbeans/sublime/atom/android studio
      BROWSER    : 进程名含 chrome/firefox/safari/edge/opera/brave
      SYSTEM     : 进程名等于 systemd/launchd/init/sshd/cupsd/cron 或含 kernel
      OTHER      : 兜底

    TODO: 按上述规则实现，当前统一返回 OTHER。
    """
    # TODO: 实现真实判定逻辑
    return "OTHER"


def identify_port_type(port: int, process_name: str = "",
                       command_line: str = "") -> str:
    """
    识别端口类型，返回以下之一：
      FRONTEND / BACKEND / DATABASE / OTHER

    判定规则：
      FRONTEND : combined 含 node/npm/yarn/webpack/vite/react/vue/angular/next/nuxt/gatsby；
                 或端口 ∈ {3000,3001,4200,5173,8081,9000,9090}
      BACKEND  : Java 后端(combined 含 java 且 spring/tomcat/jar/jetty)；
                 Python 后端(combined 含 python 且 django/flask/fastapi/uvicorn/gunicorn)；
                 Go 后端(combined 含 go 且 gin/beego/echo)；
                 Node 后端(combined 含 node 且 express/koa/nest/fastify)；
                 或端口 ∈ {8080,8000,8888,9527,7001,7002,5000,80,443}
      DATABASE : combined 含 mysql/postgres/redis/mongodb/oracle/sqlserver/mariadb/
                 clickhouse/elasticsearch；
                 或端口 ∈ {3306,5432,6379,27017,1521,1433,9200,9300,8086,9042,33060}
      OTHER    : 兜底

    可参考 config.settings 中的 FRONTEND_PORTS / BACKEND_PORTS / DATABASE_PORTS。

    TODO: 按上述规则实现，当前统一返回 OTHER。
    """
    # TODO: 实现真实判定逻辑
    return "OTHER"


def is_development_process(process_name: str, command_line: str = "") -> bool:
    """
    判断是否为开发进程：将进程名与命令行拼接转小写后，
    命中 config.settings.DEV_PROCESS_KEYWORDS 任一关键字即为 True。
    对应 Java 版 isDevProcess。
    """
    combined = (process_name + " " + command_line).lower()
    return any(kw in combined for kw in settings.DEV_PROCESS_KEYWORDS)
