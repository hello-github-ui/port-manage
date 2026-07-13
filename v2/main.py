#!/usr/bin/env v2
# -*- coding: utf-8 -*-
# @Time    : 2026/7/13 11:07
# @Author  : 19921224
# @File    : main.py
# @Software: PyCharm
# @Description:
import sys
# PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication,QMainWindow

from v2.gui import Ui_Form


class MainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    window = MainWindow()
    # 将窗口控件显示在屏幕上
    window.show()
    # 程序运行，sys.exit方法确保程序完整退出
    sys.exit(app.exec_())