class ProcessInfo:
    """
    进程信息
    """
    def __init__(self):
        self.pid = None
        self.process_name = None
        self.process_path = None
        self.command_line = None
        self.is_development_process = False
        self.start_time = None
        self.user = None
