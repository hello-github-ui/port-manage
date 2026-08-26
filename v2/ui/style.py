#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : style.py
# @Software: PyCharm
# @Description:
#   全局样式表集中管理，支持多主题切换（浅色/深色/蓝色/绿色/紫色）。
# ======================================================================

from dataclasses import dataclass


@dataclass
class ThemeColors:
    """主题颜色基类。"""
    # 背景色
    bg_primary: str = "#f5f7fa"
    bg_secondary: str = "#ffffff"
    bg_tertiary: str = "#fafafa"
    bg_hover: str = "#f5f9ff"
    bg_selected: str = "#BBDEFB"
    bg_selected_active: str = "#90CAF9"

    # 文本色
    text_primary: str = "#2c3e50"
    text_secondary: str = "#555555"
    text_muted: str = "#7f8c8d"
    text_selected: str = "#1565C0"
    text_selected_active: str = "#0D47A1"
    text_inverse: str = "#ffffff"

    # 边框色
    border: str = "#e8eaed"
    border_light: str = "#f0f0f0"
    border_focus: str = "#2196F3"

    # 品牌色
    primary: str = "#2196F3"
    primary_hover: str = "#1976D2"
    primary_pressed: str = "#1565C0"
    primary_disabled: str = "#b0bec5"

    # 功能色
    success: str = "#4CAF50"
    warning: str = "#FF9800"
    warning_hover: str = "#F57C00"
    warning_pressed: str = "#E65100"
    danger: str = "#F44336"
    danger_hover: str = "#D32F2F"
    danger_pressed: str = "#B71C1C"

    # 滚动条
    scrollbar_handle: str = "#c0c6cf"
    scrollbar_handle_hover: str = "#9aa3af"

    # 标题/强调色
    accent: str = "#1976D2"


@dataclass
class DarkThemeColors(ThemeColors):
    """深色主题。"""
    bg_primary: str = "#1a1a2e"
    bg_secondary: str = "#16213e"
    bg_tertiary: str = "#0f3460"
    bg_hover: str = "#1f4068"
    bg_selected: str = "#0d47a1"
    bg_selected_active: str = "#1565c0"

    text_primary: str = "#ecf0f1"
    text_secondary: str = "#bdc3c7"
    text_muted: str = "#95a5a6"
    text_selected: str = "#e3f2fd"
    text_selected_active: str = "#ffffff"

    border: str = "#2c3e50"
    border_light: str = "#34495e"
    border_focus: str = "#3498db"

    primary: str = "#3498db"
    primary_hover: str = "#2980b9"
    primary_pressed: str = "#1f6dad"

    success: str = "#2ecc71"
    warning: str = "#f39c12"
    warning_hover: str = "#e67e22"
    warning_pressed: str = "#d35400"
    danger: str = "#e74c3c"
    danger_hover: str = "#c0392b"
    danger_pressed: str = "#a93226"

    scrollbar_handle: str = "#4a5568"
    scrollbar_handle_hover: str = "#718096"

    accent: str = "#3498db"


@dataclass
class BlueThemeColors(ThemeColors):
    """蓝色主题（浅色基调，蓝色强调）。"""
    bg_primary: str = "#e3f2fd"
    bg_secondary: str = "#ffffff"
    bg_tertiary: str = "#bbdefb"
    bg_hover: str = "#90caf9"
    bg_selected: str = "#64b5f6"
    bg_selected_active: str = "#42a5f5"

    text_primary: str = "#0d47a1"
    text_secondary: str = "#1565c0"
    text_muted: str = "#1976d2"
    text_selected: str = "#0d47a1"
    text_selected_active: str = "#ffffff"

    border: str = "#90caf9"
    border_light: str = "#bbdefb"
    border_focus: str = "#1976d2"

    primary: str = "#1976d2"
    primary_hover: str = "#1565c0"
    primary_pressed: str = "#0d47a1"

    accent: str = "#0d47a1"


