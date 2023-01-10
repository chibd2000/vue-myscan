from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from models import DomainVuln
from views.MyscanResource import MyscanResource

class DetailVuln(MyscanResource):

    vuln_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'url': fields.String,
        'software': fields.String,
    }

    resource_fields = {
        'status': fields.Boolean,
        'total': fields.Integer,
        'vulns': fields.List(fields.Nested(vuln_fields)),
        'page_num': fields.Integer
    }

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self, search_type, current_domain_id, page_num, page_size, query):
        if request.method == 'GET':
            if query == 'null':
                detail_vuln = DomainVuln.query.filter_by(domain_id=current_domain_id)
            else:
                if search_type == 'name':
                    detail_vuln = DomainVuln.query.filter_by(domain_id=current_domain_id, name=query)
                elif search_type == 'url':
                    detail_vuln = DomainVuln.query.filter_by(domain_id=current_domain_id, url=query)
                elif search_type == 'software':
                    detail_vuln = DomainVuln.query.filter_by(domain_id=current_domain_id, software=query)

            total = len(detail_vuln.all())
            detail_vuln_data = detail_vuln.paginate(page=int(page_num), per_page=int(page_size), error_out=False,
                                                    max_per_page=150).items
            index = ((page_num - 1) * page_size) + 1
            data = []
            for vuln in detail_vuln_data:
                data.append({'id': index, 'name': vuln.name, 'url': vuln.url, 'software': vuln.software})
                index += 1

            return {'status': True, 'total': total, 'vulns': data, 'page_num': 1}

