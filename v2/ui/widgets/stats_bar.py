#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : stats_bar.py
# @Software: PyCharm
# @Description:
#   统计栏控件：总端口数 / 开发进程 / TCP / UDP / 上次扫描时间。
#   使用分隔符美化，透明背景，无白色卡片框。
# ======================================================================

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget

from v2.ui import style


class StatsBar(QWidget):
    """统计栏。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self.setStyleSheet(style.CARD_STYLE())

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 8, 5, 8)
        layout.setSpacing(8)

        s = style.STATS_LABEL_STYLE()

        self.total_label = QLabel("📊 总端口数：0")
        self.total_label.setStyleSheet(s)
        layout.addWidget(self.total_label)

        self._add_separator(layout)

        self.dev_label = QLabel("💻 开发进程：0")
        self.dev_label.setStyleSheet(s)
        layout.addWidget(self.dev_label)

        self._add_separator(layout)

        self.tcp_label = QLabel("🔗 TCP：0")
        self.tcp_label.setStyleSheet(s)
        layout.addWidget(self.tcp_label)

        self._add_separator(layout)

        self.udp_label = QLabel("📡 UDP：0")
        self.udp_label.setStyleSheet(s)
        layout.addWidget(self.udp_label)

        layout.addStretch()

        self.scan_time_label = QLabel("⏱ 上次扫描：--:--:--")
        self.scan_time_label.setStyleSheet(s)
        layout.addWidget(self.scan_time_label)

    @staticmethod
    def _add_separator(layout):
        """添加一个竖线分隔符。"""
        sep = QLabel("|")
        sep.setStyleSheet("color: #c0c6cf; font-size: 9pt;")
        layout.addWidget(sep)

    def apply_theme(self):
        """主题切换时重新应用样式。"""
        self.setStyleSheet(style.CARD_STYLE())
        s = style.STATS_LABEL_STYLE()
        self.total_label.setStyleSheet(s)
        self.dev_label.setStyleSheet(s)
        self.tcp_label.setStyleSheet(s)
        self.udp_label.setStyleSheet(s)
        self.scan_time_label.setStyleSheet(s)
        # 分隔符颜色跟随主题
        c = style.get_colors()
        for child in self.findChildren(QLabel):
            if child.text() == "|":
                child.setStyleSheet(f"color: {c.border}; font-size: 9pt;")

    def update_stats(self, stats: dict, last_scan_time: str):
        self.total_label.setText(f"📊 总端口数：{stats.get('total', 0)}")
        self.dev_label.setText(f"💻 开发进程：{stats.get('development_processes', 0)}")
        self.tcp_label.setText(f"🔗 TCP：{stats.get('tcp', 0)}")
        self.udp_label.setText(f"📡 UDP：{stats.get('udp', 0)}")
        self.scan_time_label.setText(f"⏱ 上次扫描：{last_scan_time or '--:--:--'}")
