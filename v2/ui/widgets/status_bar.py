#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : status_bar.py
# @Software: PyCharm
# @Description:
#   底部状态栏控件：状态消息 + 自动刷新状态。
#   对应 Java 前端 Footer 区块。
#   纯展示型控件，由主窗口调用方法更新内容。
# ======================================================================

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget

from v2.ui import style


class StatusBar(QWidget):
    """底部状态栏。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self.setStyleSheet(style.CARD_STYLE)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(15)

        # 左侧：状态消息（成功默认绿色）
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet(style.STATUS_SUCCESS_STYLE)
        layout.addWidget(self.status_label)

        # 弹簧把右侧信息推到最右
        layout.addStretch()

        # 右侧：自动刷新状态
        self.auto_refresh_label = QLabel("自动刷新：开启 (5 秒)")
        self.auto_refresh_label.setStyleSheet(style.STATUS_INFO_STYLE)
        layout.addWidget(self.auto_refresh_label)

    # ------------------------------------------------------------------
    # 对外接口
    # ------------------------------------------------------------------

    def set_status(self, message: str, success: bool = True):
        """更新左侧状态消息，success 控制颜色（绿/红）。"""
        self.status_label.setText(message)
        self.status_label.setStyleSheet(
            style.STATUS_SUCCESS_STYLE if success else
            "color: #F44336; font-size: 13px; font-weight: bold;"
        )

    def set_auto_refresh_info(self, text: str):
        """更新右侧自动刷新状态文本。"""
        self.auto_refresh_label.setText(text)
