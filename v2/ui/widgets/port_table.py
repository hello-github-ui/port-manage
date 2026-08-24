#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : port_table.py
# @Software: PyCharm
# @Description:
#   端口表格控件：QTableView + PortTableModel。
#   对应 Java 前端 Table 区块。
#   功能：
#     - 表头第 0 列显示全选复选框（QCheckBox 注入表头）
#     - 每行操作列注入「关闭」按钮（setIndexWidget）
#     - 勾选数量变化时发出 selection_changed，供主窗口更新批量按钮
#     - 关闭按钮点击发出 kill_requested(PortInfo)
#
#   修复要点：
#     - 表头第 0 列通过 setIndexWidget 注入 QCheckBox 作为全选控件
#     - 用 QCheckBox 三态（checked/unchecked/partially-checked）反映整体勾选状态
#     - 不用 model.dataChanged 跟踪勾选，改用自定义视图的 mousePressEvent
# ======================================================================

from PyQt5.QtCore import (pyqtSignal, QEvent, QItemSelectionModel,
                          QModelIndex, Qt)
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import (QAbstractItemView, QCheckBox, QHeaderView,
                             QHBoxLayout, QPushButton, QTableView, QWidget)

from v2.model.port_info import PortInfo
from v2.model.table_model import PortTableModel
from v2.ui import style


