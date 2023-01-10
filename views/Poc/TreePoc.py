from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from models import DomainPoc
from views.MyscanResource import MyscanResource


class Poc(MyscanResource):

    poc_fields = {
        'id': fields.Integer,
        'label': fields.String
    }

    resource_fields = {
        'status': fields.Boolean,
        'total': fields.Integer,
        'pocs': fields.List(fields.Nested(poc_fields)),
    }

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self, query):
        if query == 'null':
            poc_data = DomainPoc.query
            total = len(DomainPoc.query.all())
        else:
            poc_data = DomainPoc.query.filter_by(name=query)
            total = len(DomainPoc.query.filter_by(name=query).all())

        data = []
        for poc in poc_data:
            is_not_repeat = True
            is_not_has_parent = True
            for index, _ in enumerate(data):
                if _['label'] and poc.parent.lower() == _['label'].lower():
                    is_not_has_parent = False
                    for child in _['children']:
                        if child['id'] == poc.id:
                            is_not_repeat = False
                            break
                    if is_not_repeat:
                        data[index]['children'].append(
                            {'id': poc.id, 'label': poc.parent.lower() + '_' + poc.name.lower()})
            if is_not_has_parent:
                data.append({'label': poc.parent.lower(), 'children': [{'id': poc.id, 'label': poc.parent.lower() + '_' + poc.name.lower()}]})
        return {'status': True, 'total': total, 'pocs': data}

    @jwt_required()
    def post(self):
        f = request.files['file']
        f.save('/tmp/test.txt')
        return {'status': True}