#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 设置任务栏中的图标显示
import ctypes
import os
import signal
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QComboBox, QLabel, QTextEdit,
    QGroupBox, QGridLayout, QProgressBar, QMessageBox,
    QFileDialog, QSpinBox, QTabWidget, QCheckBox
)

my_app_id = "my_port_manager"
# windows 特有：设置任务栏图标
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
except AttributeError:
    pass # 非Windows平台跳过


def get_system_font(size=12):
    """
    获取跨平台的系统字体
    按优先级尝试不同平台的中文字体
    :param size: 字体大小
    :return: QFont()
    """
    font_families = [
        'Arial',
        'Noto Sans CJK SC',
        'Noto Sans CJK TC',
        'Microsoft YaHei',
        'PingFang SC',
        'Hiragino Sans GB',
        'Heiti SC',
        'SimHei',
        'WenQuanYi Micro Hei',
        'Arial Unicode MS'
    ]
    font = QFont()
    for family in font_families:
        if QFont(family).exactMatch():
            font.setFamily(family)
            font.setPointSize(size)
            return font
    font.setPointSize(size)
    return font


class MainWindow(QMainWindow):
    """
    主窗口类
    提供端口管理器的图形界面
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('端口管理工具')
        self.setGeometry(100, 100, 880, 650)
        icon_path = get_icon_path()
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.create_search_input()


    def create_search_input(self):
        """创建端口号/进程名/PID输入区域"""
        search_group = QGroupBox('搜索区域')
        search_layout = QHBoxLayout(search_group)
        search_layout.setSpacing(10)



def get_icon_path():
    """获取图标文件路径，支持打包后运行"""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'icon.ico')
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')

def main():
    """图形界面入口函数"""
    app = QApplication(sys.argv)
    icon_path = get_icon_path()
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()