from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from models import DomainWebspace
from views.MyscanResource import MyscanResource


class DetailWebspace(MyscanResource):

    webspace_fields = {
        'id': fields.Integer,
        'spider': fields.String,
        'subdomain': fields.String,
        'title': fields.String,
        'ip_port': fields.String,
        'domain': fields.String,
        'web_service': fields.String,
        'port_service': fields.String,
        'asn': fields.Integer,
        'search_keyword': fields.String
    }

    resource_fields = {
        'status': fields.Boolean,
        'datas': fields.List(fields.Nested(webspace_fields)),
        'total': fields.Integer,
        'page_num': fields.Integer,
        'page_size': fields.Integer,
    }

    @marshal_with(resource_fields)
    @jwt_required()
    def get(self, detail_type, search_type, current_domain_id, page_num, page_size, query):
        if request.method == 'GET':
            if query == 'null':
                detail_webspace = DomainWebspace.query.filter_by(domain_id=current_domain_id, spider=detail_type)
            else:
                if search_type == 'title':
                    detail_webspace = DomainWebspace.query.filter_by(domain_id=current_domain_id,
                                                                     spider=detail_type).filter(
                        DomainWebspace.title.like("%" + query + "%"))
                elif search_type == 'ip_port':
                    query = query.replace('_', '.')
                    detail_webspace = DomainWebspace.query.filter_by(domain_id=current_domain_id,
                                                                     spider=detail_type).filter(
                        DomainWebspace.ip_port.like("%" + query + "%"))
                elif search_type == 'web_service':
                    detail_webspace = DomainWebspace.query.filter_by(domain_id=current_domain_id,
                                                                     spider=detail_type).filter(
                        DomainWebspace.web_service.like("%" + query + "%"))
            total = len(detail_webspace.all())
            detail_webspace_data = detail_webspace.paginate(page=int(page_num), per_page=int(page_size),
                                                            error_out=False, max_per_page=150).items
            index = ((page_num - 1) * page_size) + 1
            data = []
            for fofa in detail_webspace_data:
                data.append({'id': index, 'spider': fofa.spider, 'subdomain': fofa.subdomain, 'title': fofa.title,
                             'ip_port': fofa.ip_port,
                             'domain': fofa.domain, 'web_service': fofa.web_service, 'port_service': fofa.port_service,
                             'asn': fofa.asn, 'search_keyword': fofa.search_keyword})
                index += 1

            return {'status': True, 'total': total, 'datas': data, 'page_num': 1}
            # return jsonify(status=True, total=total, datas=data, page_num=1)
