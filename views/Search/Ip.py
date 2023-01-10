from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with
from sqlalchemy import func

from models import DomainIp, DomainService
from views.MyscanResource import MyscanResource


class SearchIp(MyscanResource):

    ip_fields = {
        'id': fields.Integer,
        'ip': fields.String,
        'port': fields.List(fields.String),
        'ip2domain': fields.List(fields.String),
    }

    resource_fields = {
        'status': fields.Boolean,
        'total': fields.Integer,
        'ips': fields.List(fields.Nested(ip_fields)),
        'page_num': fields.Integer
    }

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self, search_type, page_num, page_size, query):
        if request.method == 'GET':
            if query == 'null':
                detail_ip = DomainIp.query.outerjoin(DomainService, DomainIp.ip == DomainService.ip).with_entities(
                    DomainIp.ip, func.group_concat(DomainService.port), DomainIp.ip2domain).group_by(DomainIp.ip)
            else:
                if search_type == 'ip':
                    detail_ip = DomainIp.query.outerjoin(DomainService, DomainIp.ip == DomainService.ip).with_entities(
                        DomainIp.ip, func.group_concat(DomainService.port), DomainIp.ip2domain).filter_by(ip=query).group_by(DomainIp.ip)

            total = len(detail_ip.all())
            detail_ip_data = detail_ip.paginate(page=int(page_num), per_page=int(page_size), error_out=False, max_per_page=150).items
            index = ((page_num - 1) * page_size) + 1
            data = []
            for ip in detail_ip_data:
                data.append({'id': index, 'ip': ip[0], 'port': ip[1].split(",") if ip[1] else ['-'], 'ip2domain': ip[2].split(",") if ip[2] else ['-']})
                index += 1
            return {'status': True, 'total': total, 'ips': data, 'page_num': 1}
