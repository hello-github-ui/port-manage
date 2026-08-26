#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : port_table.py
# @Software: PyCharm
# @Description:
#   端口表格控件：使用 QTableWidget 实现。
#   - 表头第一列使用真实 QCheckBox 控件实现全选/全不选
#   - 每一行第一列也是真实 QCheckBox 控件，确保对齐准确
#   - 勾选复选框后整行高亮显示
#   - 最后一列是「关闭」按钮
# ======================================================================

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QAbstractItemView, QCheckBox, QHBoxLayout,
                             QHeaderView, QPushButton, QTableWidget,
                             QTableWidgetItem, QWidget)

from v2.model.port_info import PortInfo
from v2.ui import style


class _CheckBoxHeaderView(QHeaderView):
    """带全选复选框的自定义表头视图（两态模式）。"""

    select_all_clicked = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(Qt.Horizontal, parent)
        self._check_box = QCheckBox(self)
        self._check_box.setTristate(False)
        self._check_box.setStyleSheet(style.CHECKBOX_STYLE())
        self._check_box.stateChanged.connect(self._on_state_changed)
        self._is_updating = False

    def _on_state_changed(self, state: int):
        if self._is_updating:
            return
        self.select_all_clicked.emit(state == Qt.Checked)

    def set_checked(self, checked: bool):
        self._is_updating = True
        self._check_box.setChecked(checked)
        self._is_updating = False

    def apply_theme(self):
        self._check_box.setStyleSheet(style.CHECKBOX_STYLE())

    def showEvent(self, event):
        super().showEvent(event)
        self._update_checkbox_position()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_checkbox_position()

    def paintSection(self, painter, rect, logicalIndex):
        super().paintSection(painter, rect, logicalIndex)
        if logicalIndex == 0:
            self._update_checkbox_position()

    def _update_checkbox_position(self):
        section_width = self.sectionSize(0)
        header_height = self.height()
        checkbox_size = self._check_box.sizeHint()

        x = self.sectionViewportPosition(0) + (section_width - checkbox_size.width()) // 2
        y = (header_height - checkbox_size.height()) // 2

        self._check_box.move(x, y)
        self._check_box.raise_()


class _CenteredWidget(QWidget):
    """通用居中容器：将子控件居中显示在单元格内，透明背景。"""

    def __init__(self, child_widget, parent=None, margins=(4, 2, 4, 2)):
        super().__init__(parent)
        # 设置透明背景，避免在深色主题下出现白色块导致的阴影/错位感
        self.setStyleSheet("background: transparent;")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(*margins)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(child_widget)