@dataclass
class GreenThemeColors(ThemeColors):
    """绿色主题（浅色基调，绿色强调）。"""
    bg_primary: str = "#e8f5e9"
    bg_secondary: str = "#ffffff"
    bg_tertiary: str = "#c8e6c9"
    bg_hover: str = "#a5d6a7"
    bg_selected: str = "#81c784"
    bg_selected_active: str = "#66bb6a"

    text_primary: str = "#1b5e20"
    text_secondary: str = "#2e7d32"
    text_muted: str = "#388e3c"
    text_selected: str = "#1b5e20"
    text_selected_active: str = "#ffffff"

    border: str = "#a5d6a7"
    border_light: str = "#c8e6c9"
    border_focus: str = "#2e7d32"

    primary: str = "#2e7d32"
    primary_hover: str = "#1b5e20"
    primary_pressed: str = "#145214"
    primary_disabled: str = "#a5d6a7"

    success: str = "#1b5e20"
    warning: str = "#ff8f00"
    danger: str = "#d32f2f"

    scrollbar_handle: str = "#81c784"
    scrollbar_handle_hover: str = "#66bb6a"

    accent: str = "#2e7d32"


@dataclass
class PurpleThemeColors(ThemeColors):
    """紫色主题（浅色基调，紫色强调）。"""
    bg_primary: str = "#f3e5f5"
    bg_secondary: str = "#ffffff"
    bg_tertiary: str = "#e1bee7"
    bg_hover: str = "#ce93d8"
    bg_selected: str = "#ba68c8"
    bg_selected_active: str = "#ab47bc"

    text_primary: str = "#4a148c"
    text_secondary: str = "#6a1b9a"
    text_muted: str = "#7b1fa2"
    text_selected: str = "#4a148c"
    text_selected_active: str = "#ffffff"

    border: str = "#ce93d8"
    border_light: str = "#e1bee7"
    border_focus: str = "#7b1fa2"

    primary: str = "#7b1fa2"
    primary_hover: str = "#6a1b9a"
    primary_pressed: str = "#4a148c"
    primary_disabled: str = "#ce93d8"

    success: str = "#2e7d32"
    warning: str = "#f57c00"
    danger: str = "#c62828"

    scrollbar_handle: str = "#ba68c8"
    scrollbar_handle_hover: str = "#ab47bc"

    accent: str = "#6a1b9a"


# 主题注册表：theme_id -> ThemeColors类
THEMES = {
    "light": ThemeColors,
    "dark": DarkThemeColors,
    "blue": BlueThemeColors,
    "green": GreenThemeColors,
    "purple": PurpleThemeColors,
}

_current_colors: ThemeColors = ThemeColors()
_current_theme_id: str = "light"


def get_colors() -> ThemeColors:
    """获取当前主题颜色。"""
    return _current_colors


def get_current_theme_id() -> str:
    """获取当前主题ID。"""
    return _current_theme_id


def set_theme(theme_id: str = "light"):
    """
    切换主题。
    
    :param theme_id: 主题ID：light/dark/blue/green/purple
    """
    global _current_colors, _current_theme_id
    theme_class = THEMES.get(theme_id, ThemeColors)
    _current_colors = theme_class()
    _current_theme_id = theme_id


def is_dark_theme() -> bool:
    """当前是否为深色主题。"""
    return isinstance(_current_colors, DarkThemeColors)


# ----------------------------------------------------------------------
# QSS 生成
# ----------------------------------------------------------------------

def _app_qss() -> str:
    c = _current_colors
    return f"""
QMainWindow, QWidget {{
    background-color: {c.bg_primary};
    font-family: 'Segoe UI', 'Microsoft YaHei', 'PingFang SC', sans-serif;
    font-size: 9pt;
    color: {c.text_primary};
}}

QScrollBar:vertical {{
    background: transparent;
    width: 8px;
    margin: 0px;
}}
QScrollBar::handle:vertical {{
    background: {c.scrollbar_handle};
    border-radius: 4px;
    min-height: 28px;
}}
QScrollBar::handle:vertical:hover {{
    background: {c.scrollbar_handle_hover};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
QScrollBar:horizontal {{
    background: transparent;
    height: 8px;
    margin: 0px;
}}
QScrollBar::handle:horizontal {{
    background: {c.scrollbar_handle};
    border-radius: 4px;
    min-width: 28px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {c.scrollbar_handle_hover};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

QToolTip {{
    background-color: {c.bg_secondary};
    color: {c.text_primary};
    border: 1px solid {c.border};
    border-radius: 4px;
    padding: 4px 8px;
}}
"""


