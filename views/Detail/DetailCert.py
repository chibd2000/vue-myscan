from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from models import DomainCert
from views.MyscanResource import MyscanResource


class DetailCert(MyscanResource):
    cert_fields = {
        'id': fields.Integer,
        'cert': fields.String,
        'subdomain': fields.String
    }

    resource_fields = {
        'status': fields.Boolean,
        'total': fields.Integer,
        'certs': fields.List(fields.Nested(cert_fields)),
        'page_num': fields.Integer
    }

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self, search_type, current_domain_id, page_num, page_size, query):
        if request.method == 'GET':
            if query == 'null':
                detail_cert = DomainCert.query.filter_by(domain_id=current_domain_id)
            else:
                if search_type == 'license':
                    detail_cert = DomainCert.query.filter_by(domain_id=current_domain_id).filter_by(license=query)
            total = len(detail_cert.all())
            detail_cert_data = detail_cert.paginate(page=int(page_num), per_page=int(page_size), error_out=False,
                                                    max_per_page=30).items
            index = ((page_num - 1) * page_size) + 1
            data = []
            for cert in detail_cert_data:
                data.append({'id': index, 'certs': cert.cert, 'subdomain': cert.subdomain})
                index += 1
            return jsonify(status=True, total=total, certs=data, page_num=1)
