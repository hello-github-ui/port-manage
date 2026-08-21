#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/21 15:46
# @Author  : 19921224
# @File    : ExampleWidget.py
# @Software: PyCharm
# @Description:
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit, QHBoxLayout


class ExampleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        表格布局
        """
        form_layout = QFormLayout()

        total_port_nums_label = QLabel("总端口数：")
        total_port_nums_label_edit = QLineEdit("")
        dev_process_label = QLabel("开发进程：")
        dev_process_label_edit = QLineEdit("")
        tcp_label = QLabel("TCP：")
        tcp_label_edit = QLineEdit("")
        udp_label = QLabel("UDP：")
        udp_label_edit = QLineEdit("")
        latest_scan_time = QLabel("上次扫描：")
        latest_scan_time_edit = QLineEdit("")

        # 已上5个表单项需要显示在一行，需要使用 QHBoxLayout 水平布局来设计
        h4_layout = QHBoxLayout()
        h4_layout.addWidget(total_port_nums_label)
        h4_layout.addWidget(total_port_nums_label_edit)
        h4_layout.addWidget(dev_process_label)
        h4_layout.addWidget(dev_process_label_edit)
        h4_layout.addWidget(tcp_label)
        h4_layout.addWidget(tcp_label_edit)
        h4_layout.addWidget(udp_label)
        h4_layout.addWidget(udp_label_edit)
        h4_layout.addWidget(latest_scan_time)
        h4_layout.addWidget(latest_scan_time_edit)
        # 将水平布局作为”值“添加到表单行中
        form_layout.addRow(h4_layout)

        self.setLayout(form_layout)

        # 把窗口放到屏幕上并且设置窗口大小，参数分别代表屏幕坐标的 x、y 和窗口大小的宽、高
        # 这个方法是 resize() 和 move() 的合体
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle("端口管理工具")
        self.setWindowIcon(QIcon('../icon.ico'))
        self.show()
