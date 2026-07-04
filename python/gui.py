#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 设置任务栏中的图标显示
import ctypes
import os
import signal
import sys

my_app_id = "my_port_manager"
# windows 特有：设置任务栏图标
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
except AttributeError:
    pass # 非Windows平台跳过
