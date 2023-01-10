
from celery_tasks.mail import send_mail
from celery_tasks.main import cel
from module.githubmonitor import GithubCommitMonitor, GithubIssuePrMonitor

import asyncio


# https://api.github.com/search/commits?q=committer-date:%3E2022-12-01+repo:top-think/framework

def run_async(coro):
    return asyncio.run(coro)


@cel.task
def commit_monitor(monitor_id):
    monitor_data = run_async(GithubCommitMonitor().monitor(monitor_id))
    data = ''''''
    for monitor in monitor_data:
        if monitor:
            print(monitor)
            data += monitor
    if data:
        send_mail.delay(data)
    return 'ok'


@cel.task
def commit_all_monitor():
    monitor_data_list = run_async(GithubCommitMonitor().all_monitor())
    data = ''''''
    for monitor_data in monitor_data_list:
        for monitor in monitor_data:
            if monitor:
                data += monitor
    if data:
        send_mail.delay(data)
    return 'ok'


@cel.task
def issue_monitor(monitor_id):
    monitor_data = run_async(GithubIssuePrMonitor().monitor(monitor_id))
    data = ''''''
    for monitor in monitor_data:
        if monitor:
            data += monitor
    if data:
        send_mail.delay(data)
    return 'ok'


@cel.task
def issue_all_monitor():
    monitor_data_list = run_async(GithubIssuePrMonitor().all_monitor())
    data = ''''''
    for monitor_data in monitor_data_list:
        for monitor in monitor_data:
            if monitor:
                data += monitor
    if data:
        send_mail.delay(data)
    return 'ok'
