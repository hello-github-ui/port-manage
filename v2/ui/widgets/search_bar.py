#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : search_bar.py
# @Software: PyCharm
# @Description:
#   搜索栏控件：搜索框 + 搜索按钮 + 刷新按钮 + 暂停/继续自动刷新 + 批量关闭。
#   对应 Java 前端 Toolbar 区块。
#   通过信号把交互事件抛给主窗口，自身只管界面表现。
# ======================================================================

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QWidget

from v2.ui import style


class SearchBar(QWidget):
    """
    搜索栏。

    信号：
      - search_requested(str):     搜索关键字（回车或点击搜索按钮）
      - refresh_requested():       手动刷新
      - auto_refresh_toggled(bool):自动刷新开关（True=开启/继续）
      - batch_kill_requested():    批量关闭
    """

    search_requested = pyqtSignal(str)
    refresh_requested = pyqtSignal()
    auto_refresh_toggled = pyqtSignal(bool)
    batch_kill_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._auto_refresh_active = True  # 自动刷新初始为开启
        self._init_ui()

    def _init_ui(self):
        self.setStyleSheet(style.CARD_STYLE)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 12, 20, 12)
        layout.setSpacing(12)

        # 搜索输入框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索端口号 / 进程名 / PID...")
        self.search_input.setMinimumWidth(220)
        self.search_input.setStyleSheet(style.LINE_EDIT_STYLE)
        # 回车即触发搜索
        self.search_input.returnPressed.connect(self._on_search_clicked)
        layout.addWidget(self.search_input)

        # 搜索按钮（灰色）
        self.search_btn = QPushButton("搜索")
        self.search_btn.setMinimumWidth(85)
        self.search_btn.setStyleSheet(style.BTN_DEFAULT_STYLE)
        self.search_btn.clicked.connect(self._on_search_clicked)
        layout.addWidget(self.search_btn)

        # 刷新按钮（蓝色）
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.setMinimumWidth(85)
        self.refresh_btn.setStyleSheet(style.BTN_PRIMARY_STYLE)
        self.refresh_btn.clicked.connect(self.refresh_requested.emit)
        layout.addWidget(self.refresh_btn)

        # 暂停/继续自动刷新按钮
        # 使用基本 Unicode 符号而非 emoji（避免 Windows 字体渲染缺失）
        self.auto_refresh_btn = QPushButton("⏸ 暂停自动刷新")
        self.auto_refresh_btn.setMinimumWidth(140)
        self.auto_refresh_btn.setStyleSheet(style.BTN_DEFAULT_STYLE)
        self.auto_refresh_btn.clicked.connect(self._on_auto_refresh_toggled)
        layout.addWidget(self.auto_refresh_btn)

        # 批量关闭按钮（默认隐藏，选中行后由主窗口控制显示）
        self.batch_kill_btn = QPushButton("关闭选中 (0)")
        self.batch_kill_btn.setStyleSheet(style.BTN_BATCH_KILL_STYLE)
        self.batch_kill_btn.hide()
        self.batch_kill_btn.clicked.connect(self.batch_kill_requested.emit)
        layout.addWidget(self.batch_kill_btn)

    # ------------------------------------------------------------------
    # 内部槽
    # ------------------------------------------------------------------

    def _on_search_clicked(self):
        """点击搜索 / 回车：发出搜索关键字。"""
        self.search_requested.emit(self.search_input.text().strip())

    def _on_auto_refresh_toggled(self):
        """切换自动刷新开关，并更新按钮文案。"""
        self._auto_refresh_active = not self._auto_refresh_active
        if self._auto_refresh_active:
            self.auto_refresh_btn.setText("⏸ 暂停自动刷新")
        else:
            self.auto_refresh_btn.setText("▶ 继续自动刷新")
        self.auto_refresh_toggled.emit(self._auto_refresh_active)

    # ------------------------------------------------------------------
    # 对外接口
    # ------------------------------------------------------------------

    def set_batch_count(self, count: int):
        """根据选中数量显示/隐藏批量关闭按钮，并更新文案。"""
        if count > 0:
            self.batch_kill_btn.setText(f"关闭选中 ({count})")
            self.batch_kill_btn.show()
        else:
            self.batch_kill_btn.hide()

    def clear_search(self):
        """清空搜索框（供「清除筛选」调用）。"""
        self.search_input.clear()
