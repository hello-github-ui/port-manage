#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : main_window.py
# @Software: PyCharm
# @Description:
#   主窗口：组装所有子控件，连接信号槽，协调各层协作。
#   对应 Java 版「前端页面 + 后端 Controller」的胶水层。
#
#   设计思路：
#     - 子控件（TopBar/SearchBar/FilterBar/StatsBar/PortTable/StatusBar）
#       只负责自身界面与向外发信号，不互相直接引用。
#     - 本窗口作为「中介者」，接收子控件信号，调用 Service 层处理，
#       再把结果分发回各子控件。这样子控件之间解耦，便于独立维护。
#     - 数据流：
#         ScanService.get_all_ports() -> 原始数据 _all_ports
#         -> 应用 筛选 + 搜索 得到 filtered
#         -> PortTable.set_ports() / StatsBar / TopBar / StatusBar 同步刷新
# ======================================================================

import platform

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QWidget

from v2.config import settings
from v2.service.process_service import ProcessService
from v2.service.scan_service import ScanService
from v2.ui.widgets.filter_bar import FilterBar
from v2.ui.widgets.port_table import PortTable
from v2.ui.widgets.search_bar import SearchBar
from v2.ui.widgets.stats_bar import StatsBar
from v2.ui.widgets.status_bar import StatusBar
from v2.ui.widgets.top_bar import TopBar


def _get_system_font():
    """
    根据操作系统选择最合适的默认字体。
    避免使用 Microsoft YaHei 等可能在部分系统上渲染异常的字体。
    """
    system = platform.system()
    if system == "Windows":
        return "Segoe UI"
    elif system == "Darwin":
        return "SF Pro Text"
    else:
        return "DejaVu Sans"


