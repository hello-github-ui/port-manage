#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/21 15:48
# @Author  : 19921224
# @File    : main.py
# @Software: PyCharm
# @Description:
import sys

from PyQt5.QtWidgets import QApplication

from v2.widget.ExampleWidget import ExampleWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExampleWidget()
    sys.exit(app.exec_())