def _card_qss() -> str:
    return f"""
QWidget {{
    background-color: transparent;
}}
"""


def _title_label_qss() -> str:
    c = _current_colors
    return f"""
QLabel {{
    color: {c.accent};
    font-size: 16pt;
    font-weight: bold;
    padding: 4px;
}}
"""


def _info_label_qss() -> str:
    c = _current_colors
    return f"color: {c.text_secondary}; font-size: 9pt; padding: 4px;"


def _line_edit_qss() -> str:
    c = _current_colors
    return f"""
QLineEdit {{
    padding: 7px 12px;
    border: 1px solid {c.border};
    border-radius: 6px;
    font-size: 9pt;
    background-color: {c.bg_secondary};
    color: {c.text_primary};
}}
QLineEdit:focus {{
    border: 1px solid {c.border_focus};
    background-color: {c.bg_secondary};
}}
QLineEdit::placeholder {{
    color: {c.text_muted};
}}
"""


def _combo_box_qss() -> str:
    c = _current_colors
    return f"""
QComboBox {{
    padding: 6px 10px;
    border: 1px solid {c.border};
    border-radius: 6px;
    font-size: 9pt;
    background-color: {c.bg_secondary};
    color: {c.text_primary};
    min-width: 85px;
}}
QComboBox:hover {{
    border: 1px solid {c.border_focus};
}}
QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    border-left: none;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
}}
QComboBox::down-arrow {{
    width: 12px;
    height: 12px;
}}
QComboBox QAbstractItemView {{
    border: 1px solid {c.border};
    border-radius: 4px;
    background-color: {c.bg_secondary};
    color: {c.text_primary};
    selection-background-color: {c.bg_selected};
    selection-color: {c.text_selected};
    outline: none;
    font-size: 9pt;
    padding: 4px;
}}
"""


def _btn_primary_qss() -> str:
    c = _current_colors
    return f"""
QPushButton {{
    background-color: {c.primary};
    color: {c.text_inverse};
    border: none;
    border-radius: 6px;
    padding: 7px 16px;
    font-size: 9pt;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: {c.primary_hover};
}}
QPushButton:pressed {{
    background-color: {c.primary_pressed};
}}
QPushButton:disabled {{
    background-color: {c.primary_disabled};
}}
"""


def _btn_default_qss() -> str:
    c = _current_colors
    return f"""
QPushButton {{
    background-color: {c.bg_secondary};
    color: {c.text_primary};
    border: 1px solid {c.border};
    border-radius: 6px;
    padding: 7px 16px;
    font-size: 9pt;
}}
QPushButton:hover {{
    background-color: {c.bg_hover};
    border-color: {c.border_focus};
}}
QPushButton:pressed {{
    background-color: {c.bg_tertiary};
}}
"""


def _btn_warning_qss() -> str:
    c = _current_colors
    return f"""
QPushButton {{
    background-color: {c.warning};
    color: {c.text_inverse};
    border: none;
    border-radius: 6px;
    padding: 7px 16px;
    font-size: 9pt;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: {c.warning_hover};
}}
QPushButton:pressed {{
    background-color: {c.warning_pressed};
}}
"""


def _btn_danger_qss() -> str:
    c = _current_colors
    return f"""
QPushButton {{
    background-color: {c.danger};
    color: {c.text_inverse};
    border: none;
    border-radius: 4px;
    padding: 4px 12px;
    font-size: 8pt;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: {c.danger_hover};
}}
QPushButton:pressed {{
    background-color: {c.danger_pressed};
}}
"""


