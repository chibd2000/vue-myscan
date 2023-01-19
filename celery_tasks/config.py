BROKER = 'redis://myscan_redis:6379/1'


class CeleryConfig:
    enable_utc = False
    timezone = 'Asia/Shanghai'
    worker_max_tasks_per_child = 100