class PortTable(QWidget):
    """
    端口表格。

    信号：
      - selection_changed(int):   勾选行数变化
      - kill_requested(PortInfo): 某行「关闭」按钮被点击
    """

    selection_changed = pyqtSignal(int)
    kill_requested = pyqtSignal(PortInfo)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ports = []
        self._row_checkboxes = []
        self._kill_buttons = []
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(11)

        headers = [
            "", "端口", "类型", "协议", "状态", "PID",
            "进程名", "命令行", "用户", "开发进程", "操作",
        ]
        self.table.setHorizontalHeaderLabels(headers)

        self._header = _CheckBoxHeaderView()
        self.table.setHorizontalHeader(self._header)
        self._header.select_all_clicked.connect(self._on_select_all_clicked)

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table.setStyleSheet(style.TABLE_STYLE())
        self.table.setAlternatingRowColors(True)

        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(40)

        self._adjust_columns()

        layout.addWidget(self.table)

    def _adjust_columns(self):
        self.table.setColumnWidth(0, 48)
        self.table.setColumnWidth(1, 75)
        self.table.setColumnWidth(2, 95)
        self.table.setColumnWidth(3, 70)
        self.table.setColumnWidth(4, 105)
        self.table.setColumnWidth(5, 80)
        self.table.setColumnWidth(6, 160)
        self.table.setColumnWidth(7, 200)
        self.table.setColumnWidth(8, 70)
        self.table.setColumnWidth(9, 80)
        self.table.setColumnWidth(10, 80)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)

    def apply_theme(self):
        """主题切换时重新应用所有样式。"""
        self.table.setStyleSheet(style.TABLE_STYLE())
        self._header.apply_theme()
        for cb in self._row_checkboxes:
            cb.setStyleSheet(style.CHECKBOX_STYLE())
        for btn in self._kill_buttons:
            btn.setStyleSheet(style.BTN_DANGER_STYLE())

    # ------------------------------------------------------------------
    # 全选逻辑
    # ------------------------------------------------------------------

    def _on_select_all_clicked(self, checked: bool):
        self._set_all_rows_checked(checked)
        self._emit_selection_changed()

    def _set_all_rows_checked(self, checked: bool):
        for cb in self._row_checkboxes:
            cb.blockSignals(True)
            cb.setChecked(checked)
            cb.blockSignals(False)

    def _update_header_state(self):
        total = len(self._row_checkboxes)
        if total == 0:
            self._header.set_checked(False)
            return
        all_checked = all(cb.isChecked() for cb in self._row_checkboxes)
        self._header.set_checked(all_checked)

    # ------------------------------------------------------------------
    # 行复选框/关闭按钮处理
    # ------------------------------------------------------------------

    def _on_row_checkbox_clicked(self, row: int):
        checkbox = self._row_checkboxes[row]
        if checkbox.isChecked():
            self.table.selectRow(row)
        else:
            selected = self.table.selectedItems()
            if selected and self.table.row(selected[0]) == row:
                self.table.clearSelection()
        self._update_header_state()
        self._emit_selection_changed()

    def _on_kill_clicked(self, row: int):
        if 0 <= row < len(self._ports):
            self.kill_requested.emit(self._ports[row])

    def _emit_selection_changed(self):
        self.selection_changed.emit(len(self.get_checked_ports()))

    # ------------------------------------------------------------------
    # 对外接口
    # ------------------------------------------------------------------

    def set_ports(self, ports):
        self._ports = list(ports)
        self._row_checkboxes = []
        self._kill_buttons = []

        self.table.setRowCount(0)
        self.table.setRowCount(len(self._ports))

        for row, port in enumerate(self._ports):
            # 第0列：复选框
            cb = QCheckBox()
            cb.setStyleSheet(style.CHECKBOX_STYLE())
            cb_container = _CenteredWidget(cb, margins=(0, 0, 0, 0))
            self.table.setCellWidget(row, 0, cb_container)
            self._row_checkboxes.append(cb)
            cb.clicked.connect(
                lambda _c, r=row: self._on_row_checkbox_clicked(r)
            )

            def _set_item(col, text, center=False):
                item = QTableWidgetItem(str(text) if text is not None else "-")
                if center:
                    item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)

            _set_item(1, port.port, center=True)
            _set_item(2, port.port_type, center=True)
            _set_item(3, port.protocol, center=True)
            _set_item(4, port.status, center=True)
            _set_item(5, port.pid, center=True)
            _set_item(6, port.process_name)

            cmd_item = QTableWidgetItem(port.command_line or "")
            cmd_item.setToolTip(port.command_line or "")
            self.table.setItem(row, 7, cmd_item)

            _set_item(8, port.user if port.user else "-", center=True)
            _set_item(9, "是" if port.is_development_process else "否", center=True)

            # 第10列：关闭按钮
            btn = QPushButton("关闭")
            btn.setStyleSheet(style.BTN_DANGER_STYLE())
            self._kill_buttons.append(btn)
            btn_container = _CenteredWidget(btn, margins=(4, 2, 4, 2))
            self.table.setCellWidget(row, 10, btn_container)
            btn.clicked.connect(
                lambda _c, r=row: self._on_kill_clicked(r)
            )

        self._update_header_state()
        self._emit_selection_changed()
        self._adjust_columns()

    def get_checked_ports(self):
        return [
            self._ports[i] for i, cb in enumerate(self._row_checkboxes)
            if cb.isChecked() and i < len(self._ports)
        ]
