#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : top_bar.py
# @Software: PyCharm
# @Description:
#   顶部标题栏控件：标题 + OS 信息 + 端口总数 + 头像 + 主题切换。
#   对应 Java 前端 Header 区块。
#   通过 pyqtSignal 对外暴露「主题切换」事件，自身不处理业务逻辑。
# ======================================================================

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                             QSpacerItem, QWidget)

from v2.ui import style


class TopBar(QWidget):
    """
    顶部标题栏。

    信号：
      - theme_toggled(): 主题切换按钮点击时发出
    """

    # 主题切换信号（占位，后续主窗口连接到主题切换逻辑）
    theme_toggled = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        """构建顶部栏布局。"""
        self.setStyleSheet(style.CARD_STYLE)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(25, 15, 25, 15)
        layout.setSpacing(20)

        # 左侧：应用标题
        self.title_label = QLabel("Port Manager")
        self.title_label.setStyleSheet(style.TITLE_LABEL_STYLE)
        layout.addWidget(self.title_label)

        # 中间：弹簧，把右侧信息推到最右
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # 右侧信息组
        self.os_label = QLabel("Windows")
        self.os_label.setStyleSheet(style.INFO_LABEL_STYLE)
        layout.addWidget(self.os_label)

        self.port_count_label = QLabel("0 ports")
        self.port_count_label.setStyleSheet(style.INFO_LABEL_STYLE)
        layout.addWidget(self.port_count_label)

        # 主题切换按钮（占位）
        self.theme_btn = QPushButton("🌓")
        self.theme_btn.setFixedSize(34, 30)
        self.theme_btn.setStyleSheet(style.BTN_DEFAULT_STYLE)
        self.theme_btn.setToolTip("切换浅色/深色主题")
        self.theme_btn.clicked.connect(self.theme_toggled.emit)
        layout.addWidget(self.theme_btn)

        # 头像圆形徽标
        self.avatar_label = QLabel("U")
        self.avatar_label.setFixedSize(30, 30)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.setStyleSheet(style.AVATAR_LABEL_STYLE)
        layout.addWidget(self.avatar_label)

    # ------------------------------------------------------------------
    # 对外接口：供主窗口更新显示内容
    # ------------------------------------------------------------------

    def update_info(self, os_type: str, port_count: int):
        """更新 OS 类型与端口总数显示。"""
        self.os_label.setText(os_type)
        self.port_count_label.setText(f"{port_count} ports")
