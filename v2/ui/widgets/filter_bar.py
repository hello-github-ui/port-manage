#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : filter_bar.py
# @Software: PyCharm
# @Description:
#   筛选栏控件：5 个下拉框 + 清除筛选按钮。
#   透明背景，无白色卡片框。
# ======================================================================

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton, QWidget

from v2.config import settings
from v2.ui import style


class FilterBar(QWidget):
    """
    筛选栏。

    信号：
      - filter_changed(dict): 任一筛选条件变化时发出
    """

    filter_changed = pyqtSignal(dict)

    _PORT_TYPE_MAP = {
        "全部": "", "前端": "FRONTEND", "后端": "BACKEND",
        "数据库": "DATABASE", "其它": "OTHER",
    }
    _PROCESS_TYPE_MAP = {
        "全部": "", "Java": "JAVA", "Node.js": "NODE", "Python": "PYTHON",
        "Web服务器": "WEB_SERVER", "数据库": "DATABASE", "IDE": "IDE",
        "浏览器": "BROWSER", "系统": "SYSTEM", "其它": "OTHER",
    }
    _PROTOCOL_MAP = {"全部": "", "TCP": "TCP", "UDP": "UDP"}
    _DEV_PROCESS_MAP = {"全部": None, "是": True, "否": False}

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self.setStyleSheet(style.CARD_STYLE())

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 8, 5, 8)
        layout.setSpacing(12)

        # 端口类型
        layout.addWidget(self._make_label("端口类型："))
        self.port_type_box = self._make_combo(list(self._PORT_TYPE_MAP.keys()))
        self.port_type_box.currentTextChanged.connect(self._on_filter_changed)
        layout.addWidget(self.port_type_box)

        # 进程类型
        layout.addWidget(self._make_label("进程类型："))
        self.process_type_box = self._make_combo(list(self._PROCESS_TYPE_MAP.keys()))
        self.process_type_box.currentTextChanged.connect(self._on_filter_changed)
        layout.addWidget(self.process_type_box)

        # 协议
        layout.addWidget(self._make_label("协议："))
        self.protocol_box = self._make_combo(list(self._PROTOCOL_MAP.keys()))
        self.protocol_box.currentTextChanged.connect(self._on_filter_changed)
        layout.addWidget(self.protocol_box)

        # 开发进程
        layout.addWidget(self._make_label("开发进程："))
        self.dev_process_box = self._make_combo(list(self._DEV_PROCESS_MAP.keys()))
        self.dev_process_box.currentTextChanged.connect(self._on_filter_changed)
        layout.addWidget(self.dev_process_box)

        # 常用端口
        layout.addWidget(self._make_label("常用端口："))
        self.common_port_box = QComboBox()
        self.common_port_box.setStyleSheet(style.COMBO_BOX_STYLE())
        self.common_port_box.addItem("选择端口")
        for p in settings.COMMON_PORTS:
            service = settings.DATABASE_PORTS.get(p)
            label = f"{p} - {service}" if service else str(p)
            self.common_port_box.addItem(label, p)
        self.common_port_box.currentIndexChanged.connect(self._on_common_port_changed)
        layout.addWidget(self.common_port_box)

        # 弹簧，把清除按钮推到右侧
        layout.addStretch()

        # 清除筛选按钮
        self.clear_btn = QPushButton("🧹 清除筛选")
        self.clear_btn.setMinimumWidth(100)
        self.clear_btn.setStyleSheet(style.BTN_WARNING_STYLE())
        self.clear_btn.clicked.connect(self.clear_all)
        layout.addWidget(self.clear_btn)

    @staticmethod
    def _make_label(text: str) -> QLabel:
        label = QLabel(text)
        label.setStyleSheet(style.FILTER_LABEL_STYLE())
        return label

    @staticmethod
    def _make_combo(items) -> QComboBox:
        box = QComboBox()
        box.setStyleSheet(style.COMBO_BOX_STYLE())
        box.addItems(items)
        return box

    def apply_theme(self):
        """主题切换时重新应用样式。"""
        self.setStyleSheet(style.CARD_STYLE())
        for child in self.findChildren(QLabel):
            child.setStyleSheet(style.FILTER_LABEL_STYLE())
        for child in self.findChildren(QComboBox):
            child.setStyleSheet(style.COMBO_BOX_STYLE())
        self.clear_btn.setStyleSheet(style.BTN_WARNING_STYLE())

    def _current_filters(self) -> dict:
        return {
            "port_type": self._PORT_TYPE_MAP[self.port_type_box.currentText()],
            "process_type": self._PROCESS_TYPE_MAP[self.process_type_box.currentText()],
            "protocol": self._PROTOCOL_MAP[self.protocol_box.currentText()],
            "dev_process": self._DEV_PROCESS_MAP[self.dev_process_box.currentText()],
            "common_port": self.common_port_box.currentData(),
        }

    def _on_filter_changed(self):
        self.filter_changed.emit(self._current_filters())

    def _on_common_port_changed(self):
        if self.common_port_box.currentIndex() == 0:
            self._on_filter_changed()
            return

        for box in (self.port_type_box, self.process_type_box,
                    self.protocol_box, self.dev_process_box):
            box.blockSignals(True)
            box.setCurrentIndex(0)
            box.blockSignals(False)

        self.filter_changed.emit(self._current_filters())

    def clear_all(self):
        for box in (self.port_type_box, self.process_type_box,
                    self.protocol_box, self.dev_process_box,
                    self.common_port_box):
            box.blockSignals(True)
            box.setCurrentIndex(0)
            box.blockSignals(False)
        self.filter_changed.emit(self._current_filters())
