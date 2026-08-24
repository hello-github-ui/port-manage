#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/21 17:42
# @Author  : 19921224
# @File    : ui_widget.py
# @Software: PyCharm
# @Description:
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QHBoxLayout, QComboBox, QPushButton,
                             QSpacerItem, QSizePolicy, QVBoxLayout, QApplication, QTableWidget, QHeaderView,
                             QTableWidgetItem)


def print_value(value):
    print(value)


class UIWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        系统界面布局 - 优化版（圆润、柔和、现代化）
        """
        # ==========================================
        # 1. 主布局：垂直排列 (QVBoxLayout)
        # ==========================================
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(18)  # 卡片之间间距加大，更透气
        main_layout.setContentsMargins(25, 25, 25, 25)  # 四周留白更多

        # ==========================================
        # 2. 顶部卡片 (Port Manager 标题栏)
        # ==========================================
        # QWidget 卡片容器，表示容器或者画布，可以把它想象成一个空白的盒子，容器整体对外呈现为一个整体
        top_card = QWidget()
        top_card.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 12px;
                /* 去掉边框，改用阴影模拟卡片感 */
            }
        """)
        # 卡片容器的内部布局
        top_layout = QHBoxLayout(top_card)
        top_layout.setContentsMargins(25, 15, 25, 15)
        top_layout.setSpacing(20)

        # 左边：标题
        self.title_label = QLabel("Port Manager")
        self.title_label.setStyleSheet("""
            QLabel {
                color: #2196F3;
                font-size: 19px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        top_layout.addWidget(self.title_label)

        # 中间：弹簧
        top_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # 右边：信息组
        right_group = QHBoxLayout()
        right_group.setSpacing(22)

        os_label = QLabel("Windows")
        os_label.setStyleSheet("color: #757575; font-size: 14px; padding: 5px;")
        right_group.addWidget(os_label)

        port_label = QLabel("35 ports")
        port_label.setStyleSheet("color: #757575; font-size: 14px; padding: 5px;")
        right_group.addWidget(port_label)

        avatar_label = QLabel()
        avatar_label.setFixedSize(30, 30)
        avatar_label.setStyleSheet("""
            QLabel {
                background: linear-gradient(135deg, #FF9800, #FF5722);
                border-radius: 15px;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
            QLabel:hover {
                background: linear-gradient(135deg, #F57C00, #E64A19);
            }
        """)
        avatar_label.setAlignment(Qt.AlignCenter)
        avatar_label.setText("U")
        right_group.addWidget(avatar_label)

        top_layout.addLayout(right_group)
        main_layout.addWidget(top_card)

        # ==========================================
        # 3. 搜索栏卡片 (搜索框 + 按钮)
        # ==========================================
        search_card = QWidget()
        search_card.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 10px;
            }
        """)
        search_layout = QHBoxLayout(search_card)
        search_layout.setContentsMargins(20, 12, 20, 12)
        search_layout.setSpacing(12)

        # 搜索输入框（美化）
        self.search_input_edit = QLineEdit()
        self.search_input_edit.setPlaceholderText("搜索端口号 / 进程名 / PID...")
        self.search_input_edit.setMinimumWidth(220)
        self.search_input_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                background-color: #fafafa;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
                background-color: #ffffff;
            }
        """)
        search_layout.addWidget(self.search_input_edit)

        # 搜索按钮（灰色）
        self.search_btn = QPushButton("搜索")
        self.search_btn.setMinimumWidth(85)
        self.search_btn.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                color: #333;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        search_layout.addWidget(self.search_btn)

        # 刷新按钮（蓝色）
        self.flush_btn = QPushButton("刷新")
        self.flush_btn.setMinimumWidth(85)
        self.flush_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        search_layout.addWidget(self.flush_btn)

        # 暂停自动刷新按钮
        self.pause_auto_flush_btn = QPushButton("暂停自动刷新")
        self.pause_auto_flush_btn.setMinimumWidth(130)
        self.pause_auto_flush_btn.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                color: #333;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        search_layout.addWidget(self.pause_auto_flush_btn)

        main_layout.addWidget(search_card)

        # ==========================================
        # 4. 筛选栏卡片 (下拉框 + 清除按钮)
        # ==========================================
        filter_card = QWidget()
        filter_card.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 10px;
            }
        """)
        filter_layout = QHBoxLayout(filter_card)
        filter_layout.setContentsMargins(20, 12, 20, 12)
        filter_layout.setSpacing(12)

        # 通用下拉框样式
        combo_style = """
            QComboBox {
                padding: 8px 10px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                background-color: #fafafa;
                min-width: 90px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox:hover {
                border: 1px solid #2196F3;
            }
        """

        # 端口类型
        self.port_type_box_label = QLabel("端口类型：")
        self.port_type_box = QComboBox()
        self.port_type_box.setStyleSheet(combo_style)
        self.port_type_box.addItems(["全部", "前端", "后端", "数据库", "其它"])
        filter_layout.addWidget(self.port_type_box_label)
        filter_layout.addWidget(self.port_type_box)

        # 进程类型
        self.process_type_box_label = QLabel("进程类型：")
        self.process_type_box = QComboBox()
        self.process_type_box.setStyleSheet(combo_style)
        self.process_type_box.addItems(
            ["全部", "Java", "Node.js", "Python", "Web服务器", "数据库", "IDE", "浏览器", "系统", "其它"])
        filter_layout.addWidget(self.process_type_box_label)
        filter_layout.addWidget(self.process_type_box)

        # 协议
        self.protocol_type_box_label = QLabel("协议：")
        self.protocol_type_box = QComboBox()
        self.protocol_type_box.setStyleSheet(combo_style)
        self.protocol_type_box.addItems(["全部", "TCP", "UDP"])
        filter_layout.addWidget(self.protocol_type_box_label)
        filter_layout.addWidget(self.protocol_type_box)

        # 开发进程
        self.dev_process_box_label = QLabel("开发进程：")
        self.dev_process_box = QComboBox()
        self.dev_process_box.setStyleSheet(combo_style)
        self.dev_process_box.addItems(["全部", "是", "否"])
        filter_layout.addWidget(self.dev_process_box_label)
        filter_layout.addWidget(self.dev_process_box)

        # 常用端口
        self.commonly_used_port_box_label = QLabel("常用端口：")
        self.commonly_used_port_box = QComboBox()
        self.commonly_used_port_box.setStyleSheet(combo_style)
        self.commonly_used_port_box.addItems([
            "80 - HTTP", "443 - HTTPS", "3000 - React/Node", "3306 - MySQL",
            "5432 - PostgreSQL", "6379 - Redis", "8080 - Tomcat", "8888 - Jupyter",
            "9090 - Prometheus", "27017 - MongoDB"
        ])
        filter_layout.addWidget(self.commonly_used_port_box_label)
        filter_layout.addWidget(self.commonly_used_port_box)

        # 清除筛选按钮（橙色）
        self.clear_choose_btn = QPushButton("清除筛选")
        self.clear_choose_btn.setMinimumWidth(90)
        self.clear_choose_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:pressed {
                background-color: #E65100;
            }
        """)
        filter_layout.addWidget(self.clear_choose_btn)

        main_layout.addWidget(filter_card)

        # ==========================================
        # 5. 统计栏卡片 (端口数 + 时间)
        # ==========================================
        stats_card = QWidget()
        stats_card.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 10px;
            }
        """)
        stats_layout = QHBoxLayout(stats_card)
        stats_layout.setContentsMargins(20, 12, 20, 12)
        stats_layout.setSpacing(25)

        self.total_port_nums_label = QLabel("总端口数：35")
        self.dev_process_label = QLabel("开发进程：9")
        self.tcp_label = QLabel("TCP：35")
        self.udp_label = QLabel("UDP：0")
        self.latest_scan_time = QLabel("上次扫描：10:17:17")

        # 灰色小字体风格
        style = "color: #666666; font-size: 14px; padding: 5px;"
        self.total_port_nums_label.setStyleSheet(style)
        self.dev_process_label.setStyleSheet(style)
        self.tcp_label.setStyleSheet(style)
        self.udp_label.setStyleSheet(style)
        self.latest_scan_time.setStyleSheet(style)

        stats_layout.addWidget(self.total_port_nums_label)
        stats_layout.addWidget(self.dev_process_label)
        stats_layout.addWidget(self.tcp_label)
        stats_layout.addWidget(self.udp_label)
        stats_layout.addWidget(self.latest_scan_time)

        main_layout.addWidget(stats_card)

        # ==========================================
        # 6. 表格区域 (占位，后续加 QTableWidget)
        # ==========================================
        # 这里先留空，你可以加 QTableWidget 或者 QScrollArea + QTableWidget
        # table_widget = QTableWidget()
        # main_layout.addWidget(table_widget)

        table_card = QTableWidget()
        table_card.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 10px;
            }
        """)
        table_layout = QHBoxLayout(table_card)
        table_layout.setContentsMargins(20, 10, 20, 10)
        table_layout.setSpacing(15)
        # 创建表格
        self.port_table = QTableWidget()
        # 设置表格为10列显示
        self.port_table.setColumnCount(10)
        # 设置表头
        headers = ["端口", "类型", "协议", "状态", "PID", "进程名", "命令行", "用户", "开发进程", "操作"]
        self.port_table.setHorizontalHeaderLabels(headers)
        # 设置表格样式
        self.port_table.setStyleSheet("""
                    QTableWidget {
                        background-color: #ffffff;
                        border: none;  /* 去掉边框 */
                        gridline-color: #f0f0f0; /* 网格线颜色，很淡 */
                        font-size: 13px;
                    }
                    QTableWidget::item {
                        padding: 8px;
                        border-bottom: 1px solid #f0f0f0; /* 行分割线 */
                    }
                    QTableWidget::item:hover {
                        background-color: #f5f9ff; /* 鼠标悬停淡蓝色 */
                    }
                    QHeaderView::section {
                        background-color: #fafafa;
                        color: #666666;
                        border: none;
                        border-bottom: 1px solid #e0e0e0;
                        font-weight: bold;
                        font-size: 13px;
                        padding: 10px;
                    }
                """)
        # 设置列宽自适应
        self.port_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 这里我们加一列“复选框”作为第0列，后面列顺延
        self.port_table.insertColumn(0)
        self.port_table.setHorizontalHeaderItem(0, QTableWidgetItem(""))  # 表头留空
        self.port_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.port_table.setColumnWidth(0, 40)  # 复选框列宽度
        # 设置水平滚动条隐藏（如果数据不超宽）
        self.port_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 垂直滚动条保留
        self.port_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        table_layout.addWidget(self.port_table)
        main_layout.addWidget(table_card)

        # ==========================================
        # 7. 填充模拟数据 (2条)
        # ==========================================
        import v2.utils.mock_util as mock_util
        mock_util.fill_mock_data(self.port_table)

        # ==========================================
        # 8. 底部状态栏 (接在表格下面)
        # ==========================================
        status_card = QWidget()
        status_card.setStyleSheet("""
                   QWidget {
                       background-color: #ffffff;
                       border-radius: 10px;
                   }
               """)
        status_layout = QHBoxLayout(status_card)
        status_layout.setContentsMargins(20, 10, 20, 10)
        status_layout.setSpacing(15)
        self.status_label = QLabel("加载成功: 35 个端口")
        self.status_label.setStyleSheet("color: #4CAF50; font-size: 13px; font-weight: bold;")
        status_layout.addWidget(self.status_label)

        self.auto_refresh_label = QLabel("自动刷新：开启 (5 秒)")
        self.auto_refresh_label.setStyleSheet("color: #757575; font-size: 13px;")
        status_layout.addStretch()
        status_layout.addWidget(self.auto_refresh_label)
        main_layout.addWidget(status_card)

        # ==========================================
        # 最后设置窗口
        # ==========================================
        self.setLayout(main_layout)
        self.setGeometry(300, 300, 1100, 750)  # 窗口更大一点
        self.setWindowTitle("端口管理工具")
        self.setWindowIcon(QIcon('../icon.ico'))

        # 全局字体
        font = QFont("Microsoft YaHei", 10)
        self.setFont(font)

        self.show()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = UIWidget()
    sys.exit(app.exec_())