def _btn_batch_kill_qss() -> str:
    c = _current_colors
    return f"""
QPushButton {{
    background-color: {c.danger};
    color: {c.text_inverse};
    border: none;
    border-radius: 6px;
    padding: 7px 16px;
    font-size: 9pt;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: {c.danger_hover};
}}
QPushButton:disabled {{
    background-color: {c.primary_disabled};
}}
"""


def _table_qss() -> str:
    c = _current_colors
    return f"""
QTableView {{
    background-color: {c.bg_secondary};
    border: 1px solid {c.border};
    border-radius: 8px;
    gridline-color: {c.border_light};
    font-size: 9pt;
    selection-background-color: {c.bg_selected};
    selection-color: {c.text_selected};
    alternate-background-color: {c.bg_tertiary};
    outline: none;
}}
QTableView::item {{
    padding: 6px 8px;
    border-bottom: 1px solid {c.border_light};
}}
QTableView::item:hover {{
    background-color: {c.bg_hover};
}}
QTableView::item:selected {{
    background-color: {c.bg_selected};
    color: {c.text_selected};
    border: none;
}}
QTableView::item:selected:active {{
    background-color: {c.bg_selected_active};
    color: {c.text_selected_active};
}}
QHeaderView::section {{
    background-color: {c.bg_tertiary};
    color: {c.text_secondary};
    border: none;
    border-bottom: 2px solid {c.border};
    font-weight: 600;
    font-size: 9pt;
    padding: 10px 8px;
}}
QHeaderView::section:hover {{
    background-color: {c.bg_hover};
}}
QTableCornerButton::section {{
    background-color: {c.bg_tertiary};
    border: none;
    border-bottom: 2px solid {c.border};
}}
"""


def _stats_label_qss() -> str:
    c = _current_colors
    return f"color: {c.text_secondary}; font-size: 9pt; font-weight: 500; padding: 4px 8px;"


def _filter_label_qss() -> str:
    c = _current_colors
    return f"color: {c.text_secondary}; font-size: 9pt; font-weight: 500;"


def _status_success_qss() -> str:
    c = _current_colors
    return f"color: {c.success}; font-size: 9pt; font-weight: 600;"


def _status_info_qss() -> str:
    c = _current_colors
    return f"color: {c.text_muted}; font-size: 9pt;"


def _checkbox_qss() -> str:
    """复选框样式 - 透明背景，避免深色主题下的阴影/错位感。"""
    c = _current_colors
    return f"""
QCheckBox {{
    spacing: 6px;
    color: {c.text_primary};
    background: transparent;
    border: none;
}}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 2px solid {c.text_secondary};
    border-radius: 3px;
    background-color: transparent;
}}
QCheckBox::indicator:hover {{
    border-color: {c.primary};
}}
QCheckBox::indicator:checked {{
    background-color: {c.primary};
    border-color: {c.primary};
}}
QCheckBox::indicator:checked:hover {{
    background-color: {c.primary_hover};
    border-color: {c.primary_hover};
}}
"""


# ----------------------------------------------------------------------
# 导出：函数式调用，每次获取最新主题样式
# ----------------------------------------------------------------------

def APP_QSS(): return _app_qss()
def CARD_STYLE(): return _card_qss()
def TITLE_LABEL_STYLE(): return _title_label_qss()
def INFO_LABEL_STYLE(): return _info_label_qss()
def LINE_EDIT_STYLE(): return _line_edit_qss()
def COMBO_BOX_STYLE(): return _combo_box_qss()
def BTN_PRIMARY_STYLE(): return _btn_primary_qss()
def BTN_DEFAULT_STYLE(): return _btn_default_qss()
def BTN_WARNING_STYLE(): return _btn_warning_qss()
def BTN_DANGER_STYLE(): return _btn_danger_qss()
def BTN_BATCH_KILL_STYLE(): return _btn_batch_kill_qss()
def TABLE_STYLE(): return _table_qss()
def STATS_LABEL_STYLE(): return _stats_label_qss()
def FILTER_LABEL_STYLE(): return _filter_label_qss()
def STATUS_SUCCESS_STYLE(): return _status_success_qss()
def STATUS_INFO_STYLE(): return _status_info_qss()
def CHECKBOX_STYLE(): return _checkbox_qss()
