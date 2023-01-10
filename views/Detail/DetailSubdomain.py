from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from models import DomainSubdomain
from views.MyscanResource import MyscanResource


class DetailSubdomain(MyscanResource):
    subdomain_fields = {
        'id': fields.Integer,
        'subdomain': fields.String,
        'resolve_type': fields.String,
        'ip': fields.String,
    }

    resource_fields = {
        'status': fields.Boolean,
        'total': fields.Integer,
        'subdomains': fields.List(fields.Nested(subdomain_fields)),
        'page_num': fields.Integer
    }

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self, search_type, current_domain_id, page_num, page_size, query):
        if request.method == 'GET':
            if query == 'null':
                detail_subdomain = DomainSubdomain.query.filter_by(domain_id=current_domain_id)
            else:
                if search_type == 'subdomain':
                    detail_subdomain = DomainSubdomain.query.filter_by(domain_id=current_domain_id, subdomain=query)
                elif search_type == 'ip':
                    detail_subdomain = DomainSubdomain.query.filter_by(domain_id=current_domain_id, ip=query)

            total = len(detail_subdomain.all())
            detail_subdomain_data = detail_subdomain.paginate(page=int(page_num), per_page=int(page_size),
                                                              error_out=False, max_per_page=150).items
            index = ((page_num - 1) * page_size) + 1
            data = []
            for subdomain in detail_subdomain_data:
                data.append({'id': index, 'subdomain': subdomain.subdomain, 'resolve_type': subdomain.resolve_type,
                             'ip': subdomain.ip})
                index += 1
            return {'status': True, 'total': total, 'subdomains': data, 'page_num': 1}
