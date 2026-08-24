#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : stats_bar.py
# @Software: PyCharm
# @Description:
#   统计栏控件：总端口数 / 开发进程 / TCP / UDP / 上次扫描时间。
#   对应 Java 前端 Stats Bar 区块。
#   纯展示型控件，由主窗口调用 update_stats 刷新数据。
# ======================================================================

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget

from v2.ui import style


class StatsBar(QWidget):
    """统计栏。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self.setStyleSheet(style.CARD_STYLE)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 12, 20, 12)
        layout.setSpacing(25)

        s = style.STATS_LABEL_STYLE

        self.total_label = QLabel("总端口数：0")
        self.total_label.setStyleSheet(s)
        layout.addWidget(self.total_label)

        self.dev_label = QLabel("开发进程：0")
        self.dev_label.setStyleSheet(s)
        layout.addWidget(self.dev_label)

        self.tcp_label = QLabel("TCP：0")
        self.tcp_label.setStyleSheet(s)
        layout.addWidget(self.tcp_label)

        self.udp_label = QLabel("UDP：0")
        self.udp_label.setStyleSheet(s)
        layout.addWidget(self.udp_label)

        # 弹簧把「上次扫描」推到右侧
        layout.addStretch()

        self.scan_time_label = QLabel("上次扫描：--:--:--")
        self.scan_time_label.setStyleSheet(s)
        layout.addWidget(self.scan_time_label)

    # ------------------------------------------------------------------
    # 对外接口
    # ------------------------------------------------------------------

    def update_stats(self, stats: dict, last_scan_time: str):
        """
        更新统计显示。

        :param stats: ScanService.get_statistics 返回的 dict
                      {total, development_processes, tcp, udp}
        :param last_scan_time: 上次扫描时间字符串
        """
        self.total_label.setText(f"总端口数：{stats.get('total', 0)}")
        self.dev_label.setText(f"开发进程：{stats.get('development_processes', 0)}")
        self.tcp_label.setText(f"TCP：{stats.get('tcp', 0)}")
        self.udp_label.setText(f"UDP：{stats.get('udp', 0)}")
        self.scan_time_label.setText(f"上次扫描：{last_scan_time or '--:--:--'}")
