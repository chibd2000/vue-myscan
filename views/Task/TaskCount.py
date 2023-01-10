from flask_restful import fields

from celery_tasks.task import scan_task
from datetime import datetime
from flask import request, jsonify
from flask_jwt_extended import jwt_required

from models import DomainTask
from module.parser import task_command_parser
from utils.common import get_random_md5
from views.MyscanResource import MyscanResource
import sys

if sys.version >= '3.8':
    import multiprocessing as mp

    mp.set_start_method('fork')


class TaskCount(MyscanResource):

    resource_fields = {
        'status': fields.Boolean,
        'unfinished': fields.Integer,
        'finished': fields.Integer,
    }

    @jwt_required()
    def get(self, search_type):
        if search_type == 'scan':
            finished_count = DomainTask.query.filter_by(is_verify=0, status=1).count()
            total = DomainTask.query.filter_by(is_verify=0).count()
            return jsonify(status=True, finished=finished_count, all_total=total)
        elif search_type == 'verify':
            finished_count = DomainTask.query.filter_by(is_verify=1, status=1).count()
            total = DomainTask.query.filter_by(is_verify=1).count()
            return jsonify(status=True, finished=finished_count, all_total=total)
        return jsonify(status=False)
