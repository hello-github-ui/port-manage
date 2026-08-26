#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/26
# @Description:
#   应用启动入口（根目录级别）。
#   用于PyInstaller打包：从项目根目录启动，确保v2包可以被正确导入。
#   开发运行也可以直接使用：python PortManager.py
# ======================================================================

import ctypes
import os
import sys


def get_resource_path(relative_path: str) -> str:
    """
    获取资源文件的绝对路径，兼容开发环境和PyInstaller打包环境。
    PyInstaller打包后，临时解压目录在 sys._MEIPASS 中。
    """
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def set_windows_app_id():
    """设置Windows任务栏应用ID，确保图标正确显示。"""
    if sys.platform == "win32":
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "PortManager.App.1.0"
            )
        except Exception:
            pass


def get_icon_path():
    """获取图标文件路径（优先v2目录下的icon.ico）。"""
    # 尝试多个位置找图标
    for candidate in [
        get_resource_path("v2/icon.ico"),
        get_resource_path("icon.ico"),
    ]:
        if os.path.exists(candidate):
            return candidate
    return None


def main():
    # Windows任务栏ID
    set_windows_app_id()

    # 确保项目根目录在sys.path中（打包后sys._MEIPASS就是根）
    root_dir = os.path.dirname(os.path.abspath(__file__))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)

    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QApplication

    from v2.ui import style
    from v2.ui.main_window import MainWindow

    app = QApplication(sys.argv)

    # 设置应用图标
    icon_path = get_icon_path()
    if icon_path:
        app.setWindowIcon(QIcon(icon_path))

    # 应用全局样式
    app.setStyleSheet(style.APP_QSS())

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
