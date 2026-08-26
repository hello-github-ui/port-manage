#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : status_bar.py
# @Software: PyCharm
# @Description:
#   底部状态栏控件：状态消息 + 自动刷新状态。
#   透明背景，无白色卡片框。
# ======================================================================

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget

from v2.ui import style


class StatusBar(QWidget):
    """底部状态栏。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self.setStyleSheet(style.CARD_STYLE())

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 8, 5, 8)
        layout.setSpacing(15)

        # 左侧：状态消息
        self.status_label = QLabel("✅ 就绪")
        self.status_label.setStyleSheet(style.STATUS_SUCCESS_STYLE())
        layout.addWidget(self.status_label)

        layout.addStretch()

        # 右侧：自动刷新状态
        self.auto_refresh_label = QLabel("🔄 自动刷新：开启 (5 秒)")
        self.auto_refresh_label.setStyleSheet(style.STATUS_INFO_STYLE())
        layout.addWidget(self.auto_refresh_label)

    def apply_theme(self):
        """主题切换时重新应用样式。"""
        self.setStyleSheet(style.CARD_STYLE())
        # 保持成功/错误状态，重新应用信息标签样式
        current_text = self.status_label.text()
        is_success = current_text.startswith("✅") or current_text == "就绪"
        self.status_label.setStyleSheet(
            style.STATUS_SUCCESS_STYLE() if is_success else 
            f"color: {style.get_colors().danger}; font-size: 9pt; font-weight: 600;"
        )
        self.auto_refresh_label.setStyleSheet(style.STATUS_INFO_STYLE())

    def set_status(self, message: str, success: bool = True):
        """更新左侧状态消息。"""
        prefix = "✅" if success else "❌"
        self.status_label.setText(f"{prefix} {message}")
        c = style.get_colors()
        self.status_label.setStyleSheet(
            style.STATUS_SUCCESS_STYLE() if success else
            f"color: {c.danger}; font-size: 9pt; font-weight: 600;"
        )

    def set_auto_refresh_info(self, text: str):
        """更新右侧自动刷新状态文本。"""
        if "暂停" in text:
            self.auto_refresh_label.setText(f"⏸ {text}")
        elif "开启" in text:
            self.auto_refresh_label.setText(f"🔄 {text}")
        else:
            self.auto_refresh_label.setText(text)

    def show_message(self, message: str):
        """显示状态消息，自动判断成功/错误。"""
        success = True
        if message.startswith("❌") or message.startswith("⏳"):
            # 已经带前缀，直接设置文本
            text = message
            success = not message.startswith("❌")
        else:
            if "失败" in message or "错误" in message or "❌" in message:
                success = False
            text = message
        self.set_status(text.lstrip("✅❌⏳ "), success=success)

    def set_auto_refresh(self, enabled: bool):
        """设置自动刷新状态。"""
        if enabled:
            self.auto_refresh_label.setText("🔄 自动刷新：开启 (5 秒)")
        else:
            self.auto_refresh_label.setText("⏸ 自动刷新：已暂停")
