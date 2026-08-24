#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : filter_bar.py
# @Software: PyCharm
# @Description:
#   筛选栏控件：5 个下拉框 + 清除筛选按钮。
#   对应 Java 前端 Filter Bar 区块。
#   下拉框显示中文，向外发出枚举值，便于主窗口直接与 PortInfo 字段比较。
# ======================================================================

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton, QWidget

from v2.config import settings
from v2.ui import style


class FilterBar(QWidget):
    """
    筛选栏。

    信号：
      - filter_changed(dict): 任一筛选条件变化时发出，dict 结构：
            {
              "port_type":   str,   # "" 表示全部
              "process_type":str,   # "" 表示全部
              "protocol":    str,   # "" 表示全部
              "dev_process": bool|None,  # None 表示全部
              "common_port": int|None,   # None 表示未选常用端口
            }
        当选择常用端口时，会自动清空其他筛选（独占筛选）。
    """

    filter_changed = pyqtSignal(dict)

    # 下拉框中文 -> 枚举值映射
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
        self.setStyleSheet(style.CARD_STYLE)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 12, 20, 12)
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

        # 常用端口：第一项为占位「选择端口」，其余从配置生成
        layout.addWidget(self._make_label("常用端口："))
        self.common_port_box = QComboBox()
        self.common_port_box.setStyleSheet(style.COMBO_BOX_STYLE)
        self.common_port_box.addItem("选择端口")
        # 遍历配置的常用端口，附上可读服务名（DATABASE_PORTS 提供服务名）
        for p in settings.COMMON_PORTS:
            service = settings.DATABASE_PORTS.get(p)
            label = f"{p} - {service}" if service else str(p)
            self.common_port_box.addItem(label, p)  # userData 存放端口号
        self.common_port_box.currentIndexChanged.connect(self._on_common_port_changed)
        layout.addWidget(self.common_port_box)

        # 清除筛选按钮（橙色）
        self.clear_btn = QPushButton("清除筛选")
        self.clear_btn.setMinimumWidth(90)
        self.clear_btn.setStyleSheet(style.BTN_WARNING_STYLE)
        self.clear_btn.clicked.connect(self.clear_all)
        layout.addWidget(self.clear_btn)

    # ------------------------------------------------------------------
    # 工具方法
    # ------------------------------------------------------------------

    @staticmethod
    def _make_label(text: str) -> QLabel:
        label = QLabel(text)
        label.setStyleSheet("color: #666; font-size: 14px;")
        return label

    @staticmethod
    def _make_combo(items) -> QComboBox:
        box = QComboBox()
        box.setStyleSheet(style.COMBO_BOX_STYLE)
        box.addItems(items)
        return box

    # ------------------------------------------------------------------
    # 内部槽
    # ------------------------------------------------------------------

    def _current_filters(self) -> dict:
        """收集当前所有筛选条件为 dict（枚举值形式）。"""
        return {
            "port_type": self._PORT_TYPE_MAP[self.port_type_box.currentText()],
            "process_type": self._PROCESS_TYPE_MAP[self.process_type_box.currentText()],
            "protocol": self._PROTOCOL_MAP[self.protocol_box.currentText()],
            "dev_process": self._DEV_PROCESS_MAP[self.dev_process_box.currentText()],
            "common_port": self.common_port_box.currentData(),  # None 或 int
        }

    def _on_filter_changed(self):
        """普通筛选变化：发出当前筛选条件。"""
        self.filter_changed.emit(self._current_filters())

    def _on_common_port_changed(self):
        """
        常用端口变化：若选了具体端口，则清空其他筛选（独占筛选），
        与 Java 前端 handleCommonPortSelect 行为一致。
        """
        if self.common_port_box.currentIndex() == 0:
            # 选回「选择端口」只当作取消常用端口筛选
            self._on_filter_changed()
            return

        # 临时断开信号，避免重置下拉框时反复触发
        for box in (self.port_type_box, self.process_type_box,
                    self.protocol_box, self.dev_process_box):
            box.blockSignals(True)
            box.setCurrentIndex(0)
            box.blockSignals(False)

        self.filter_changed.emit(self._current_filters())

    # ------------------------------------------------------------------
    # 对外接口
    # ------------------------------------------------------------------

    def clear_all(self):
        """清除全部筛选，重置所有下拉框到首项。"""
        for box in (self.port_type_box, self.process_type_box,
                    self.protocol_box, self.dev_process_box,
                    self.common_port_box):
            box.blockSignals(True)
            box.setCurrentIndex(0)
            box.blockSignals(False)
        self.filter_changed.emit(self._current_filters())
