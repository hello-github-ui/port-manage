#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : top_bar.py
# @Software: PyCharm
# @Description:
#   顶部标题栏控件：标题 + OS 信息 + 端口总数 + 主题选择下拉框。
# ======================================================================

import platform
import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QComboBox, QHBoxLayout, QLabel, QSizePolicy,
                             QSpacerItem, QWidget)

from v2.config import settings
from v2.ui import style


class TopBar(QWidget):
    """
    顶部标题栏。

    信号：
      - theme_changed(str): 主题切换时发出，参数为主题名称
    """

    theme_changed = pyqtSignal(str)

    # 可用主题列表
    THEMES = [
        ("浅色主题", "light"),
        ("深色主题", "dark"),
        ("蓝色主题", "blue"),
        ("绿色主题", "green"),
        ("紫色主题", "purple"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        """构建顶部栏布局。"""
        self.setStyleSheet(style.CARD_STYLE())

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 8, 5, 8)
        layout.setSpacing(20)

        # 左侧：应用标题 + 版本号
        self.title_label = QLabel(f"🔌 {settings.APP_TITLE}")
        self.title_label.setStyleSheet(style.TITLE_LABEL_STYLE())
        layout.addWidget(self.title_label)

        # 版本号标签（小号灰色字体）
        colors = style.get_colors()
        self.version_label = QLabel(settings.APP_VERSION)
        self.version_label.setStyleSheet(
            f"color: {colors.text_muted}; font-size: 11px; padding: 0 0 2px 0;"
        )
        layout.addWidget(self.version_label)

        # 中间：弹簧
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # 作者信息
        self.author_label = QLabel(f"👤 {settings.APP_AUTHOR}")
        self.author_label.setStyleSheet(style.INFO_LABEL_STYLE())
        layout.addWidget(self.author_label)

        # 右侧信息组：自动检测操作系统
        os_name = platform.system()
        if "Windows" in os_name:
            os_icon, os_display = "🪟", "Windows"
        elif "Darwin" in os_name:
            os_icon, os_display = "🍎", "macOS"
        else:
            os_icon, os_display = "🐧", "Linux"
        self.os_label = QLabel(f"{os_icon} {os_display}")
        self.os_label.setStyleSheet(style.INFO_LABEL_STYLE())
        layout.addWidget(self.os_label)

        self.port_count_label = QLabel("📊 0 个端口")
        self.port_count_label.setStyleSheet(style.INFO_LABEL_STYLE())
        layout.addWidget(self.port_count_label)

        # 主题选择标签
        theme_label = QLabel("🎨 主题：")
        theme_label.setStyleSheet(style.INFO_LABEL_STYLE())
        layout.addWidget(theme_label)

        # 主题选择下拉框
        self.theme_combo = QComboBox()
        self.theme_combo.setStyleSheet(style.COMBO_BOX_STYLE())
        for theme_name, theme_id in self.THEMES:
            self.theme_combo.addItem(theme_name, theme_id)
        self.theme_combo.setCurrentIndex(0)  # 默认浅色主题
        self.theme_combo.currentIndexChanged.connect(self._on_theme_changed)
        layout.addWidget(self.theme_combo)

    def _on_theme_changed(self, index):
        """主题下拉框选择变化。"""
        theme_id = self.theme_combo.itemData(index)
        self.theme_changed.emit(theme_id)

    def apply_theme(self):
        """主题切换时重新应用样式。"""
        colors = style.get_colors()
        self.setStyleSheet(style.CARD_STYLE())
        self.title_label.setStyleSheet(style.TITLE_LABEL_STYLE())
        self.version_label.setStyleSheet(
            f"color: {colors.text_muted}; font-size: 11px; padding: 0 0 2px 0;"
        )
        self.author_label.setStyleSheet(style.INFO_LABEL_STYLE())
        self.os_label.setStyleSheet(style.INFO_LABEL_STYLE())
        self.port_count_label.setStyleSheet(style.INFO_LABEL_STYLE())
        self.theme_combo.setStyleSheet(style.COMBO_BOX_STYLE())

    def set_current_theme(self, theme_id: str):
        """设置当前选中的主题（不触发信号）。"""
        for i, (_, tid) in enumerate(self.THEMES):
            if tid == theme_id:
                self.theme_combo.blockSignals(True)
                self.theme_combo.setCurrentIndex(i)
                self.theme_combo.blockSignals(False)
                break

    def update_info(self, os_type: str, port_count: int):
        """更新 OS 类型与端口总数显示。"""
        os_icon = "🪟" if "windows" in os_type.lower() else "🍎" if "darwin" in os_type.lower() else "🐧"
        self.os_label.setText(f"{os_icon} {os_type}")
        self.port_count_label.setText(f"📊 {port_count} 个端口")

    def set_port_count(self, count: int):
        """设置端口总数显示。"""
        self.port_count_label.setText(f"📊 {count} 个端口")
