import time

from flask import request
from flask_jwt_extended import jwt_required
from sqlalchemy import func, and_

from celery_tasks.github import commit_monitor, issue_monitor
from models import GithubTask, GithubCommit, GithubIssue
from utils.common import get_random_md5
from views.MyscanResource import MyscanResource


class Git(MyscanResource):

    @jwt_required()
    def get(self, search_type, page_num, page_size, query):
        if request.method == 'GET':
            if query == 'null':
                # select a.monitor_id,a.target,a.name,a.status,count(b.is_visited) not_visited,a.last_update_time, a.next_update_time,a.create_time from github_task a left join github_commit b on (a.monitor_id = b.monitor_id and b.is_visited = 0) group by monitor_id
                github_task = GithubTask.query.outerjoin(GithubCommit,
                                                    and_(GithubTask.monitor_id == GithubCommit.monitor_id,
                                                         GithubCommit.is_visited == 0)).with_entities(
                                                        GithubTask.monitor_id, GithubTask.target, GithubTask.name,
                                                        GithubTask.status, func.count(GithubCommit.is_visited),
                                                        GithubTask.last_update_time, GithubTask.next_update_time,
                                                        GithubTask.create_time).group_by(GithubTask.monitor_id)
            elif search_type == 'name':
                github_task = GithubTask.query.outerjoin(GithubCommit,
                                                    and_(GithubTask.monitor_id == GithubCommit.monitor_id,
                                                         GithubCommit.is_visited == 0)).with_entities(
                                                        GithubTask.monitor_id, GithubTask.target, GithubTask.name,
                                                        GithubTask.status, func.count(GithubCommit.is_visited),
                                                        GithubTask.last_update_time, GithubTask.next_update_time,
                                                        GithubTask.create_time).filter(GithubTask.name.like("%" + query + "%")).group_by(GithubTask.monitor_id)

            total = len(github_task.all())
            github_task_data = github_task.paginate(page=int(page_num), per_page=int(page_size), error_out=False,
                                                    max_per_page=150).items
            index = ((page_num - 1) * page_size) + 1
            data = []
            for task in github_task_data:
                data.append({'id': index, 'monitor_id': task[0], 'target': task[1], 'name': task[2],
                             'status': task[3], 'not_visited': task[4], 'last_update_time': task[5],
                             'next_update_time': task[6], 'create_time': task[7]})
                index += 1
            return {'status': True, 'total': total, 'gits': data, 'page_num': 1}

    @jwt_required()
    def post(self, post_type):
        if request.method == 'POST':
            args = self.get_parser()
            if post_type == 'singlemonitor':
                commit_monitor.delay(args.monitor_id)
                issue_monitor.delay(args.monitor_id)
                return {'status': True}
            elif post_type == 'allmonitor':
                github_task = GithubTask()
                github_task.monitor_id = get_random_md5()[0:31]
                github_task.target = args.task_target
                github_task.name = args.task_name
                github_task.status = 0
                github_task.create_time = time.time()
                github_task.not_visited = 0
                if GithubTask.add_task(github_task):
                    commit_monitor.delay(github_task.monitor_id)
                    issue_monitor.delay(github_task.monitor_id)
                    return {'status': True}
                else:
                    return {'status': False}

    @jwt_required()
    def delete(self):
        if request.method == 'DELETE':
            delete_domain_id_list = eval(request.data.decode())
            for domain_id in delete_domain_id_list:
                GithubTask.delete_task_by_mointorid(domain_id)
            return {'status': True}
