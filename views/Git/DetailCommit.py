from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from models import DomainAsn, GithubCommit
from views.MyscanResource import MyscanResource


class DetailCommit(MyscanResource):
    commit_fields = {'commit_sha': fields.String, 'monitor_id': fields.String,
                     'commit_url': fields.String, 'commit_message': fields.String,
                     'commit_author_name': fields.String, 'commit_author_date': fields.Integer,
                     'commit_committer_name': fields.String, 'commit_committer_date': fields.Integer,
                     'commit_branch': fields.String, 'commit_level': fields.Integer}

    resource_fields = {
        'status': fields.Boolean,
        'total': fields.Integer,
        'commits': fields.List(fields.Nested(commit_fields)),
        'page_num': fields.Integer
    }

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self, search_type, current_monitor_id, page_num, page_size, query):
        if request.method == 'GET':
            detail_commit = GithubCommit.query.filter_by(monitor_id=current_monitor_id).order_by(GithubCommit.commit_author_date.desc())
            total = len(detail_commit.all())
            detail_commit_data = detail_commit.paginate(page=int(page_num), per_page=int(page_size), error_out=False, max_per_page=150).items
            data = [{'commit_sha': commit.commit_sha, 'monitor_id': commit.monitor_id, 'commit_url': commit.commit_url,
                     'commit_message': commit.commit_message, 'commit_author_name': commit.commit_author_name,
                     'commit_author_date': commit.commit_author_date,
                     'commit_committer_name': commit.commit_committer_name,
                     'commit_committer_date': commit.commit_committer_date, 'commit_branch': commit.commit_branch,
                     'commit_level': commit.commit_level} for commit in detail_commit_data]
            return {'status': True, 'total': total, 'issues': data, 'page_num': 1}

    @jwt_required()
    def post(self):
        if request.method == 'POST':
            args = self.get_parser()
            if GithubCommit.update_visited(args.monitor_id):
                return {'status': True}
            else:
                return {'status': False}
