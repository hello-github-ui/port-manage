class PortInfo:
    """
    端口信息
    """
    
    def __init__(self):
        self.port = None
        self.protocol = None
        self.status = None
        self.pid = None
        self.process_name = None
        self.process_path = None
        self.command_line = None
        self.is_development_process = False
        self.start_time = None
        self.user = None
        self.local_address = None
        self.remote_address = None
        self.port_type = None
        self.process_type = None
