# Port Manage v2 🚀

<div align="center">

**跨平台桌面端口管理工具 | 支持 Windows / macOS / Linux**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://pypi.org/project/PyQt5/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](#)

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [打包发布](#-打包发布) • [技术架构](#-技术架构)

</div>

---

## 📖 项目简介

Port Manage v2 是一个基于 **Python + PyQt5** 开发的跨平台桌面端口管理工具，帮助开发者快速查看、管理本地端口占用情况。无需浏览器，双击即可使用，支持一键关闭进程、批量操作、永久停止系统服务等功能。

> **v2 重构说明**：从原 Java Spring Boot Web 版本重构为原生桌面应用，启动更快、界面更流畅、无需安装Java环境、不占用Web端口。

### 🎯 核心优势

- ⚡ **原生桌面应用** - 双击启动，无需浏览器，秒开
- 🖥️ **跨平台支持** - 完美支持 Windows / macOS / Linux
- 🎨 **5种主题配色** - 浅色、深色、蓝色、绿色、紫色，护眼舒适
- 🧠 **智能识别** - 自动识别进程类型（数据库、Web服务器、开发工具等）
- 💪 **功能强大** - 单个关闭、批量关闭、永久停止系统服务
- 🔍 **多维筛选** - 端口类型、进程类型、协议、开发进程、常用端口
- 🔄 **自动刷新** - 5秒自动扫描，支持暂停/继续
- 🚫 **零依赖运行** - 打包后单文件/单目录可执行，无需Python环境

---

## ✨ 功能特性

### 核心功能

| 功能 | 说明 |
|------|------|
| 📊 **实时端口扫描** | 后台线程扫描所有监听端口，不阻塞UI |
| 🔍 **快速搜索** | 支持端口号、进程名、PID、命令行搜索，回车即搜，一键清空 |
| 🎯 **多维筛选** | 端口类型/进程类型/协议(TCP/UDP)/开发进程/常用端口 |
| ❌ **一键关闭** | 点击关闭按钮，危险进程红色警告提示 |
| 📦 **批量关闭** | 全选/多选端口，一次性批量关闭 |
| 🛑 **永久停止** | 自动识别系统服务，支持永久停止并禁用开机自启 |
| ⏸️ **自动刷新控制** | 5秒自动刷新，支持暂停/继续切换 |
| 🎨 **主题切换** | 5种配色主题实时切换，无白色边框卡片 |
| ☑️ **全选复选框** | 两态全选（全选/取消全选），完美对齐 |
| 📈 **实时统计** | 总端口数/开发进程/TCP/UDP实时统计 |

### 智能进程识别

自动识别以下进程类型并标记：
- **数据库**: MySQL, Redis, PostgreSQL, MongoDB, SQL Server 等
- **Web服务器**: Nginx, Apache, Tomcat, IIS 等
- **开发工具**: Node.js, Python, Java, Go, Rust 等开发服务
- **IDE**: VSCode, PyCharm, IntelliJ IDEA, WebStorm 等
- **浏览器**: Chrome, Firefox, Edge, Safari 等
- **系统进程**: svchost, System, launchd 等系统关键进程

### 跨平台进程管理

| 平台 | 临时关闭 | 永久停止系统服务 |
|------|---------|----------------|
| **Windows** | `taskkill /F /PID` | `sc stop` + `sc config` + PowerShell `Get-CimInstance` |
| **macOS** | `kill -9` | `brew services stop` + `launchctl unload` |
| **Linux** | `kill -9` | `systemctl stop` + `systemctl disable` |

---

## 🚀 快速开始

### 方式一：下载发布包（推荐普通用户）

1. 从 [Releases](https://github.com/hello-github-ui/port-manage/releases) 下载对应平台的发布包
2. 解压后直接运行可执行文件：
   - **Windows**: 双击 `PortManager.exe`
   - **macOS**: 双击 `PortManager.app`（首次运行右键→打开）
   - **Linux**: 运行 `./PortManager`

### 方式二：从源码运行（开发者）

#### 环境要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows 10+, macOS 10.15+, Linux (Ubuntu 18.04+ 等)

#### 安装依赖

```bash
# 克隆项目
git clone https://github.com/hello-github-ui/port-manage.git
cd port-manage

# 安装依赖
pip install -r requirements.txt
```

#### 运行应用

```bash
# 方式1：根目录入口（推荐，和打包入口一致）
python PortManager.py

# 方式2：模块方式运行
python -m v2.main

# 方式3：直接运行v2目录下入口
python v2/main.py
```

启动后即可看到端口管理工具主界面。

---

## 📦 打包发布

使用 **PyInstaller** 将Python应用打包为各平台原生可执行文件。

### 通用准备工作

**重要：必须在目标操作系统上打包对应平台的版本！** PyInstaller不支持交叉编译（例如不能在Windows上打包macOS版本）。

```bash
# 1. 确保安装了最新依赖
pip install -r requirements.txt
pip install pyinstaller>=6.0.0

# 2. 验证应用可以正常运行（两种方式都可以）
python PortManager.py
# 或者：python -m v2.main
```

---

### Windows 打包

**重要**：使用项目根目录下的 `PortManager.py` 作为入口，不要使用 `v2/main.py`，否则会出现模块找不到错误。

#### 打包为单目录（推荐，启动快）

```powershell
# 在项目根目录执行
pyinstaller --name "PortManager" \
    --windowed \
    --icon "v2/icon.ico" \
    --add-data "v2/icon.ico;v2/" \
    --clean \
    --noconfirm \
    PortManager.py
```

打包完成后，产物在 `dist/PortManager/` 目录下，整个目录压缩为 `PortManager-Windows-x64.zip` 即可发布。

#### 打包为单文件（分发方便，启动稍慢）

```powershell
pyinstaller --name "PortManager"  \
	--onefile  \
	--windowed  \
	--icon "v2/icon.ico"  \
	--add-data "v2/icon.ico;v2/"  \
	--clean  \
	--noconfirm  \
	PortManager.py
```

产物为 `dist/PortManager.exe` 单文件，直接压缩发布即可。

---

### macOS 打包

#### 准备工作

```bash
# 如果没有图标，先生成 .icns 图标（可选，或直接使用icon.ico）
# 确保安装了 pyinstaller
pip install pyinstaller
```

#### 打包为 .app（单目录）

```bash
pyinstaller --name "PortManager" \
    --windowed \
    --icon "v2/icon.ico" \
    --add-data "v2/icon.ico:v2/" \
    --clean \
    --noconfirm \
    PortManager.py
```

打包完成后，产物在 `dist/PortManager.app`，压缩为 `PortManager-macOS-x64.zip` 发布。

> **注意**：macOS 用户首次打开可能提示"无法验证开发者"，解决方法：
> 1. 右键点击 `PortManager.app` → 选择「打开」
> 2. 或在终端执行：`xattr -cr /Applications/PortManager.app`

---

### Linux 打包

#### 打包为单目录

```bash
pyinstaller --name "PortManager" \
    --windowed \
    --icon "v2/icon.ico" \
    --add-data "v2/icon.ico:v2/" \
    --clean \
    --noconfirm \
    PortManager.py
```

打包完成后产物在 `dist/PortManager/` 目录，运行入口为 `dist/PortManager/PortManager`。可以创建桌面快捷方式或压缩为 `PortManager-Linux-x64.tar.gz` 发布。

```bash
# 赋予执行权限
chmod +x dist/PortManager/PortManager

# 压缩发布
cd dist
tar -czf ../PortManager-Linux-x64.tar.gz PortManager/
cd ..
```

---

### PyInstaller 常用参数说明

| 参数 | 说明 |
|------|------|
| `--name "PortManager"` | 输出的应用名称 |
| `--windowed` / `-w` | GUI程序，不显示控制台黑窗口（Windows/macOS） |
| `--onefile` / `-F` | 打包为单个可执行文件（不指定则为单目录） |
| `--icon <path>` | 设置应用图标 |
| `--add-data "源;目标"` | 添加数据文件（Windows用`;`分隔，macOS/Linux用`:`分隔） |
| `--clean` | 打包前清理临时文件 |
| `--noconfirm` | 覆盖输出目录不询问 |
| `--debug all` | 调试用，显示控制台输出（排查打包问题时使用） |

---

### 🤖 GitHub Actions 自动构建（可选）

如果需要配置CI自动构建，可以创建 `.github/workflows/build.yml`，在三个平台分别打包：

```yaml
name: Build Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: |
          pyinstaller --name "PortManager" --windowed --icon "v2/icon.ico" \
            --add-data "v2/icon.ico;v2/" --clean --noconfirm PortManager.py
      - uses: actions/upload-artifact@v4
        with:
          name: PortManager-Windows
          path: dist/PortManager/

  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: |
          pyinstaller --name "PortManager" --windowed --icon "v2/icon.ico" \
            --add-data "v2/icon.ico:v2/" --clean --noconfirm PortManager.py
      - uses: actions/upload-artifact@v4
        with:
          name: PortManager-macOS
          path: dist/PortManager.app

  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: |
          sudo apt-get update && sudo apt-get install -y libxcb-xinerama0 libxcb-cursor0
          pip install -r requirements.txt
      - run: |
          pyinstaller --name "PortManager" --windowed --icon "v2/icon.ico" \
            --add-data "v2/icon.ico:v2/" --clean --noconfirm PortManager.py
      - uses: actions/upload-artifact@v4
        with:
          name: PortManager-Linux
          path: dist/PortManager/
```

手动上传发布时，只需在本地对应平台打包，将生成的 `dist` 目录压缩后上传到 GitHub Releases 即可。

---

## 🏗️ 技术架构

### 分层架构设计

```
v2/
├── main.py                 # 应用入口（QApplication初始化、图标设置）
├── icon.ico                # 应用图标
├── config/
│   └── settings.py         # 配置常量（常用端口、端口范围等）
├── model/
│   ├── port_info.py        # PortInfo数据模型
│   └── process_info.py     # ProcessInfo数据模型
├── scanner/                # 端口扫描层（平台相关）
│   ├── port_scanner.py     # 扫描器抽象基类
│   ├── scanner_factory.py  # 扫描器工厂（自动选择当前平台实现）
│   ├── windows_scanner.py  # Windows: netstat + tasklist + PowerShell
│   └── mac_scanner.py      # macOS/Linux: lsof + ps
├── service/                # 业务服务层
│   ├── scan_service.py     # 扫描服务（缓存、自动刷新、搜索、筛选、统计）
│   ├── scan_worker.py      # QThread后台扫描线程（不阻塞UI）
│   └── process_service.py  # 进程管理服务（kill、批量kill、系统服务停止）
├── utils/
│   ├── cmd_util.py         # 跨平台命令执行工具（编码处理、隐藏窗口）
│   └── port_type_identifier.py  # 进程/端口类型智能识别
└── ui/                     # UI表现层
    ├── style.py            # 主题配色系统（5种主题QSS）
    ├── main_window.py      # 主窗口（信号槽连接、业务逻辑对接）
    └── widgets/            # 独立UI控件
        ├── top_bar.py      # 顶部栏（标题、平台标识、主题切换）
        ├── search_bar.py   # 搜索栏（搜索框、刷新、暂停自动刷新、批量关闭）
        ├── filter_bar.py   # 筛选栏（5个筛选下拉框）
        ├── stats_bar.py    # 统计栏（端口数统计、上次扫描时间）
        ├── port_table.py   # 端口表格（自定义复选框表头、居中复选框）
        └── status_bar.py   # 状态栏（操作反馈、自动刷新状态）
```

### 核心技术栈

- **GUI框架**: PyQt5 5.15+
- **后端扫描**: 系统原生命令调用
  - Windows: `netstat -ano` + `tasklist` + PowerShell `Get-CimInstance`
  - macOS/Linux: `lsof -nP -iTCP -sTCP:LISTEN` + `lsof -nP -iUDP` + `ps -eo`
- **多线程**: QThread 后台扫描，pyqtSignal 信号通知UI更新
- **打包工具**: PyInstaller 6.0+
- **缓存设计**: 桌面场景使用简单内存List，后台扫描完成全量替换，无需复杂并发缓存

---

## 📱 使用说明

### 基本操作

1. **启动应用**：双击启动后自动开始首次扫描
2. **搜索端口**：在搜索框输入端口号/进程名/PID，按回车搜索，点击×清空恢复显示全部
3. **筛选**：使用筛选栏下拉框按条件筛选端口
4. **关闭单个进程**：点击对应行右侧红色「关闭」按钮
5. **批量关闭**：勾选多个端口（或点左上角全选），点击顶部「关闭选中」按钮
6. **永久停止服务**：关闭系统服务进程时，对话框会显示「永久停止服务并禁用自启」选项
7. **自动刷新**：默认5秒自动刷新，点击「暂停/继续自动刷新」按钮控制
8. **切换主题**：右上角主题下拉框，支持浅色/深色/蓝色/绿色/紫色5种主题

### 典型使用场景

| 场景 | 操作 |
|------|------|
| 清理开发环境 | 筛选「开发进程: 是」→ 全选 → 批量关闭 |
| 释放占用端口 | 搜索端口号 → 查看占用进程 → 关闭 |
| 停止数据库 | 筛选「进程类型: DATABASE」→ 选择目标 → 永久停止 |
| 查看TCP/UDP分布 | 统计栏实时显示TCP/UDP数量 |

---

## ❓ 常见问题

### Q1: 为什么Notepad++/记事本等程序没有显示？
**A**: 这是端口管理工具，只显示**正在监听/占用网络端口**的进程。普通文本编辑器等不监听网络端口的程序不会显示——这是正确的设计。

### Q2: 打包后运行提示缺少模块？
**A**: 可以尝试添加 `--hidden-import=模块名` 参数到PyInstaller命令，或使用 `--debug all` 参数运行查看具体缺失的模块。

### Q3: Windows打包后杀毒软件报毒？
**A**: PyInstaller打包的Python程序可能被误报，添加信任或使用代码签名证书即可。

### Q4: macOS提示"无法打开，因为无法验证开发者"？
**A**: 右键点击应用 → 选择「打开」，或在终端执行：`sudo xattr -cr /Applications/PortManager.app`。

### Q5: Linux下启动报错缺少xcb库？
**A**: 安装Qt运行依赖：`sudo apt-get install libxcb-xinerama0 libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxcb-xfixes0 libxcb-xkb1 libxkbcommon-x11-0`。

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

<div align="center">

Made with ❤️ using Python & PyQt5

</div>
