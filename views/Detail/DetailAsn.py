from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from models import DomainAsn
from views.MyscanResource import MyscanResource


class DetailAsn(MyscanResource):

    ans_fields = {
        'id': fields.Integer,
        'asn': fields.Integer
    }

    resource_fields = {
        'status': fields.Boolean,
        'total': fields.Integer,
        'asns': fields.List(fields.Nested(ans_fields)),
        'page_num': fields.Integer
    }

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self, search_type, current_domain_id, page_num, page_size, query):
        if request.method == 'GET':
            detail_asn = DomainAsn.query.filter_by(domain_id=current_domain_id).order_by(DomainAsn.asn)
            total = len(detail_asn.all())
            detail_asn_data = detail_asn.paginate(page=int(page_num), per_page=int(page_size), error_out=False,
                                                  max_per_page=150).items
            index = ((page_num - 1) * page_size) + 1
            data = []
            for asn in detail_asn_data:
                data.append({'id': index, 'asn': asn.asn})
                index += 1

            return {'status': True, 'total': total, 'asns': data, 'page_num': 1}