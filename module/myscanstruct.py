class MyscanCommand:
    def __init__(self, domain, ksubdomain_scan, web_search, port_scan, web_scan, web_scan_type, service_scan, proxy,
                 space_scan, poc_type, thread_num):
        self.domain = domain
        self.ksubdomain_scan = ksubdomain_scan
        self.web_search = web_search
        self.port_scan = port_scan
        self.web_scan = web_scan
        self.web_scan_type = web_scan_type
        self.service_scan = service_scan
        self.proxy = proxy
        self.space_scan = space_scan
        self.poc_type = poc_type
        self.thread_num = thread_num


class MyscanParser:

    # python3 batch.py -d zjhu.edu.cn -k -ws -cs -ss -x http://127.0.0.1:7890 -fn exec

    def __init__(self, myscan_command):
        self._command_list = list()
        self._command_list.append('python3')
        self._command_list.append('batch.py')
        if isinstance(myscan_command.domain, str):
            self._command_list.append('-d')
            self._command_list.append(myscan_command.domain)
        if isinstance(myscan_command.ksubdomain_scan, bool) and myscan_command.ksubdomain_scan:
            self._command_list.append('-k')
        if isinstance(myscan_command.web_search, bool) and myscan_command.web_search:
            self._command_list.append('-ws')
        if isinstance(myscan_command.port_scan, str):
            self._command_list.append('-p')
            self._command_list.append(myscan_command.port_scan)
        if isinstance(myscan_command.web_scan, bool) and myscan_command.web_scan:
            self._command_list.append('-cs')
        if isinstance(myscan_command.service_scan, bool) and myscan_command.service_scan:
            self._command_list.append('-ss')
        if isinstance(myscan_command.web_scan_type, str):
            self._command_list.append('-fn')
            self._command_list.append(myscan_command.web_scan_type)
        if isinstance(myscan_command.proxy, str):
            self._command_list.append('-x')
            self._command_list.append(myscan_command.proxy)

    @property
    def get_command_list(self) -> list:
        return self._command_list if self._command_list else exit(0)


class MyscanTaskParser(MyscanParser):
    pass


class MyscanVerifyParser(MyscanParser):
    pass
