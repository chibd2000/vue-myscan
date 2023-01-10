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


class Task(MyscanResource):
    poc_fields = {
        'label': fields.String,
        'children': fields.String
    }

    resource_fields = {
        'status': fields.Boolean,
        'total': fields.Integer,
        'pocs': fields.List(fields.Nested(poc_fields)),
    }

    @jwt_required()
    def get(self, search_type, page_num, page_size, query):
        if request.method == 'GET':
            if query == 'null':
                domain_task = DomainTask.query.filter_by(is_verify=0)
            else:
                if search_type == 'domainid':
                    domain_task = DomainTask.query.filter_by(is_verify=0).filter(
                        DomainTask.domain_id.like("%" + query + "%"))
                elif search_type == 'name':
                    domain_task = DomainTask.query.filter_by(is_verify=0).filter(
                        DomainTask.name.like("%" + query + "%"))
                elif search_type == 'target':
                    domain_task = DomainTask.query.filter_by(is_verify=0).filter(
                        DomainTask.target.like("%" + query + "%"))
                elif search_type == 'status':
                    domain_task = DomainTask.query.filter_by(is_verify=0).filter_by(status=int(query))
            total = len(domain_task.all())
            domain_task_data = domain_task.paginate(page=int(page_num), per_page=int(page_size), error_out=False,
                                                    max_per_page=150).items
            data = [
                {'domain_id': task.domain_id,
                 'target': task.target,
                 'name': task.name,
                 'create_time': task.create_time,
                 'is_ksubdomain': task.is_ksubdomain,
                 'is_portscan': task.is_portscan,
                 'is_webscan': task.is_webscan,
                 'is_servicescan': task.is_servicescan,
                 'is_websearch': task.is_websearch,
                 'status': task.status,
                 'module_status': task.module_status,
                 'scanning_start_time': task.scanning_start_time,
                 'scanning_end_time': task.scanning_end_time,
                 'delete_status': task.delete_status,
                 'is_verify': task.is_verify} for task in domain_task_data]
            return jsonify(status=True, total=total, tasks=data, page_num=1)

    @jwt_required()
    def post(self):
        if request.method == 'POST':
            args = self.get_parser()
            domain_task = DomainTask()
            domain_task.domain_id = get_random_md5()[0:31]
            domain_task.target = args.task_target
            domain_task.name = args.task_name
            domain_task.status = 0
            domain_task.create_time = int(datetime.now().timestamp())
            domain_task.delete_status = 0
            domain_task.scanning_start_time = 0
            domain_task.scanning_end_time = 0
            domain_task.is_verify = False
            # 默认存在端口扫描，默认扫描格式为top100
            domain_task.is_portscan = True
            domain_task.port_scan_content = args.task_port_content if args.task_port_content else 'top100'
            # 下面是四个功能选择
            domain_task.is_ksubdomain = True if args.task_ksubdomain else False
            domain_task.is_websearch = True if args.task_websearch else False
            domain_task.is_servicescan = True if args.task_service else False
            domain_task.is_webscan = True if args.task_web else False
            # web_scan_type
            domain_task.web_poc_scan_type = args.task_web_poc_type if args.task_web_poc_type else 'attack'
            # proxy
            domain_task.proxy = args.task_proxy if args.task_proxy else None
            # add domain_task
            if DomainTask.add_task(domain_task):
                scan_task.apply_async(args=(task_command_parser(domain_task),), queue='task_queue')
                return jsonify(status=True)
            else:
                return jsonify(status=False)

    @jwt_required()
    def delete(self):
        if request.method == 'DELETE':
            delete_domain_id_list = eval(request.data.decode())
            for domain_id in delete_domain_id_list:
                DomainTask.delete_task_by_domainid(domain_id)
            return jsonify(status=True)
