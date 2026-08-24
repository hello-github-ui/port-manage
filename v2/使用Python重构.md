> PyQt5 控件开发

## Qt Designer
安装该组件后，可以通过拖控件的方式来快速构建界面。

### 安装
```bash
pip install pyqt5-tools
```

## 代码结构
```text
v2/
├── main.py                      # 入口（sys.path 兜底 + 全局样式）
├── config/settings.py           # 配置层（扫描间隔/常用端口/开发关键字/端口集合）
├── model/                       # 数据模型层
│   ├── port_info.py             #   PortInfo（@dataclass，对应 Java PortInfo）
│   ├── process_info.py          #   ProcessInfo
│   └── table_model.py           #   PortTableModel（QAbstractTableModel，MVC）
├── scanner/                     # 扫描器层（占位 + 详细 TODO）
│   ├── port_scanner.py          #   抽象基类
│   ├── windows_scanner.py       #   Windows（netstat/tasklist 命令注释）
│   ├── mac_scanner.py           #   Mac（lsof 命令注释）
│   └── scanner_factory.py       #   工厂（platform 分流）
├── service/                     # 业务服务层
│   ├── scan_service.py          #   扫描/统计/搜索（当前返回模拟数据）
│   └── process_service.py       #   进程关闭（占位 + 命令注释）
├── utils/
│   ├── port_type_identifier.py  #   类型识别（占位 + 完整判定规则注释）
│   └── mock_util.py             #   9 条多类型模拟数据
└── ui/                          # UI 表现层
    ├── style.py                 #   全局 QSS（卡片/按钮/表格/滚动条）
    ├── main_window.py           #   主窗口（中介者，组装+信号槽+QTimer）
    └── widgets/                 #   6 个独立子控件，均用 pyqtSignal 解耦
        ├── top_bar.py           #   顶栏（标题/OS/端口数/主题切换）
        ├── search_bar.py        #   搜索栏（搜索/刷新/暂停/批量关闭）
        ├── filter_bar.py        #   筛选栏（5 下拉框，中文显示+枚举值）
        ├── stats_bar.py         #   统计栏
        ├── port_table.py        #   表格（表头全选+行内关闭按钮注入）
        └── status_bar.py        #   状态栏
```
设计要点
* 分层解耦：子控件只管界面与发信号，不互相引用；主窗口作为中介者协调 Service 层与各控件
* MVC：表格用 QAbstractTableModel 而非 QStandardItemModel，视图/数据分离
* 信号驱动：勾选、搜索、筛选、关闭均通过 pyqtSignal 上抛，业务逻辑集中在主窗口
* 占位数据：ScanService 当前返回模拟数据，接入真实扫描器后界面无需改动
* QTimer 自动刷新：每 5 秒刷新一次（对应 Java @Scheduled），可暂停