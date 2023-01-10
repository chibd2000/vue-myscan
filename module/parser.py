from models import DomainTask


def task_command_parser(domain_task: DomainTask):
    command_list = ['batch.py']

    if isinstance(domain_task.target, str):
        command_list.append('-d')
        command_list.append(domain_task.target)

    if isinstance(domain_task.is_ksubdomain, int) and domain_task.is_ksubdomain:
        command_list.append('-k')

    if isinstance(domain_task.is_websearch, int) and domain_task.is_websearch:
        command_list.append('-ws')

    if isinstance(domain_task.is_servicescan, int) and domain_task.is_servicescan:
        command_list.append('-ss')

    if isinstance(domain_task.is_webscan, int) and domain_task.is_webscan:
        command_list.append('-cs')
        if isinstance(domain_task.web_poc_scan_type, str):
            command_list.append('-fn')
            command_list.append(domain_task.web_poc_scan_type)

    if isinstance(domain_task.is_portscan, int) and domain_task.is_portscan:
        command_list.append('-p')
        command_list.append(domain_task.port_scan_content)

    if isinstance(domain_task.proxy, str) and domain_task.proxy is not None:
        command_list.append('-x')
        command_list.append(domain_task.proxy)

    if isinstance(domain_task.domain_id, str):
        command_list.append('-tf')
        command_list.append(domain_task.domain_id)

    return command_list


def verify_command_parser(domain_task: DomainTask, verify_type, verify_space, poc=None):
    command_list = ['batch.py']

    # python3 batch.py -fs "title=\"系统管理\"" -cs -m exploit.a.b,exploit.c.d -fn attack

    if verify_type == 'space':
        if isinstance(domain_task.target, str):
            if verify_space == 'fofa':
                command_list.append('-fs')
                command_list.append(domain_task.target)

    elif verify_type == 'ip':
        if isinstance(domain_task.target, str):
            command_list.append('-i')
            command_list.append(domain_task.target)

        if isinstance(domain_task.is_portscan, int) and domain_task.is_portscan:
            command_list.append('-p')
            command_list.append(domain_task.port_scan_content)

        if isinstance(domain_task.is_servicescan, int) and domain_task.is_servicescan:
            command_list.append('-ss')

    if isinstance(domain_task.is_webscan, int) and domain_task.is_webscan:
        command_list.append('-cs')

        if isinstance(poc, str) and poc:
            command_list.append('-m')
            command_list.append(poc)

        if isinstance(domain_task.web_poc_scan_type, str):
            command_list.append('-fn')
            command_list.append(domain_task.web_poc_scan_type)

    if isinstance(domain_task.proxy, str) and domain_task.proxy is not None:
        command_list.append('-x')
        command_list.append(domain_task.proxy)

    if isinstance(domain_task.domain_id, str):
        command_list.append('-tf')
        command_list.append(domain_task.domain_id)

    return command_list
