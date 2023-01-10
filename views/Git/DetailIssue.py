from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from models import DomainAsn, GithubIssue
from views.MyscanResource import MyscanResource


class DetailIssue(MyscanResource):
    issue_fields = {'issue_id': fields.Integer, 'monitor_id': fields.String,
                    'issue_url': fields.String, 'issue_create_user': fields.String,
                    'issue_create_date': fields.Integer, 'issue_status': fields.String, 'issue_level': fields.Integer,
                    'issue_title': fields.String, 'issue_body': fields.String,
                    'issue_type': fields.String}

    resource_fields = {
        'status': fields.Boolean,
        'total': fields.Integer,
        'issues': fields.List(fields.Nested(issue_fields)),
        'page_num': fields.Integer
    }

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self, search_type, current_monitor_id, page_num, page_size, query):
        if request.method == 'GET':
            detail_issue = GithubIssue.query.filter_by(monitor_id=current_monitor_id).order_by(
                GithubIssue.issue_create_date.desc())
            total = len(detail_issue.all())
            detail_issue_data = detail_issue.paginate(page=int(page_num), per_page=int(page_size), error_out=False,
                                                      max_per_page=150).items
            data = [{'issue_id': issue.issue_id, 'monitor_id': issue.monitor_id, 'issue_url': issue.issue_url,
                     'issue_create_user': issue.issue_create_user,
                     'issue_create_date': issue.issue_create_date, 'issue_status': issue.issue_status,
                     'issue_level': issue.issue_level, 'issue_title': issue.issue_title,
                     'issue_body': issue.issue_body, 'issue_type': issue.type} for issue in detail_issue_data]
            return {'status': True, 'total': total, 'issues': data, 'page_num': 1}

    @jwt_required()
    def post(self):
        if request.method == 'POST':
            args = self.get_parser()
            if GithubIssue.update_visited(args.monitor_id):
                return {'status': True}
            else:
                return {'status': False}
