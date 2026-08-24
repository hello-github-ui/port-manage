#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/21 15:48
# @Author  : 19921224
# @File    : main.py
# @Software: PyCharm
# @Description:
#   应用入口。负责初始化 QApplication、应用全局样式、显示主窗口。
#   通过 sys.path 兜底，保证「直接运行 main.py」与「IDE 运行」均可
#   正常导入 v2 包下的各模块。
# ======================================================================

import os
import sys

# 兜底：把项目根目录（port-manage）加入 sys.path，
# 使 `from v2.xxx import ...` 在直接运行脚本时也能生效。
# __file__ 为 v2/main.py，上两级即项目根。
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication

from v2.ui import style
from v2.ui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 应用全局样式表（背景、滚动条等）
    app.setStyleSheet(style.APP_QSS)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
