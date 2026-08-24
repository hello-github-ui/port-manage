#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : table_model.py
# @Software: PyCharm
# @Description:
#   端口表格数据模型，继承 QAbstractTableModel。
#   采用标准的 MVC（Model-View-Controller）思路：本类只负责「数据如何呈现
#   给视图」，不关心视图长什么样；视图 QTableView 通过模型接口取数。
#   相比 QStandardItemModel 逐格 setItem，此处更高效、更可控。
# ======================================================================

from typing import List

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt

from v2.model.port_info import PortInfo


class PortTableModel(QAbstractTableModel):
    """
    端口列表表格模型。

    列定义（与 Java 前端表格 11 列对齐）：
        0  复选框（用于批量选择）
        1  端口
        2  类型（端口类型 FRONTEND/BACKEND/DATABASE/OTHER）
        3  协议（TCP/UDP）
        4  状态（LISTENING 等）
        5  PID
        6  进程名
        7  命令行
        8  用户
        9  开发进程（是/否）
        10 操作（占位文本「关闭」，实际按钮由视图层用 setIndexWidget 注入）
    """

    # 表头（按列索引顺序排列）
    HEADERS = [
        "", "端口", "类型", "协议", "状态", "PID",
        "进程名", "命令行", "用户", "开发进程", "操作",
    ]

    # 列索引常量，方便视图层引用，避免到处写魔法数字
    COL_CHECK = 0
    COL_PORT = 1
    COL_PORT_TYPE = 2
    COL_PROTOCOL = 3
    COL_STATUS = 4
    COL_PID = 5
    COL_PROCESS_NAME = 6
    COL_COMMAND = 7
    COL_USER = 8
    COL_DEV = 9
    COL_ACTION = 10

    def __init__(self, parent=None):
        super().__init__(parent)
        # 内部数据：PortInfo 列表。模型不持有缓存逻辑，缓存由 ScanService 负责。
        self._ports: List[PortInfo] = []
        # 记录每一行的勾选状态（按行号索引）。用 list 而非 Set 是为了
        # 在数据整体替换后能快速重置。
        self._checked_rows: List[bool] = []

    # ------------------------------------------------------------------
    # 必须重写的 QAbstractTableModel 接口
    # ------------------------------------------------------------------

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """返回行数（即端口条目数）。"""
        return len(self._ports)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """返回列数（固定 11 列）。"""
        return len(self.HEADERS)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        """
        视图取数入口。根据列与角色返回对应内容。

        :param index: 单元格索引
        :param role:  Qt 角色（显示文本 / 对齐 / 勾选状态 等）
        """
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        if row < 0 or row >= len(self._ports):
            return None

        port: PortInfo = self._ports[row]

        # ---- 复选框列：通过 CheckStateRole 控制勾选 ----
        if col == self.COL_CHECK:
            if role == Qt.CheckStateRole:
                # _checked_rows 与 _ports 等长，True 表示已勾选
                return Qt.Checked if self._checked_rows[row] else Qt.Unchecked
            return None  # 复选框列不显示文本

        # ---- 普通文本列：DisplayRole 返回展示文本 ----
        if role == Qt.DisplayRole:
            if col == self.COL_PORT:
                return str(port.port)
            if col == self.COL_PORT_TYPE:
                return port.port_type
            if col == self.COL_PROTOCOL:
                return port.protocol
            if col == self.COL_STATUS:
                return port.status
            if col == self.COL_PID:
                return str(port.pid)
            if col == self.COL_PROCESS_NAME:
                return port.process_name
            if col == self.COL_COMMAND:
                # 命令行可能很长，这里原样返回；视图层用 ToolTip 显示完整内容
                return port.command_line
            if col == self.COL_USER:
                return port.user if port.user else "-"
            if col == self.COL_DEV:
                return "是" if port.is_development_process else "否"
            if col == self.COL_ACTION:
                # 占位文本；真实「关闭」按钮由视图层通过 setIndexWidget 注入
                return "关闭"

        # ---- 工具提示：命令行列悬停显示完整命令行（避免被截断） ----
        if role == Qt.ToolTipRole:
            if col == self.COL_COMMAND and port.command_line:
                return port.command_line

        # ---- 文本对齐：端口/PID/协议/状态居中，便于阅读 ----
        if role == Qt.TextAlignmentRole:
            if col in (self.COL_PORT, self.COL_PID, self.COL_PROTOCOL,
                       self.COL_STATUS, self.COL_PORT_TYPE, self.COL_DEV):
                return Qt.AlignCenter

        return None

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = Qt.DisplayRole):
        """返回表头文本（仅水平表头）。"""
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.HEADERS[section]
        return None

    def flags(self, index: QModelIndex):
        """
        单元格标志。
        - 复选框列：可选中、可勾选（ItemIsUserCheckable）、可编辑
        - 其他列：只读、可选中
        - 操作列：后续放按钮，保持可选中即可
        """
        if not index.isValid():
            return Qt.NoItemFlags
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if index.column() == self.COL_CHECK:
            # 复选框列需要 ItemIsUserCheckable + ItemIsEditable，
            # 否则用户点击无法触发 setData
            flags |= Qt.ItemIsUserCheckable | Qt.ItemIsEditable
        return flags

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole) -> bool:
        """处理复选框勾选/取消，并通知视图刷新对应单元格。"""
        if not index.isValid():
            return False
        if index.column() == self.COL_CHECK and role == Qt.CheckStateRole:
            self._checked_rows[index.row()] = (value == Qt.Checked)
            # dataChanged 信号让视图重绘该单元格
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    # ------------------------------------------------------------------
    # 业务辅助方法（供视图 / 主窗口调用）
    # ------------------------------------------------------------------

    def set_ports(self, ports: List[PortInfo]):
        """
        整体替换数据源（每次扫描后调用）。
        使用 beginResetModel / endResetModel 通知视图彻底刷新，
        比逐行 insert/remove 更高效、更不容易出显示错位。
        """
        self.beginResetModel()
        self._ports = list(ports)
        # 重置勾选状态（保持与行数等长）
        self._checked_rows = [False] * len(self._ports)
        self.endResetModel()

    def get_port(self, row: int) -> PortInfo:
        """根据行号取 PortInfo，供「关闭」按钮等交互使用。"""
        if 0 <= row < len(self._ports):
            return self._ports[row]
        return None

    def get_checked_ports(self) -> List[PortInfo]:
        """返回当前所有勾选中的 PortInfo，用于批量关闭。"""
        return [self._ports[i] for i, c in enumerate(self._checked_rows) if c]

    def set_all_checked(self, checked: bool):
        """全选 / 全不选。"""
        self.beginResetModel()
        self._checked_rows = [checked] * len(self._ports)
        self.endResetModel()

    def is_all_checked(self) -> bool:
        """是否全部勾选（用于表头三态切换判断）。"""
        return len(self._checked_rows) > 0 and all(self._checked_rows)

    def is_none_checked(self) -> bool:
        """是否全部未勾选。"""
        return not any(self._checked_rows)
