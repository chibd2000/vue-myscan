from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from models import DomainWebtitle
from views.MyscanResource import MyscanResource

class SearchWebsite(MyscanResource):
    @jwt_required()
    def get(self, search_type, page_num, page_size, query):
        if request.method == 'GET':
            if query == 'null':
                detail_website = DomainWebtitle.query.filter_by()
            else:
                if search_type == 'url':
                    detail_website = DomainWebtitle.query.filter(DomainWebtitle.url.like("%" + query + "%"))
                elif search_type == 'title':
                    detail_website = DomainWebtitle.query.filter(DomainWebtitle.title.like("%" + query + "%"))
                elif search_type == 'status':
                    detail_website = DomainWebtitle.query.filter_by(status=int(query))
                elif search_type == 'header':
                    detail_website = DomainWebtitle.query.filter(DomainWebtitle.header.like("%" + query + "%"))
            total = len(detail_website.all())
            detail_website_data = detail_website.paginate(page=int(page_num), per_page=int(page_size), error_out=False,
                                                          max_per_page=150).items
            index = ((page_num - 1) * page_size) + 1
            data = []
            for website in detail_website_data:
                data.append({'id': index, 'url': website.url, 'status': website.status, 'title': website.title,
                             'header': website.header})
                index += 1

            return jsonify(status=True, total=total, websites=data, page_num=1)
