from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from models import DomainSimilar
from views.MyscanResource import MyscanResource


class DetailSimilar(MyscanResource):
    similar_fields = {
        'id': fields.Integer,
        'similar': fields.String
    }

    resource_fields = {
        'status': fields.Boolean,
        'total': fields.Integer,
        'similars': fields.List(fields.Nested(similar_fields)),
        'page_num': fields.Integer
    }

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self, search_type, current_domain_id, page_num, page_size, query):
        if request.method == 'GET':
            detail_similar = DomainSimilar.query.filter_by(domain_id=current_domain_id)
            total = len(detail_similar.all())
            detail_similar_data = detail_similar.paginate(page=int(page_num), per_page=int(page_size), error_out=False,
                                                          max_per_page=150).items
            index = ((page_num - 1) * page_size) + 1
            data = []
            for similar in detail_similar_data:
                data.append({'id': index, 'similar': similar.similar.split(",")})
                index += 1

            return {'status': True, 'total': total, 'similars': data, 'page_num': 1}
