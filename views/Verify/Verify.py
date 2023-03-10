from datetime import datetime
from celery_tasks.task import scan_verify
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from models import DomainTask, DomainPoc
from module.parser import verify_command_parser
from utils.common import get_random_md5
from views.MyscanResource import MyscanResource
import sys

if sys.version >= '3.8':
    import multiprocessing as mp
    mp.set_start_method('fork')


class Verify(MyscanResource):
    @jwt_required()
    def get(self, search_type, page_num, page_size, query):
        if request.method == 'GET':
            if query == 'null':
                domain_verify_task = DomainTask.query.filter_by(is_verify=1)
            else:
                if search_type == 'domainid':
                    domain_verify_task = DomainTask.query.filter_by(is_verify=1).filter(DomainTask.domain_id.like("%" + query + "%"))
                elif search_type == 'name':
                    domain_verify_task = DomainTask.query.filter_by(is_verify=1).filter(DomainTask.name.like("%" + query + "%"))
            total = len(domain_verify_task.all())
            domain_task_data = domain_verify_task.paginate(page=int(page_num), per_page=int(page_size), error_out=False, max_per_page=150).items
            data = [
                {'domain_id': task.domain_id, 'domain': task.target, 'name': task.name,
                 'create_time': task.create_time, 'is_portscan': task.is_portscan,
                 'is_webscan': task.is_webscan, 'is_servicescan': task.is_servicescan,
                 'status': task.status, 'module_status': task.module_status,
                 'scanning_start_time': task.scanning_start_time, 'scanning_end_time': task.scanning_end_time,
                 'delete_status': task.delete_status} for task in domain_task_data]
            return jsonify(status=True, total=total, verifys=data, page_num=1)

    @jwt_required()
    def post(self):
        if request.method == 'POST':
            args = self.get_parser()
            domain_task = DomainTask()
            domain_task.domain_id = get_random_md5()[0:31]
            domain_task.target = args.task_target
            domain_task.name = args.task_name
            domain_task.status = 0
            domain_task.delete_status = 0
            domain_task.create_time = int(datetime.now().timestamp())
            domain_task.scanning_start_time = 0
            domain_task.scanning_end_time = 0
            domain_task.is_verify = True
            # ????????????????????????????????????????????????top100
            domain_task.is_portscan = True if args.task_port else False
            domain_task.port_scan_content = args.task_port_content if args.task_port_content else 'top100'
            # ???????????????????????????
            domain_task.is_webscan = True if args.task_web else False
            domain_task.is_servicescan = True if args.task_service else False
            # web_scan_type
            poc = DomainPoc.get_poc_by_id(args.task_web_poc) if args.task_web_poc != 'all_poc' else None
            domain_task.web_poc_scan_type = args.task_web_poc_type if args.task_web_poc_type else 'attack'
            # proxy
            domain_task.proxy = args.task_proxy if args.task_proxy else None
            # verify_type
            verify_type = args.task_verify_type
            # verify_space
            verify_space = args.task_verify_space
            # add domain_task
            if DomainTask.add_task(domain_task):
                scan_verify.apply_async(args=(verify_command_parser(domain_task, verify_type, verify_space, poc),), queue='task_queue')
                return jsonify(status=True)
            else:
                return jsonify(status=False)

    @jwt_required()
    def delete(self, domain_id):
        if request.method == 'DELETE':
            if DomainTask.delete_task_by_domainid(domain_id):
                return jsonify(status=True)
            else:
                return jsonify(status=False)
