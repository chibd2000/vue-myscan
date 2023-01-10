from utils.conf_reader import get_celery_conf
from datetime import timedelta
from celery import Celery
from celery_tasks.config import CeleryConfig, BROKER
from kombu import Queue, Exchange

# 任务执行：celery -A celery_tasks.main worker -l info -c 1

# 定时任务：celery -A celery_tasks.main beat -l info

broker = BROKER
# backend = 'redis://127.0.0.1:6379/2' backend=backend 不需要用到检查结果
task_list = ['celery_tasks.task', 'celery_tasks.github', 'celery_tasks.mail']

# redis分区
cel = Celery('celery_myscan', broker=broker, include=task_list)

cel.config_from_object(CeleryConfig)

cel.autodiscover_tasks(["celery_tasks.task", "celery_tasks.mail", "celery_tasks.github"])

task_queues = (
    Queue('default', exchange=Exchange('default'), routing_key='default'),
    Queue('task_queue', exchange=Exchange('task_queue'), routing_key='task_queue'),
)

task_routes = {
    'celery_tasks.task.scan_verify': {'queue': 'task_task', 'routing_key': 'task_task'},
    'celery_tasks.task.scan_task': {'queue': 'task_task', 'routing_key': 'task_task'},
}

# https://www.celerycn.io/yong-hu-zhi-nan/ding-qi-ren-wu-periodic-tasks
# github commit monitor
cel.conf.beat_schedule = {
    'add-commit-monitor-task': {
        'task': 'celery_tasks.github.commit_all_monitor',
        'schedule': timedelta(seconds=get_celery_conf()['schedule']),
        # 'schedule': crontab(hour=8, day_of_week=1),  # 每周一早八点
        'args': (),
    },
    'add-issue-monitor-task': {
        'task': 'celery_tasks.github.issue_all_monitor',
        'schedule': timedelta(seconds=get_celery_conf()['schedule']),
        # 'schedule': crontab(hour=8, day_of_week=1),  # 每周一早八点
        'args': (),
    }
}

# celery -A proj beat -s /home/celery/var/run/celerybeat-schedule

if __name__ == '__main__':
    cel.start()
