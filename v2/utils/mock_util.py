#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24 11:10
# @Author  : 19921224
# @File    : mock_util.py
# @Software: PyCharm
# @Description:
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton


def fill_mock_data(table_card: QTableWidget):
    """
    填充模拟数据 (方便你后续替换成真实数据)
    """
    # 清空表格
    table_card.setRowCount(0)

    # 模拟数据列表 (每行是一个列表，对应一行的数据)
    mock_data = [
        # 复选框(自动处理), 端口, 类型, 协议, 状态, PID, 进程名, 命令行, 用户, 开发进程, 操作(按钮)
        [
            "135", "其他", "TCP", "LISTENING", "1192", "svchost.exe",
            "C:\\WINDOWS\\system32\\svchost.exe -k RPCSS -p", "-", "-",
            "false"  # 用于判断是否高亮“开发进程”
        ],
        [
            "63342", "其他", "TCP", "LISTENING", "47036", "pycharm64.exe",
            "C:\\Program Files\\JetBrains\\PyCharm 2024.3.1\\bin\\pycharm64.exe", "-", "是",
            "true"  # 标记为开发进程，后续可以高亮
        ]
    ]

    # 设置行数
    table_card.setRowCount(len(mock_data))

    # 遍历数据填充
    for row_idx, row_data in enumerate(mock_data):
        # 1. 复选框 (第0列)
        checkbox_item = QTableWidgetItem()
        checkbox_item.setCheckState(Qt.Unchecked)
        table_card.setItem(row_idx, 0, checkbox_item)

        # 2. 端口 (第1列) - 加粗
        port_item = QTableWidgetItem(row_data[0])
        port_item.setFont(QFont("Microsoft YaHei", 13, QFont.Bold))
        table_card.setItem(row_idx, 1, port_item)

        # 3. 类型 (第2列) - 灰色背景标签风格
        type_item = QTableWidgetItem(row_data[1])
        type_item.setTextAlignment(Qt.AlignCenter)
        # 模拟“其他”的灰色背景
        type_item.setBackground(QColor("#f0f0f0"))
        type_item.setForeground(QColor("#666666"))
        table_card.setItem(row_idx, 2, type_item)

        # 4. 协议 (第3列)
        table_card.setItem(row_idx, 3, QTableWidgetItem(row_data[2]))

        # 5. 状态 (第4列) - 蓝色背景标签
        status_item = QTableWidgetItem(row_data[3])
        status_item.setTextAlignment(Qt.AlignCenter)
        status_item.setBackground(QColor("#E3F2FD"))  # 浅蓝背景
        status_item.setForeground(QColor("#1976D2"))  # 深蓝文字
        status_item.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        table_card.setItem(row_idx, 4, status_item)

        # 6. PID (第5列)
        table_card.setItem(row_idx, 5, QTableWidgetItem(row_data[4]))

        # 7. 进程名 (第6列)
        table_card.setItem(row_idx, 6, QTableWidgetItem(row_data[5]))

        # 8. 命令行 (第7列) - 灰色小字
        cmd_item = QTableWidgetItem(row_data[6])
        cmd_item.setForeground(QColor("#999999"))
        cmd_item.setFont(QFont("Microsoft YaHei", 11))
        table_card.setItem(row_idx, 7, cmd_item)

        # 9. 用户 (第8列)
        table_card.setItem(row_idx, 8, QTableWidgetItem(row_data[7]))

        # 10. 开发进程 (第9列) - 如果是“是”，显示橙色
        dev_process_item = QTableWidgetItem(row_data[8])
        if row_data[8] == "是":
            dev_process_item.setForeground(QColor("#FF9800"))  # 橙色
            dev_process_item.setFont(QFont("Microsoft YaHei", 13, QFont.Bold))
        table_card.setItem(row_idx, 9, dev_process_item)

        # 11. 操作 (第10列) - 放“关闭”按钮
        # 注意：QTableWidget 的 cell 不能直接放按钮，通常用 setCellWidget
        close_btn = QPushButton("关闭")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 12px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        # 绑定点击信号 (这里先打印行号，方便调试)
        close_btn.clicked.connect(lambda checked, r=row_idx: on_close_clicked(r))

        # 将按钮放入单元格
        table_card.setCellWidget(row_idx, 10, close_btn)


def on_close_clicked(table_card: QTableWidget, row):
    """
    点击“关闭”按钮的槽函数
    """
    port = table_card.item(row, 1).text()
    print(f"正在关闭端口: {port} (行号: {row})")
    # 这里后续可以调用你的关闭端口函数
    # 也可以弹窗确认
    # QMessageBox.information(self, "提示", f"即将关闭端口 {port}")
