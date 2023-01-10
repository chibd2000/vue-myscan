from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from models import DomainPoc
from views.MyscanResource import MyscanResource


class Poc(MyscanResource):

    poc_fields = {
        'id': fields.Integer,
        'parent': fields.String,
        'name': fields.String,
        'type': fields.String,
        'number': fields.String,
        'info': fields.String,
    }

    resource_fields = {
        'status': fields.Boolean,
        'pocs': fields.List(fields.Nested(poc_fields)),
        'page_num': fields.Integer,
        'total': fields.Integer
    }

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self, page_num, page_size):
        domain_poc = DomainPoc.query.order_by(DomainPoc.parent)
        total = len(domain_poc.all())
        domain_poc_data = domain_poc.paginate(page=int(page_num), per_page=int(page_size), error_out=False, max_per_page=150).items
        index = ((page_num - 1) * page_size) + 1
        data = []
        for poc in domain_poc_data:
            data.append({'id': index, 'parent': poc.parent, 'name': poc.name, 'type': poc.type, 'number': poc.number,
                         'info': poc.info})
            index += 1
        return {'status': True, 'total': total, 'pocs': data, 'page_num': 1}

