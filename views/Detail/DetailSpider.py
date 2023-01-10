from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from models import DomainWebspace, DomainSpider
from views.MyscanResource import MyscanResource

class DetailSpider(MyscanResource):

    spider_fields = {
        'id': fields.Integer,
        'keyword': fields.String,
        'url': fields.String,
        'title': fields.String,
        'type': fields.String,
    }

    resource_fields = {
        'status': fields.Boolean,
        'total': fields.Integer,
        'spiders': fields.List(fields.Nested(spider_fields)),
        'page_num': fields.Integer
    }

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self, search_type, current_domain_id, page_num, page_size, query):
        if request.method == 'GET':
            if query == 'null':
                detail_spider = DomainSpider.query.filter_by(domain_id=current_domain_id)
            else:
                if search_type == 'keyword':
                    detail_spider = DomainSpider.query.filter_by(domain_id=current_domain_id, keyword=query)
                elif search_type == 'title':
                    detail_spider = DomainSpider.query.filter_by(domain_id=current_domain_id).filter(
                        DomainSpider.title.like("%" + query + "%"))

            total = len(detail_spider.all())
            detail_spider_data = detail_spider.paginate(page=int(page_num), per_page=int(page_size), error_out=False,
                                                        max_per_page=150).items
            index = ((page_num - 1) * page_size) + 1
            data = []
            for spider in detail_spider_data:
                data.append({'id': index, 'keyword': spider.keyword, 'url': spider.url, 'title': spider.title,
                             'type': spider.type})
                index += 1

            return {'status': True, 'total': total, 'spiders': data, 'page_num': 1}
