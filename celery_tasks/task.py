from celery_tasks.main import cel
import subprocess
import sys


@cel.task
def scan_verify(command: list) -> str:
    command.insert(0, sys.executable)
    print(command)
    subprocess.run(command, cwd='./client')
    return "ok"


@cel.task
def scan_task(command: list) -> str:
    command.insert(0, sys.executable)
    print(command)
    subprocess.run(command, cwd='./client')
    return "ok"


@cel.task
def scan_xray(web_list) -> str:
    print('scan_xray...')
    return "ok"
