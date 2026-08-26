#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : search_bar.py
# @Software: PyCharm
# @Description:
#   搜索栏控件：搜索框 + 搜索按钮 + 刷新按钮 + 暂停/继续自动刷新 + 批量关闭。
#   透明背景，无白色卡片框。
# ======================================================================

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QWidget

from v2.ui import style


class SearchBar(QWidget):
    """
    搜索栏。

    信号：
      - search_requested(str):     搜索关键字
      - refresh_requested():       手动刷新
      - auto_refresh_toggled(bool):自动刷新开关
      - batch_kill_requested():    批量关闭
    """

    search_requested = pyqtSignal(str)
    refresh_requested = pyqtSignal()
    auto_refresh_toggled = pyqtSignal(bool)
    batch_kill_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._auto_refresh_active = True
        self._init_ui()

    def _init_ui(self):
        self.setStyleSheet(style.CARD_STYLE())

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 8, 5, 8)
        layout.setSpacing(12)

        # 搜索输入框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 搜索端口号 / 进程名 / PID...")
        self.search_input.setMinimumWidth(240)
        self.search_input.setStyleSheet(style.LINE_EDIT_STYLE())
        self.search_input.returnPressed.connect(self._on_search_clicked)
        layout.addWidget(self.search_input)

        # 搜索按钮
        self.search_btn = QPushButton("搜索")
        self.search_btn.setMinimumWidth(85)
        self.search_btn.setStyleSheet(style.BTN_DEFAULT_STYLE())
        self.search_btn.clicked.connect(self._on_search_clicked)
        layout.addWidget(self.search_btn)

        # 刷新按钮
        self.refresh_btn = QPushButton("🔄 刷新")
        self.refresh_btn.setMinimumWidth(95)
        self.refresh_btn.setStyleSheet(style.BTN_PRIMARY_STYLE())
        self.refresh_btn.clicked.connect(self.refresh_requested.emit)
        layout.addWidget(self.refresh_btn)

        # 暂停/继续自动刷新按钮
        self.auto_refresh_btn = QPushButton("⏸ 暂停自动刷新")
        self.auto_refresh_btn.setMinimumWidth(145)
        self.auto_refresh_btn.setStyleSheet(style.BTN_DEFAULT_STYLE())
        self.auto_refresh_btn.clicked.connect(self._on_auto_refresh_toggled)
        layout.addWidget(self.auto_refresh_btn)

        # 弹簧，把批量关闭按钮推到右侧
        layout.addStretch()

        # 批量关闭按钮
        self.batch_kill_btn = QPushButton("🗑 关闭选中 (0)")
        self.batch_kill_btn.setStyleSheet(style.BTN_BATCH_KILL_STYLE())
        self.batch_kill_btn.hide()
        self.batch_kill_btn.clicked.connect(self.batch_kill_requested.emit)
        layout.addWidget(self.batch_kill_btn)

    def _on_search_clicked(self):
        self.search_requested.emit(self.search_input.text().strip())

    def _on_auto_refresh_toggled(self):
        self._auto_refresh_active = not self._auto_refresh_active
        if self._auto_refresh_active:
            self.auto_refresh_btn.setText("⏸ 暂停自动刷新")
        else:
            self.auto_refresh_btn.setText("▶️ 继续自动刷新")
        self.auto_refresh_toggled.emit(self._auto_refresh_active)

    def apply_theme(self):
        """主题切换时重新应用样式。"""
        self.setStyleSheet(style.CARD_STYLE())
        self.search_input.setStyleSheet(style.LINE_EDIT_STYLE())
        self.search_btn.setStyleSheet(style.BTN_DEFAULT_STYLE())
        self.refresh_btn.setStyleSheet(style.BTN_PRIMARY_STYLE())
        self.auto_refresh_btn.setStyleSheet(style.BTN_DEFAULT_STYLE())
        self.batch_kill_btn.setStyleSheet(style.BTN_BATCH_KILL_STYLE())

    def set_batch_count(self, count: int):
        if count > 0:
            self.batch_kill_btn.setText(f"🗑 关闭选中 ({count})")
            self.batch_kill_btn.show()
        else:
            self.batch_kill_btn.hide()

    def clear_search(self):
        self.search_input.clear()
