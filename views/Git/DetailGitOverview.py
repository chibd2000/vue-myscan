from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from models import GithubCommit, GithubIssue
from views.MyscanResource import MyscanResource


class DetailGitOverview(MyscanResource):
    detail_fields = {
        'commit': fields.Integer,
        'issue': fields.Integer,
    }

    resource_fields = {
        'status': fields.Boolean,
        'counts': fields.Nested(detail_fields),
    }

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self, current_monitor_id):
        if request.method == 'GET':
            commit = GithubCommit.query.filter_by(monitor_id=current_monitor_id).count()
            issue = GithubIssue.query.filter_by(monitor_id=current_monitor_id).count()
            data = {'commit': commit, 'issue': issue}
            return {'status': True, 'counts': data}