class _PortTableView(QTableView):
    """
    自定义 QTableView 子类。

    重写 mousePressEvent 来检测复选框列的点击，避免依赖 model.dataChanged
    （模型 reset 时 dataChanged 会被误触发，导致行消失等异常）。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._on_checkbox_toggled = None

    def mousePressEvent(self, event: QMouseEvent):
        """
        鼠标按下事件。检测是否点击在复选框列（COL_CHECK=0）上，
        若是则在父类处理后：
          1. 通知外部更新选中数
          2. 选中该行，使其出现选中高亮效果
        """
        index = self.indexAt(event.pos())
        if index.isValid() and index.column() == PortTableModel.COL_CHECK:
            # 先让父类正常处理（切换勾选状态）
            super().mousePressEvent(event)
            # 关键：选中该行，触发整行高亮视觉效果
            # ClearAndSelect 确保只有这一行被选中
            self.selectionModel().select(
                index,
                QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows
            )
            # 通知外部更新选中数
            if self._on_checkbox_toggled:
                self._on_checkbox_toggled()
        else:
            super().mousePressEvent(event)


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
        self._init_ui()

    def _init_ui(self):
        """构建表格视图与基础配置。"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 数据模型
        self.model = PortTableModel()

        # 自定义表格视图
        self.view = _PortTableView()
        self.view.setModel(self.model)

        # 选中行为
        self.view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.view.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 显式设置选中背景色
        from PyQt5.QtGui import QColor, QPalette
        palette = self.view.palette()
        palette.setColor(QPalette.Highlight, QColor("#BBDEFB"))
        palette.setColor(QPalette.HighlightedText, QColor("#1565C0"))
        self.view.setPalette(palette)

        # 启用交替行颜色
        self.view.setAlternatingRowColors(True)

        # 表头配置
        header = self.view.horizontalHeader()
        header.setStretchLastSection(False)
        self.view.verticalHeader().setVisible(False)
        self.view.verticalHeader().setDefaultSectionSize(38)

        # ---- 先设置列宽，确保第0列宽度足够 ----
        self._adjust_columns()

        # ---- 再注入表头全选复选框 ----
        self._header_checkbox = QCheckBox()
        self._header_checkbox.setToolTip("全选 / 全不选")
        # 设置复选框最小尺寸，确保可见
        self._header_checkbox.setMinimumSize(18, 18)
        self._header_checkbox.setMaximumSize(18, 18)
        self._header_checkbox.setStyleSheet(
            "QCheckBox { spacing: 0px; margin: 0px; padding: 0px; }"
            "QCheckBox::indicator { width: 16px; height: 16px; }"
        )
        self._header_checkbox.setTristate(True)

        # 关键点：使用 header 的 viewport 作为父控件，并正确定位
        # QHeaderView.setIndexWidget 需要 QModelIndex
        header.setIndexWidget(
            self.model.index(0, PortTableModel.COL_CHECK),
            self._header_checkbox)

        # 复选框状态变化
        self._header_checkbox.stateChanged.connect(
            self._on_header_checkbox_state_changed)

        # 把复选框变更回调绑定到视图
        self.view._on_checkbox_toggled = self._on_checkbox_toggled

        layout.addWidget(self.view)

        # 延迟一帧再定位复选框，确保表头布局完成
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(0, self._reposition_header_checkbox)

    # ------------------------------------------------------------------
    # 内部槽
    # ------------------------------------------------------------------

    def _on_header_checkbox_state_changed(self, state: int):
        """
        表头复选框状态变化（用户点击表头复选框）。
        三态逻辑：
          - Checked(2)    -> 全选
          - Unchecked(0)  -> 全不选
          - PartiallyChecked(1) -> 由 set_ports / _on_checkbox_toggled 自动同步
        """
        # 仅在 Checked / Unchecked 时主动设置全选状态；
        # PartiallyChecked 由数据变更时同步，不再反向触发
        if state == Qt.Checked:
            self.model.set_all_checked(True)
        elif state == Qt.Unchecked:
            self.model.set_all_checked(False)
        # PartiallyChecked 不处理（避免循环触发）

        # 数据变更后重新注入按钮
        self._inject_close_buttons()
        self._emit_selection_changed()

    def _on_checkbox_toggled(self):
        """行复选框状态变化时，同步表头复选框状态并发出信号。"""
        self._sync_header_checkbox()
        self._emit_selection_changed()

    def _sync_header_checkbox(self):
        """
        根据当前行勾选情况，更新表头复选框的三态显示。
        """
        if self.model.rowCount() == 0:
            self._header_checkbox.setCheckState(Qt.Unchecked)
            return

        all_checked = self.model.is_all_checked()
        none_checked = self.model.is_none_checked()

        # 阻止 setCheckState 触发 stateChanged 导致循环
        self._header_checkbox.blockSignals(True)
        if all_checked:
            self._header_checkbox.setCheckState(Qt.Checked)
        elif none_checked:
            self._header_checkbox.setCheckState(Qt.Unchecked)
        else:
            self._header_checkbox.setCheckState(Qt.PartiallyChecked)
        self._header_checkbox.blockSignals(False)

    def _emit_selection_changed(self):
        """统计勾选数量并发出信号。"""
        count = len(self.model.get_checked_ports())
        self.selection_changed.emit(count)

    def _on_kill_clicked(self, row: int):
        """某行「关闭」按钮点击：取出对应 PortInfo 并发出信号。"""
        port_info = self.model.get_port(row)
        if port_info:
            self.kill_requested.emit(port_info)

    # ------------------------------------------------------------------
    # 私有方法
    # ------------------------------------------------------------------

    def _inject_close_buttons(self):
        """为每一行的「操作」列注入「关闭」按钮。"""
        for row in range(self.model.rowCount()):
            btn = QPushButton("关闭")
            btn.setStyleSheet(style.BTN_DANGER_STYLE)
            btn.clicked.connect(
                lambda _checked=False, r=row: self._on_kill_clicked(r))
            index = self.model.index(row, PortTableModel.COL_ACTION)
            self.view.setIndexWidget(index, btn)

    def _adjust_columns(self):
        """调整列宽。"""
        m = PortTableModel
        view = self.view
        view.setColumnWidth(m.COL_CHECK, 40)
        view.setColumnWidth(m.COL_PORT, 75)
        view.setColumnWidth(m.COL_PORT_TYPE, 95)
        view.setColumnWidth(m.COL_PROTOCOL, 70)
        view.setColumnWidth(m.COL_STATUS, 105)
        view.setColumnWidth(m.COL_PID, 80)
        view.setColumnWidth(m.COL_PROCESS_NAME, 160)
        view.setColumnWidth(m.COL_USER, 70)
        view.setColumnWidth(m.COL_DEV, 80)
        view.setColumnWidth(m.COL_ACTION, 75)
        view.horizontalHeader().setSectionResizeMode(
            m.COL_COMMAND, QHeaderView.Stretch)

    # ------------------------------------------------------------------
    # 对外接口
    # ------------------------------------------------------------------

    def set_ports(self, ports):
        """更新表格数据。"""
        self.model.set_ports(ports)
        self._inject_close_buttons()
        self._adjust_columns()
        # 数据重置后重新定位表头复选框
        self._reposition_header_checkbox()
        # 同步表头复选框状态
        self._sync_header_checkbox()
        self._emit_selection_changed()

    def get_checked_ports(self):
        """返回当前勾选的 PortInfo 列表。"""
        return self.model.get_checked_ports()

    def resizeEvent(self, event):
        """窗口尺寸变化时，重新定位表头复选框。"""
        super().resizeEvent(event)
        self._reposition_header_checkbox()

    def _reposition_header_checkbox(self):
        """将表头复选框定位到第0列中心位置。"""
        if not hasattr(self, '_header_checkbox') or not self._header_checkbox:
            return
        m = PortTableModel
        col_x = self.view.columnViewportPosition(m.COL_CHECK)
        col_w = self.view.columnWidth(m.COL_CHECK)
        header_h = self.view.horizontalHeader().height()
        checkbox_size = 18
        x = col_x + (col_w - checkbox_size) // 2
        y = (header_h - checkbox_size) // 2
        self._header_checkbox.setGeometry(x, y, checkbox_size, checkbox_size)
