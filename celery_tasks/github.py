
from celery_tasks.mail import send_mail
from celery_tasks.main import cel
from module.data import gLogger
from module.githubmonitor import GithubCommitMonitor, GithubIssuePrMonitor

import asyncio


# https://api.github.com/search/commits?q=committer-date:%3E2022-12-01+repo:top-think/framework

def run_async(coro):
    return asyncio.run(coro)


@cel.task(soft_time_limit=60)
def commit_monitor(monitor_id):
    try:
        monitor_data = run_async(GithubCommitMonitor().monitor(monitor_id))
        data = ''''''
        for monitor in monitor_data:
            if monitor:
                data += monitor
        if data:
            send_mail.delay(data)
    except Exception as e:
        gLogger.myscan_error(e.__str__())
    return 'ok'


@cel.task(soft_time_limit=240)
def commit_all_monitor():
    try:
        monitor_data_list = run_async(GithubCommitMonitor().all_monitor())
        data = ''''''
        for monitor_data in monitor_data_list:
            for monitor in monitor_data:
                if monitor:
                    data += monitor
        if data:
            send_mail.delay(data)
    except Exception as e:
        gLogger.myscan_error(e.__str__())
    return 'ok'


@cel.task(soft_time_limit=60)
def issue_monitor(monitor_id):
    try:
        monitor_data = run_async(GithubIssuePrMonitor().monitor(monitor_id))
        data = ''''''
        for monitor in monitor_data:
            if monitor:
                data += monitor
        if data:
            send_mail.delay(data)
    except Exception as e:
        gLogger.myscan_error(e.__str__())
    return 'ok'


@cel.task(soft_time_limit=240)
def issue_all_monitor():
    try:
        monitor_data_list = run_async(GithubIssuePrMonitor().all_monitor())
        data = ''''''
        for monitor_data in monitor_data_list:
            for monitor in monitor_data:
                if monitor:
                    data += monitor
        if data:
            send_mail.delay(data)
    except Exception as e:
        gLogger.myscan_error(e.__str__())
    return 'ok'
