from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from models import DomainService
from views.MyscanResource import MyscanResource


class DetailService(MyscanResource):
    service_fields = {
        'id': fields.Integer,
        'ip': fields.String,
        'port': fields.Integer,
        'title': fields.String,
        'service': fields.String,
        'info': fields.String,
    }

    resource_fields = {
        'status': fields.Boolean,
        'total': fields.Integer,
        'services': fields.List(fields.Nested(service_fields)),
        'page_num': fields.Integer
    }

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self, search_type, current_domain_id, page_num, page_size, query):
        if request.method == 'GET':
            if query == 'null':
                detail_service = DomainService.query.filter_by(domain_id=current_domain_id)
            else:
                if search_type == 'ip':
                    detail_service = DomainService.query.filter_by(domain_id=current_domain_id, ip=query)
                elif search_type == 'port':
                    detail_service = DomainService.query.filter_by(domain_id=current_domain_id, port=int(query))

            total = len(detail_service.all())
            detail_ip_data = detail_service.paginate(page=int(page_num), per_page=int(page_size), error_out=False,
                                                     max_per_page=150).items
            index = ((page_num - 1) * page_size) + 1
            data = []
            for service in detail_ip_data:
                data.append({'id': index, 'ip': service.ip, 'port': service.port, 'title': service.title,
                             'service': service.service,
                             'info': service.info})
                index += 1

            return {'status': True, 'total': total, 'services': data, 'page_num': 1}
