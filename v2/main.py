#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/21 15:48
# @Author  : 19921224
# @File    : main.py
# @Software: PyCharm
# @Description:
#   应用入口。负责初始化 QApplication、应用全局样式、设置图标、显示主窗口。
#   Windows下设置AppUserModelID以确保任务栏图标正确显示。
# ======================================================================

import ctypes
import os
import sys

# 兜底：把项目根目录加入 sys.path
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from v2.ui import style
from v2.ui.main_window import MainWindow


def set_windows_app_id():
    """
    设置Windows应用程序用户模型ID（AppUserModelID）。
    这是确保Windows任务栏显示正确图标的关键步骤。
    如果不设置，Windows会将python.exe作为宿主进程，任务栏图标可能显示为Python图标。
    """
    if sys.platform == "win32":
        try:
            # 任意唯一标识符即可，格式建议: Company.Product.Subproduct.Version
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "PortManager.App.1.0"
            )
        except Exception:
            pass  # 非Windows或调用失败时静默忽略


def get_icon_path():
    """获取图标文件的绝对路径。"""
    # main.py在v2/目录下，icon.ico也在v2/目录下
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
    if os.path.exists(icon_path):
        return icon_path
    return None


if __name__ == '__main__':
    # 设置Windows任务栏ID
    set_windows_app_id()

    app = QApplication(sys.argv)

    # 设置应用图标（这会同时影响窗口标题栏和任务栏）
    icon_path = get_icon_path()
    if icon_path:
        app.setWindowIcon(QIcon(icon_path))

    # 应用全局样式表
    app.setStyleSheet(style.APP_QSS())

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
