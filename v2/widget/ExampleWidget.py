#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/21 15:46
# @Author  : 19921224
# @File    : ExampleWidget.py
# @Software: PyCharm
# @Description:
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit, QHBoxLayout, QComboBox, QPushButton


def print_value(value):
    print(value)


class ExampleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        表格布局
        """
        form_layout = QFormLayout()

        ### 表单第二行项
        # 搜索端口号/进程名/PID
        self.search_input_edit = QLineEdit().setPlaceholderText("搜索端口号/进程名/PID")
        # 搜索 按钮
        self.search_btn = QPushButton("搜索")
        # 刷新 按钮
        self.flush_btn = QPushButton("刷新")
        # 暂停自动刷新 按钮
        self.pause_auto_flush_btn = QPushButton("暂停自动刷新")
        # 以上内容水平显示
        h2_layout = QHBoxLayout()
        h2_layout.addWidget(self.search_input_edit)
        h2_layout.addWidget(self.search_btn)
        h2_layout.addWidget(self.flush_btn)
        h2_layout.addWidget(self.pause_auto_flush_btn)

        ### 表单第三行项，其中多是下拉选择框，使用 QComBox 对象实现
        # 端口类型
        self.port_type_box_label = QLabel("端口类型：")
        self.port_type_box = QComboBox()
        self.port_type_box.resize(100, 20)
        # 添加条目
        self.port_type_box.addItem("全部")
        self.port_type_box.addItem("前端")
        self.port_type_box.addItem("后端")
        self.port_type_box.addItem("数据库")
        self.port_type_box.addItem("其它")
        # 信号
        # 条目发生改变，发射信号，传递条目内容
        self.port_type_box.currentIndexChanged[str].connect(print_value)
        # 在下拉列表中，鼠标移动到某个条目时发出信号，传递条目内容
        self.port_type_box.highlighted[str].connect(print_value)
        # 进程类型
        self.process_type_box_label = QLabel("端口类型：")
        self.process_type_box = QComboBox()
        # self.process_type_box.move(100, 20)
        self.process_type_box.addItem("全部")
        self.process_type_box.addItem("Java")
        self.process_type_box.addItem("Node.js")
        self.process_type_box.addItem("Python")
        self.process_type_box.addItem("Web服务器")
        self.process_type_box.addItem("数据库")
        self.process_type_box.addItem("IDE")
        self.process_type_box.addItem("浏览器")
        self.process_type_box.addItem("系统")
        self.process_type_box.addItem("其它")
        self.process_type_box.currentIndexChanged[str].connect(print_value)
        self.process_type_box.highlighted[str].connect(print_value)
        # 协议
        self.protocol_type_box_label = QLabel("协议：")
        self.protocol_type_box = QComboBox()
        self.protocol_type_box.addItem("全部")
        self.protocol_type_box.addItem("TCP")
        self.protocol_type_box.addItem("UDP")
        # 开发进程
        self.dev_process_box_label = QLabel("开发进程：")
        self.dev_process_box = QComboBox()
        self.dev_process_box.addItem("全部")
        self.dev_process_box.addItem("是")
        self.dev_process_box.addItem("否")
        # 常用端口
        self.commonly_used_port_box_label = QLabel("常用端口：")
        self.commonly_used_port_box = QComboBox()
        self.commonly_used_port_box.addItem("80 - HTTP")
        self.commonly_used_port_box.addItem("443 - HTTPS")
        self.commonly_used_port_box.addItem("3000 - React/Node")
        self.commonly_used_port_box.addItem("3306 - MySQL")
        self.commonly_used_port_box.addItem("5432 - PostgreSQL")
        self.commonly_used_port_box.addItem("6379 - Redis")
        self.commonly_used_port_box.addItem("8080 - Tomcat")
        self.commonly_used_port_box.addItem("8888 - Jupyter")
        self.commonly_used_port_box.addItem("9090 - Prometheus")
        self.commonly_used_port_box.addItem("27017 - MongoDB")
        # 清楚筛选
        self.clear_choose_btn = QPushButton("清楚筛选")

        # 以上6个表单项置于表单中的一行，使用水平布局设置
        h3_layout = QHBoxLayout()
        h3_layout.addWidget(self.port_type_box_label)
        h3_layout.addWidget(self.port_type_box)
        h3_layout.addWidget(self.process_type_box_label)
        h3_layout.addWidget(self.process_type_box)
        h3_layout.addWidget(self.protocol_type_box_label)
        h3_layout.addWidget(self.protocol_type_box)
        h3_layout.addWidget(self.dev_process_box_label)
        h3_layout.addWidget(self.dev_process_box)
        h3_layout.addWidget(self.commonly_used_port_box_label)
        h3_layout.addWidget(self.commonly_used_port_box)
        h3_layout.addWidget(self.commonly_used_port_box_label)
        h3_layout.addWidget(self.commonly_used_port_box)
        h3_layout.addWidget(self.clear_choose_btn)

        ### 表单第四行项
        self.total_port_nums_label = QLabel("总端口数：")
        self.total_port_nums_label_edit = QLineEdit("")
        self.dev_process_label = QLabel("开发进程：")
        self.dev_process_label_edit = QLineEdit("")
        self.tcp_label = QLabel("TCP：")
        self.tcp_label_edit = QLineEdit("")
        self.udp_label = QLabel("UDP：")
        self.udp_label_edit = QLineEdit("")
        self.latest_scan_time = QLabel("上次扫描：")
        self.latest_scan_time_edit = QLineEdit("")

        # (表单第四行项)以上5个表单项需要显示在一行，需要使用 QHBoxLayout 水平布局来设计
        h4_layout = QHBoxLayout()
        h4_layout.addWidget(self.total_port_nums_label)
        h4_layout.addWidget(self.total_port_nums_label_edit)
        h4_layout.addWidget(self.dev_process_label)
        h4_layout.addWidget(self.dev_process_label_edit)
        h4_layout.addWidget(self.tcp_label)
        h4_layout.addWidget(self.tcp_label_edit)
        h4_layout.addWidget(self.udp_label)
        h4_layout.addWidget(self.udp_label_edit)
        h4_layout.addWidget(self.latest_scan_time)
        h4_layout.addWidget(self.latest_scan_time_edit)

        # 将水平布局作为”值“添加到表单行中
        form_layout.addRow(h2_layout)
        form_layout.addRow(h3_layout)
        form_layout.addRow(h4_layout)

        self.setLayout(form_layout)

        # 把窗口放到屏幕上并且设置窗口大小，参数分别代表屏幕坐标的 x、y 和窗口大小的宽、高
        # 这个方法是 resize() 和 move() 的合体
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle("端口管理工具")
        self.setWindowIcon(QIcon('../icon.ico'))
        self.show()
