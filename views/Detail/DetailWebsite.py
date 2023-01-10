from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from models import DomainWebtitle
from views.MyscanResource import MyscanResource


class DetailWebsite(MyscanResource):
    subdomain_fields = {
        'id': fields.Integer,
        'url': fields.String,
        'status': fields.Integer,
        'title': fields.String,
        'header': fields.String
    }

    resource_fields = {
        'status': fields.Boolean,
        'total': fields.Integer,
        'websites': fields.List(fields.Nested(subdomain_fields)),
        'page_num': fields.Integer
    }

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self, search_type, current_domain_id, page_num, page_size, query):
        if request.method == 'GET':
            if query == 'null':
                detail_website = DomainWebtitle.query.filter_by(domain_id=current_domain_id)
            else:
                if search_type == 'url':
                    detail_website = DomainWebtitle.query.filter_by(domain_id=current_domain_id).filter(
                        DomainWebtitle.url.like("%" + query + "%"))
                elif search_type == 'title':
                    detail_website = DomainWebtitle.query.filter_by(domain_id=current_domain_id).filter(
                        DomainWebtitle.title.like("%" + query + "%"))
                elif search_type == 'status':
                    detail_website = DomainWebtitle.query.filter_by(domain_id=current_domain_id, status=int(query))
                elif search_type == 'header':
                    detail_website = DomainWebtitle.query.filter_by(domain_id=current_domain_id).filter(
                        DomainWebtitle.header.like("%" + query + "%"))
            total = len(detail_website.all())
            detail_website_data = detail_website.paginate(page=int(page_num), per_page=int(page_size), error_out=False,
                                                          max_per_page=150).items
            index = ((page_num - 1) * page_size) + 1
            data = []
            for website in detail_website_data:
                data.append({'id': index, 'url': website.url, 'status': website.status, 'title': website.title,
                             'header': website.header})
                index += 1
            return {'status': True, 'total': total, 'websites': data, 'page_num': 1}
