#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : style.py
# @Software: PyCharm
# @Description:
#   全局样式表集中管理。对应 Java 前端 css/style.css 的浅色主题部分。
#   采用 QSS（Qt Style Sheet）实现，各子控件按需引用对应常量。
# ======================================================================

# ----------------------------------------------------------------------
# 全局应用样式：作用于 QApplication
# ----------------------------------------------------------------------
APP_QSS = """
QMainWindow, QWidget {
    background-color: #f5f7fa;
    font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
    font-size: 9pt;
    color: #333333;
}

/* 滚动条：细窄、圆角、更现代 */
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #c0c6cf;
    border-radius: 4px;
    min-height: 28px;
}
QScrollBar::handle:vertical:hover {
    background: #9aa3af;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    background: transparent;
    height: 8px;
    margin: 0px;
}
QScrollBar::handle:horizontal {
    background: #c0c6cf;
    border-radius: 4px;
    min-width: 28px;
}
QScrollBar::handle:horizontal:hover {
    background: #9aa3af;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}
"""

# ----------------------------------------------------------------------
# 卡片容器样式：白色背景 + 圆角 + 轻微阴影
# ----------------------------------------------------------------------
CARD_STYLE = """
QWidget {
    background-color: #ffffff;
    border-radius: 8px;
}
"""

# ----------------------------------------------------------------------
# 标题文本样式
# ----------------------------------------------------------------------
TITLE_LABEL_STYLE = """
QLabel {
    color: #1976D2;
    font-size: 16pt;
    font-weight: bold;
    padding: 4px;
}
"""

# 次要信息文字样式
INFO_LABEL_STYLE = "color: #666666; font-size: 9pt; padding: 4px;"

# 头像圆形徽标样式
AVATAR_LABEL_STYLE = """
QLabel {
    background-color: #FF9800;
    border-radius: 14px;
    color: white;
    font-weight: bold;
    font-size: 10pt;
}
QLabel:hover {
    background-color: #F57C00;
}
"""

# ----------------------------------------------------------------------
# 输入框样式
# ----------------------------------------------------------------------
LINE_EDIT_STYLE = """
QLineEdit {
    padding: 6px 10px;
    border: 1px solid #dcdcdc;
    border-radius: 4px;
    font-size: 9pt;
    background-color: #fafafa;
}
QLineEdit:focus {
    border: 1px solid #2196F3;
    background-color: #ffffff;
}
"""

# 下拉框通用样式
COMBO_BOX_STYLE = """
QComboBox {
    padding: 5px 8px;
    border: 1px solid #dcdcdc;
    border-radius: 4px;
    font-size: 9pt;
    background-color: #fafafa;
    min-width: 85px;
}
QComboBox::drop-down {
    margin-right: 10px;
    border: none;
}
QComboBox::down-arrow {
    width: 16px;
    height: 16px;
    border-radius: 4px;
}
QComboBox:hover {
    border: 1px solid #2196F3;
}
QComboBox QAbstractItemView {
    border: 1px solid #dcdcdc;
    background-color: #ffffff;
    selection-background-color: #2196F3;
    selection-color: white;
    outline: none;
    font-size: 9pt;
}
"""

# ----------------------------------------------------------------------
# 按钮样式：按用途分色
# ----------------------------------------------------------------------

# 主按钮（蓝色，如「刷新」）
BTN_PRIMARY_STYLE = """
QPushButton {
    background-color: #2196F3;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px 14px;
    font-size: 9pt;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #1976D2;
}
QPushButton:pressed {
    background-color: #1565C0;
}
QPushButton:disabled {
    background-color: #b0bec5;
}
"""

# 次要按钮（灰色，如「搜索」）
BTN_DEFAULT_STYLE = """
QPushButton {
    background-color: #f0f0f0;
    color: #333333;
    border: none;
    border-radius: 4px;
    padding: 6px 14px;
    font-size: 9pt;
}
QPushButton:hover {
    background-color: #e0e0e0;
}
QPushButton:pressed {
    background-color: #d0d0d0;
}
"""

# 警告按钮（橙色，如「清除筛选」）
BTN_WARNING_STYLE = """
QPushButton {
    background-color: #FF9800;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px 14px;
    font-size: 9pt;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #F57C00;
}
QPushButton:pressed {
    background-color: #E65100;
}
"""

# 危险按钮（红色，如「关闭」进程）
BTN_DANGER_STYLE = """
QPushButton {
    background-color: #F44336;
    color: white;
    border: none;
    border-radius: 3px;
    padding: 3px 10px;
    font-size: 8pt;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #D32F2F;
}
QPushButton:pressed {
    background-color: #B71C1C;
}
"""

# 批量关闭按钮（红色，稍大）
BTN_BATCH_KILL_STYLE = """
QPushButton {
    background-color: #F44336;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px 14px;
    font-size: 9pt;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #D32F2F;
}
QPushButton:disabled {
    background-color: #b0bec5;
}
"""

# ----------------------------------------------------------------------
# 表格样式
# ----------------------------------------------------------------------
TABLE_STYLE = """
QTableView {
    background-color: #ffffff;
    border: none;
    gridline-color: #eeeeee;
    font-size: 9pt;
    selection-background-color: #BBDEFB;
    selection-color: #1565C0;
    alternate-background-color: #FAFAFA;
}
QTableView::item {
    padding: 4px 6px;
    border-bottom: 1px solid #f0f0f0;
}
QTableView::item:hover {
    background-color: #f5f9ff;
}
QTableView::item:selected {
    background-color: #BBDEFB;
    color: #1565C0;
    border: none;
}
QTableView::item:selected:active {
    background-color: #90CAF9;
    color: #0D47A1;
}
QHeaderView::section {
    background-color: #fafafa;
    color: #555555;
    border: none;
    border-bottom: 1px solid #e0e0e0;
    font-weight: bold;
    font-size: 9pt;
    padding: 6px 8px;
}
"""

# 统计栏灰色小字
STATS_LABEL_STYLE = "color: #555555; font-size: 9pt; padding: 4px;"

# 底部状态栏
STATUS_SUCCESS_STYLE = "color: #4CAF50; font-size: 9pt; font-weight: bold;"
STATUS_INFO_STYLE = "color: #666666; font-size: 9pt;"
