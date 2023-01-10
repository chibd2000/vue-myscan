import celery

from module.constant import TASK_STATUS
from models import DomainTask
from flask import Flask

from module.database import GithubDB


# after_return：在任务执行返回后交给 worker 执行
# on_failure：在任务执行失败后交给 worker 执行
# on_retry：在任务进行重试是交给 worker 执行
# on_success：在任务执行成功后交给 worker 执行

class BaseTask(celery.Task):

    app = Flask(__name__)

    def before_start(self, task_id, args, kwargs):
        print(args, kwargs)
        with self.app.app_context():
            DomainTask.update_status(task_id, 2)
            DomainTask.update_start_time(task_id)

    def on_success(self, retval, task_id, args, kwargs):
        with self.app.app_context():
            DomainTask.update_end_time(task_id)
            DomainTask.update_status(task_id, TASK_STATUS.SUCCESS)
            return super(BaseTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        with self.app.app_context():
            DomainTask.update_end_time(task_id)
            DomainTask.update_status(task_id, TASK_STATUS.FAIL)
            return super(BaseTask, self).on_failure(exc, task_id, args, kwargs, einfo)


class BaseGit(celery.Task):

    def before_start(self, task_id, args, kwargs):
        print(task_id, args, kwargs)
        # db_conf = {'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'pass': 'Chiling.123', 'db': 'myscan'}
        # self.db_conn = GithubDB(db_conf)
        # self.db_conn.update_last_update_time()

    def on_success(self, retval, task_id, args, kwargs):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


