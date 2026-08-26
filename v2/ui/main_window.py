#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/8/24
# @Author  : 19921224
# @File    : main_window.py
# @Software: PyCharm
# @Description:
#   主窗口：组合所有控件，连接信号槽，对接业务服务层。
#   对应 Java 版前端 app.js 的所有交互逻辑。
# ======================================================================

import platform
import sys
from typing import List

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
                             QLabel, QMainWindow, QMessageBox, QStyle,
                             QVBoxLayout, QWidget)

from v2.config import settings
from v2.model.port_info import PortInfo
from v2.service.process_service import ProcessService
from v2.service.scan_service import ScanService
from v2.ui import style
from v2.ui.widgets.filter_bar import FilterBar
from v2.ui.widgets.port_table import PortTable
from v2.ui.widgets.search_bar import SearchBar
from v2.ui.widgets.stats_bar import StatsBar
from v2.ui.widgets.status_bar import StatusBar
from v2.ui.widgets.top_bar import TopBar


class MainWindow(QMainWindow):
    """主窗口。"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("端口管理工具")
        self.resize(1280, 760)

        # 服务层
        self.scan_service = ScanService(self)
        self.process_service = ProcessService()

        # 当前显示的端口列表（经过搜索/筛选后的）
        self._displayed_ports: List[PortInfo] = []

        # UI控件
        self.top_bar: TopBar = None
        self.search_bar: SearchBar = None
        self.filter_bar: FilterBar = None
        self.stats_bar: StatsBar = None
        self.port_table: PortTable = None
        self.status_bar: StatusBar = None

        # 关闭进程后延迟刷新的定时器
        self._refresh_after_kill_timer = QTimer(self)
        self._refresh_after_kill_timer.setSingleShot(True)
        self._refresh_after_kill_timer.setInterval(2000)
        self._refresh_after_kill_timer.timeout.connect(self.scan_service.trigger_scan)

        self._init_ui()
        self._connect_signals()
        self._setup_font()

        # 启动自动刷新
        self.scan_service.start_auto_refresh()

    def _init_ui(self):
        """初始化UI布局。"""
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 16, 16, 8)
        root.setSpacing(10)

        # 顶部栏
        self.top_bar = TopBar()
        root.addWidget(self.top_bar)

        # 搜索栏
        self.search_bar = SearchBar()
        root.addWidget(self.search_bar)

        # 筛选栏
        self.filter_bar = FilterBar()
        root.addWidget(self.filter_bar)

        # 统计栏
        self.stats_bar = StatsBar()
        root.addWidget(self.stats_bar)

        # 分隔线
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setStyleSheet(f"color: {style.get_colors().border};")
        root.addWidget(sep)

        # 端口表格
        self.port_table = PortTable()
        root.addWidget(self.port_table, stretch=1)

        # 底部状态栏
        self.status_bar = StatusBar()
        root.addWidget(self.status_bar)

    def _connect_signals(self):
        """连接所有信号槽。"""
        # 主题切换
        self.top_bar.theme_changed.connect(self._on_theme_changed)

        # 搜索栏
        self.search_bar.search_requested.connect(self._on_search)
        self.search_bar.refresh_requested.connect(self._on_refresh_clicked)
        self.search_bar.auto_refresh_toggled.connect(self._on_auto_refresh_toggled)
        self.search_bar.batch_kill_requested.connect(self._on_batch_kill)

        # 筛选栏
        self.filter_bar.filter_changed.connect(self._on_filter_changed)
        self.filter_bar.clear_filter.connect(self._on_clear_filter)

        # 表格：单个关闭按钮
        self.port_table.kill_requested.connect(self._on_kill_single)
        self.port_table.selection_changed.connect(self._on_selection_changed)

        # 扫描服务信号
        self.scan_service.ports_updated.connect(self._on_ports_updated)
        self.scan_service.scan_error.connect(self._on_scan_error)
        self.scan_service.scan_finished.connect(self._on_scan_finished)
        self.scan_service.scan_started.connect(self._on_scan_started)

    def _setup_font(self):
        """自动选择系统最佳字体。"""
        font_db = QFontDatabase()
        families = font_db.families()
        preferred = []
        if sys.platform == "win32":
            preferred = ["Segoe UI", "Microsoft YaHei UI", "微软雅黑", "Arial"]
        elif sys.platform == "darwin":
            preferred = ["PingFang SC", "Helvetica Neue", "Arial"]
        else:
            preferred = ["Noto Sans CJK SC", "WenQuanYi Micro Hei", "Ubuntu", "Arial"]
        chosen = next((f for f in preferred if f in families), "Arial")
        QApplication.setFont(QFont(chosen, 9))

    # ------------------------------------------------------------------
    # 主题切换
    # ------------------------------------------------------------------

    def _on_theme_changed(self, theme_id: str):
        """主题切换时，先设置主题颜色，再重新应用所有控件的样式。"""
        # 切换全局主题颜色
        style.set_theme(theme_id)
        # 各控件自己的apply_theme会读取最新的get_colors()
        self.search_bar.apply_theme()
        self.filter_bar.apply_theme()
        self.stats_bar.apply_theme()
        self.port_table.apply_theme()
        self.top_bar.apply_theme()
        self.status_bar.apply_theme()
        # 刷新分隔线颜色
        for child in self.findChildren(QFrame):
            if child.frameShape() == QFrame.HLine:
                child.setStyleSheet(f"color: {style.get_colors().border};")
        # 刷新表格数据重新渲染颜色
        if self._displayed_ports:
            self.port_table.set_ports(self._displayed_ports)

    # ------------------------------------------------------------------
    # 扫描服务回调
    # ------------------------------------------------------------------

    def _on_scan_started(self):
        """扫描开始。"""
        self.status_bar.show_message("⏳ 正在扫描端口...")

    def _on_scan_finished(self, elapsed: float, count: int):
        """扫描完成。"""
        self.status_bar.show_message(f"✅ 加载成功: {count} 个端口")
        self.stats_bar.set_last_scan_time(self.scan_service.last_scan_time_str)
        self.stats_bar.update_stats(self.scan_service.get_statistics(self._displayed_ports))
        self.top_bar.set_port_count(count)

    def _on_scan_error(self, error_msg: str):
        """扫描出错。"""
        self.status_bar.show_message(f"❌ 扫描失败: {error_msg.splitlines()[0]}")

    def _on_ports_updated(self, ports: List[PortInfo]):
        """扫描结果更新，刷新表格和统计。"""
        # 应用当前的搜索和筛选条件
        self._apply_filters_and_refresh()

    # ------------------------------------------------------------------
    # 搜索/筛选
    # ------------------------------------------------------------------

    def _on_search(self, keyword: str):
        """搜索按钮或回车。"""
        self._apply_filters_and_refresh()

    def _on_filter_changed(self):
        """筛选条件变化。"""
        self._apply_filters_and_refresh()

    def _on_clear_filter(self):
        """清除筛选。"""
        self.search_bar.clear_search()
        self._apply_filters_and_refresh()

    def _apply_filters_and_refresh(self):
        """根据当前搜索框和筛选栏条件，过滤端口列表并刷新表格。"""
        all_ports = self.scan_service.get_cached_ports()

        # 搜索
        keyword = self.search_bar.search_input.text().strip()
        filtered = self.scan_service.search_ports(keyword, all_ports)

        # 筛选
        filters = self.filter_bar.get_filters()
        filtered = self.scan_service.filter_ports(
            port_type=filters.get("port_type", "全部"),
            process_type=filters.get("process_type", "全部"),
            protocol=filters.get("protocol", "全部"),
            dev_only=filters.get("dev_only", False),
            common_port=filters.get("common_port"),
            ports=filtered
        )

        self._displayed_ports = filtered
        self.port_table.set_ports(filtered)
        self.stats_bar.update_stats(self.scan_service.get_statistics(filtered))
        # 顶部显示当前筛选后的端口数，总端口数在扫描完成时更新
        self.top_bar.set_port_count(len(filtered))
        self.stats_bar.set_last_scan_time(self.scan_service.last_scan_time_str)
        # 更新状态栏消息：显示当前结果数
        if len(filtered) == 0:
            if keyword or filters.get("common_port") or filters.get("port_type") != "全部" \
                    or filters.get("process_type") != "全部" or filters.get("protocol") != "全部" \
                    or filters.get("dev_only"):
                self.status_bar.show_message(f"🔍 筛选结果：0 个端口")
            else:
                self.status_bar.show_message(f"✅ 加载成功: {len(all_ports)} 个端口")
        else:
            if len(filtered) == len(all_ports) and not keyword:
                self.status_bar.show_message(f"✅ 加载成功: {len(all_ports)} 个端口")
            else:
                self.status_bar.show_message(f"🔍 显示 {len(filtered)} / {len(all_ports)} 个端口")

    # ------------------------------------------------------------------
    # 刷新/自动刷新
    # ------------------------------------------------------------------

    def _on_refresh_clicked(self):
        """手动刷新按钮。"""
        self.scan_service.trigger_scan()

    def _on_auto_refresh_toggled(self, enabled: bool):
        """自动刷新开关切换，实际控制scan_service的定时器。"""
        if enabled:
            self.scan_service.start_auto_refresh()
        else:
            self.scan_service.stop_auto_refresh()
        self.status_bar.set_auto_refresh(enabled)

    # ------------------------------------------------------------------
    # 选中行变化 / 批量关闭
    # ------------------------------------------------------------------

    def _on_selection_changed(self, count: int):
        """勾选行数变化，更新批量关闭按钮显示。"""
        self.search_bar.set_batch_count(count)

    def _on_kill_single(self, port_info: PortInfo):
        """点击单条「关闭」按钮。"""
        self._show_kill_confirm_dialog([port_info])

    def _on_batch_kill(self):
        """批量关闭按钮。"""
        checked = self.port_table.get_checked_ports()
        if not checked:
            return
        self._show_kill_confirm_dialog(checked)

    # ------------------------------------------------------------------
    # 关闭进程确认对话框（核心交互）
    # ------------------------------------------------------------------

    def _show_kill_confirm_dialog(self, ports: List[PortInfo]):
        """
        关闭进程确认对话框。
        - 数据库/SYSTEM/WEB_SERVER类型进程显示红色警告
        - 如果是系统服务，显示「永久停止服务」选项
        """
        is_batch = len(ports) > 1
        title = "确认批量关闭" if is_batch else "确认关闭端口"

        # 检测危险进程
        dangerous_types = {"DATABASE", "WEB_SERVER", "SYSTEM"}
        dangerous = [p for p in ports if p.process_type in dangerous_types or p.port_type == "DATABASE"]

        # 检测系统服务（第一个即可，批量时检测所有）
        has_service = False
        service_name = None
        if not is_batch:
            service_name = self.process_service.get_service_name_for_pid(ports[0].pid)
            has_service = service_name is not None
        else:
            for p in ports:
                sn = self.process_service.get_service_name_for_pid(p.pid)
                if sn:
                    has_service = True
                    break

        # 构建消息文本
        msg_lines = []
        if is_batch:
            msg_lines.append(f"确定要关闭选中的 <b>{len(ports)}</b> 个端口进程吗？")
            msg_lines.append("")
            for p in ports[:8]:  # 最多显示8个
                msg_lines.append(f"  • 端口 {p.port} ({p.process_name}, PID: {p.pid})")
            if len(ports) > 8:
                msg_lines.append(f"  • ... 还有 {len(ports) - 8} 个")
        else:
            p = ports[0]
            msg_lines.append(f"确定要关闭端口 <b>{p.port}</b> 的进程吗？")
            msg_lines.append("")
            msg_lines.append(f"  进程名: {p.process_name}")
            msg_lines.append(f"  PID: {p.pid}")
            msg_lines.append(f"  协议: {p.protocol}")
            if p.command_line:
                cmd_short = p.command_line[:80] + ("..." if len(p.command_line) > 80 else "")
                msg_lines.append(f"  命令行: {cmd_short}")

        # 危险警告
        if dangerous:
            msg_lines.append("")
            msg_lines.append('<span style="color: #e74c3c; font-weight: bold;">'
                           '⚠️ 警告：选中进程包含数据库/系统服务/Web服务器，'
                           '关闭后相关服务将不可用！</span>')

        # 永久停止服务选项
        permanent_stop = False
        if has_service:
            msg_lines.append("")
            msg_lines.append(f'<span style="color: #e67e22;">'
                           f'🔧 检测到这是系统服务（{service_name or "多个服务"}），'
                           f'勾选下方选项可同时禁用开机自启。</span>')

        msg_text = "<br>".join(msg_lines)

        # 创建对话框
        box = QMessageBox(self)
        box.setWindowTitle(title)
        box.setTextFormat(Qt.RichText)
        box.setText(msg_text)
        box.setIcon(QMessageBox.Warning if dangerous else QMessageBox.Question)

        btn_kill = box.addButton("临时关闭进程", QMessageBox.AcceptRole)
        btn_cancel = box.addButton("取消", QMessageBox.RejectRole)

        # 如果是系统服务，添加永久停止按钮
        btn_permanent = None
        if has_service:
            btn_permanent = box.addButton("永久停止服务并禁用自启", QMessageBox.DestructiveRole)
            btn_permanent.setStyleSheet(style.BTN_DANGER_STYLE())

        box.exec_()
        clicked = box.clickedButton()

        if clicked == btn_cancel:
            return

        permanent_stop = (clicked == btn_permanent)

        # 执行关闭操作
        self._execute_kill(ports, permanent_stop)

    def _execute_kill(self, ports: List[PortInfo], permanent: bool):
        """
        执行进程关闭操作。
        :param ports: 要关闭的端口列表
        :param permanent: 是否永久停止（系统服务）
        """
        success_count = 0
        fail_msgs = []
        service_results = []

        for p in ports:
            if permanent:
                # 永久停止系统服务
                ok, msg, svc_name = self.process_service.stop_service_permanently(p.pid)
                if ok:
                    success_count += 1
                    service_results.append(f"端口 {p.port} ({p.process_name}): {msg}")
                else:
                    # 如果永久停止失败（不是服务），回退到普通kill
                    kill_ok, kill_msg = self.process_service.kill_process(p.pid)
                    if kill_ok:
                        success_count += 1
                    else:
                        fail_msgs.append(f"端口 {p.port}: {msg} / {kill_msg}")
            else:
                # 普通kill进程
                ok, msg = self.process_service.kill_process(p.pid)
                if ok:
                    success_count += 1
                else:
                    fail_msgs.append(f"端口 {p.port} (PID {p.pid}): {msg}")

        # 显示结果
        total = len(ports)
        if success_count == total:
            if permanent:
                result_text = f"✅ 已永久停止 {success_count} 个服务并禁用自启"
            else:
                result_text = f"✅ 成功关闭 {success_count} 个进程"
            self.status_bar.show_message(result_text)
        elif success_count > 0:
            self.status_bar.show_message(f"⚠️ 成功关闭 {success_count}/{total} 个进程，{len(fail_msgs)} 个失败")
        else:
            self.status_bar.show_message(f"❌ 关闭失败: {fail_msgs[0] if fail_msgs else '未知错误'}")

        # 2秒后自动刷新（给系统时间停止进程）
        self._refresh_after_kill_timer.start()
