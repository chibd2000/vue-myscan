from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with
from sqlalchemy import desc

from models import DomainCseg
from views.MyscanResource import MyscanResource


class DetailCseg(MyscanResource):

    cseg_fields = {
        'id': fields.Integer,
        'ip_segment': fields.String,
        'ips': fields.List(fields.String),
        'num': fields.Integer
    }

    resource_fields = {
        'status': fields.Boolean,
        'total': fields.Integer,
        'csegs': fields.List(fields.Nested(cseg_fields)),
        'page_num': fields.Integer
    }

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self, search_type, current_domain_id, page_num, page_size, query):
        if request.method == 'GET':
            if query == 'null':
                detail_cseg = DomainCseg.query.filter_by(domain_id=current_domain_id).order_by(desc(DomainCseg.num))
            total = len(detail_cseg.all())
            detail_cseg_data = detail_cseg.paginate(page=int(page_num), per_page=int(page_size), error_out=False,
                                                    max_per_page=150).items
            index = ((page_num - 1) * page_size) + 1
            data = []
            for cseg in detail_cseg_data:
                data.append({'id': index, 'ip_segment': cseg.ip_segment, 'ips': cseg.ips.split(","), 'num': cseg.num})
                index += 1

            return {'status': True, 'total': total, 'csegs': data, 'page_num': 1}