class MainWindow(QWidget):
    """应用主窗口。"""

    def __init__(self):
        super().__init__()
        # ---- 业务服务层 ----
        self._scan_service = ScanService()
        self._process_service = ProcessService()

        # ---- 视图层状态 ----
        self._all_ports = []
        self._filters = {
            "port_type": "", "process_type": "", "protocol": "",
            "dev_process": None, "common_port": None,
        }
        self._keyword = ""

        # ---- 自动刷新定时器 ----
        self._timer = QTimer(self)
        self._timer.setInterval(settings.SCAN_INTERVAL_MS)
        self._timer.timeout.connect(self._refresh_data)

        self._init_ui()
        self._connect_signals()

        # 启动后立即加载一次数据，并开启自动刷新
        self._refresh_data()
        self._timer.start()

    # ------------------------------------------------------------------
    # UI 构建
    # ------------------------------------------------------------------

    def _init_ui(self):
        """构建主窗口布局。"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 16, 20, 16)

        # 各功能区块
        self.top_bar = TopBar()
        self.search_bar = SearchBar()
        self.filter_bar = FilterBar()
        self.stats_bar = StatsBar()
        self.port_table = PortTable()
        self.status_bar = StatusBar()

        main_layout.addWidget(self.top_bar)
        main_layout.addWidget(self.search_bar)
        main_layout.addWidget(self.filter_bar)
        main_layout.addWidget(self.stats_bar)
        main_layout.addWidget(self.port_table, 1)
        main_layout.addWidget(self.status_bar)

        # 窗口基础属性
        self.setGeometry(300, 300,
                         settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        self.setWindowTitle(settings.APP_TITLE)
        self.setWindowIcon(QIcon(settings.ICON_PATH))

        # 全局字体：使用系统合适的默认字体，避免渲染异常
        font = QFont(_get_system_font(), 9)
        self.setFont(font)

    def _connect_signals(self):
        """连接子控件信号到本窗口的处理方法。"""
        self.top_bar.theme_toggled.connect(self._on_theme_toggle)

        self.search_bar.search_requested.connect(self._on_search)
        self.search_bar.refresh_requested.connect(self._refresh_data)
        self.search_bar.auto_refresh_toggled.connect(self._on_auto_refresh_toggled)
        self.search_bar.batch_kill_requested.connect(self._on_batch_kill)

        self.filter_bar.filter_changed.connect(self._on_filter_changed)

        self.port_table.selection_changed.connect(self._on_selection_changed)
        self.port_table.kill_requested.connect(self._on_kill)

    # ------------------------------------------------------------------
    # 数据加载与视图刷新
    # ------------------------------------------------------------------

    def _refresh_data(self):
        """拉取最新端口数据并刷新视图。"""
        self._all_ports = self._scan_service.get_all_ports()
        self._apply_view()

    def _apply_view(self):
        """根据当前筛选条件与搜索关键字，计算最终展示列表并刷新所有视图。"""
        ports = self._all_ports
        f = self._filters

        # 常用端口为「独占筛选」
        if f.get("common_port"):
            ports = [p for p in ports if p.port == f["common_port"]]
        else:
            if f["port_type"]:
                ports = [p for p in ports if p.port_type == f["port_type"]]
            if f["process_type"]:
                ports = [p for p in ports if p.process_type == f["process_type"]]
            if f["protocol"]:
                ports = [p for p in ports if p.protocol == f["protocol"]]
            if f["dev_process"] is not None:
                ports = [p for p in ports
                         if p.is_development_process == f["dev_process"]]

        if self._keyword:
            ports = self._scan_service.search_ports(ports, self._keyword)

        ports = sorted(ports, key=lambda p: p.port)

        self.port_table.set_ports(ports)
        stats = self._scan_service.get_statistics(self._all_ports)
        self.stats_bar.update_stats(stats, self._scan_service.last_scan_time)
        self.top_bar.update_info(self._process_service.get_os_type(),
                                 len(self._all_ports))
        self.status_bar.set_status(f"加载成功: {len(ports)} 个端口")

    # ------------------------------------------------------------------
    # 信号处理
    # ------------------------------------------------------------------

    def _on_search(self, keyword: str):
        """搜索：记录关键字并重新应用视图。"""
        self._keyword = keyword
        self._apply_view()

    def _on_filter_changed(self, filters: dict):
        """筛选条件变化：更新本地筛选状态并重新应用视图。"""
        self._filters = filters
        if filters.get("common_port"):
            self.search_bar.clear_search()
            self._keyword = ""
        self._apply_view()

    def _on_selection_changed(self, count: int):
        """表格勾选数量变化：更新批量关闭按钮显示。"""
        self.search_bar.set_batch_count(count)

    def _on_auto_refresh_toggled(self, active: bool):
        """自动刷新开关切换。"""
        if active:
            self._timer.start()
            self.status_bar.set_auto_refresh_info(
                f"自动刷新：开启 ({settings.SCAN_INTERVAL_MS // 1000} 秒)")
        else:
            self._timer.stop()
            self.status_bar.set_auto_refresh_info("自动刷新：已暂停")

    def _on_kill(self, port_info):
        """单条「关闭」按钮：弹出确认对话框。"""
        reply = QMessageBox.question(
            self, "确认关闭",
            f"确定要关闭端口 {port_info.port} 上的进程吗？\n"
            f"进程名: {port_info.process_name}\nPID: {port_info.pid}",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            QMessageBox.information(
                self, "提示",
                f"关闭功能尚在开发中（PID={port_info.pid}）。\n"
                "待 ProcessService 接入真实命令后生效。"
            )

    def _on_batch_kill(self):
        """批量关闭：取出勾选项，弹出确认对话框。"""
        checked = self.port_table.get_checked_ports()
        if not checked:
            return
        port_list = "\n".join(
            f"  端口 {p.port}  {p.process_name}  (PID {p.pid})"
            for p in checked
        )
        reply = QMessageBox.question(
            self, "批量关闭确认",
            f"将关闭以下 {len(checked)} 个进程：\n{port_list}\n\n是否继续？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            QMessageBox.information(
                self, "提示",
                f"批量关闭功能尚在开发中（共 {len(checked)} 个）。\n"
                "待 ProcessService 接入真实命令后生效。"
            )

    def _on_theme_toggle(self):
        """主题切换（占位）。"""
        QMessageBox.information(self, "主题切换",
                                "深色主题开发中，敬请期待。")
