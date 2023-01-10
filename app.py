from werkzeug.middleware.proxy_fix import ProxyFix

from flask import Flask
from flask_restful import Api
from extension import db, cors, jwt
from views.Common.export.ExportIp import ExportIp
from views.Common.export.ExportSubdomain import ExportSubDomain
from views.Common.export.ExportWebsite import ExportWebsite
from views.Detail.DetailOverview import DetailOverview
from views.Detail.DetailSimilar import DetailSimilar
from views.Git.DetailCommit import DetailCommit
from views.Git.DetailGitOverview import DetailGitOverview
from views.Git.DetailIssue import DetailIssue
from views.Git.Git import Git
from views.Menu.Menu import UserMenu
from views.Poc.Poc import Poc
from views.Poc.PocSync import PocSync
from views.Search.Ip import SearchIp
from views.Search.Subdomain import SearchSubdomain
from views.Search.Website import SearchWebsite
from views.Settings.Settings import Settings
from views.Task.Task import Task
from views.Task.TaskCount import TaskCount
from views.Task.TreePoc import TreePoc
from views.UserLogin import UserLogin
from views.Detail.DetailWebspace import DetailWebspace
from views.Detail.DetailCert import DetailCert

from views.Detail.DetailAsn import DetailAsn
from views.Detail.DetailBeian import DetailBeian
from views.Detail.DetailCseg import DetailCseg
from views.Detail.DetailIp import DetailIp
from views.Detail.DetailService import DetailService
from views.Detail.DetailSpider import DetailSpider
from views.Detail.DetailSubdomain import DetailSubdomain
from views.Detail.DetailVuln import DetailVuln
from views.Detail.DetailWebsite import DetailWebsite
from views.Verify.Verify import Verify

import os

myscan_app = Flask(__name__)
myscan_app.config.from_pyfile('settings.py')
myscan_app.config['FLASK_PATH'] = os.getcwd() + os.path.sep
myscan_app.config['POC_PATH'] = os.path.join(myscan_app.config['FLASK_PATH'], 'exploit/scripts/')

jwt.init_app(myscan_app)
db.init_app(myscan_app)
cors.init_app(myscan_app)
myscan_api = Api(myscan_app)

from cli import *
@myscan_app.cli.command()
def create():
    db.drop_all()
    db.create_all()
    DomainUser.init_data()

# login...
myscan_api.add_resource(UserLogin, '/login', endpoint='login_endpoint')
# menu...
myscan_api.add_resource(UserMenu, '/menu', endpoint='menu_endpoint')
# poc...
myscan_api.add_resource(Poc, '/poc/<int:page_num>/<int:page_size>', endpoint='poc_endpoint')
myscan_api.add_resource(PocSync, '/poc/sync', endpoint='poc_sync_endpoint')
myscan_api.add_resource(TreePoc, '/poc/treepoc/<string:query>', endpoint='task_treepoc_endpoint')
# git...
myscan_api.add_resource(Git, '/git', '/git/<string:post_type>', '/git/<string:search_type>/<int:page_num>/<int:page_size>/<string:query>', endpoint='git_endpoint')
myscan_api.add_resource(DetailCommit, '/gitdetail/commit', '/gitdetail/commit/<string:search_type>/<string:current_monitor_id>/<int:page_num>/<int:page_size>/<string:query>', endpoint='git_commit_endpoint')
myscan_api.add_resource(DetailIssue, '/gitdetail/issue', '/gitdetail/issue/<string:search_type>/<string:current_monitor_id>/<int:page_num>/<int:page_size>/<string:query>', endpoint='git_issue_endpoint')
myscan_api.add_resource(DetailGitOverview, '/gitdetail/overview/<string:current_monitor_id>', endpoint='git_overview_endpoint')
# search...
myscan_api.add_resource(SearchWebsite,
                        '/search/website/<string:search_type>/<int:page_num>/<int:page_size>/<string:query>',
                        endpoint='search_website_endpoint')
myscan_api.add_resource(SearchIp,
                        '/search/ip/<string:search_type>/<int:page_num>/<int:page_size>/<string:query>',
                        endpoint='search_ip_endpoint')
myscan_api.add_resource(SearchSubdomain,
                        '/search/subdomain/<string:search_type>/<int:page_num>/<int:page_size>/<string:query>',
                        endpoint='search_subdomain_endpoint')
# task...
myscan_api.add_resource(Task, '/task', '/task/<string:search_type>/<int:page_num>/<int:page_size>/<string:query>',
                        endpoint='task_endpoint')
myscan_api.add_resource(TaskCount, '/task/count/<string:search_type>',
                        endpoint='task_count_endpoint')
# settings...
myscan_api.add_resource(Settings, '/settings', endpoint='settings_endpoint')
# verify...
myscan_api.add_resource(Verify, '/verify', '/verify/<string:search_type>/<int:page_num>/<int:page_size>/<string:query>',
                        '/verify/<string:domain_id>', endpoint='verify_endpoint')
# detail...
myscan_api.add_resource(DetailOverview,
                        '/detail/overview/<string:current_domain_id>',
                        endpoint='detail_overview_endpoint')
myscan_api.add_resource(DetailWebsite,
                        '/detail/website/<string:search_type>/<string:current_domain_id>/<int:page_num>/<int:page_size>/<string:query>',
                        endpoint='detail_website_endpoint')
myscan_api.add_resource(DetailSubdomain,
                        '/detail/subdomain/<string:search_type>/<string:current_domain_id>/<int:page_num>/<int:page_size>/<string:query>',
                        endpoint='detail_subdomain_endpoint')
myscan_api.add_resource(DetailIp,
                        '/detail/ip/<string:search_type>/<string:current_domain_id>/<int:page_num>/<int:page_size>/<string:query>',
                        endpoint='detail_ip_endpoint')
myscan_api.add_resource(DetailVuln,
                        '/detail/vuln/<string:search_type>/<string:current_domain_id>/<int:page_num>/<int:page_size>/<string:query>',
                        endpoint='detail_vuln_endpoint')
myscan_api.add_resource(DetailBeian,
                        '/detail/beian/<string:search_type>/<string:current_domain_id>/<int:page_num>/<int:page_size>/<string:query>',
                        endpoint='detail_beian_endpoint')
myscan_api.add_resource(DetailService,
                        '/detail/service/<string:search_type>/<string:current_domain_id>/<int:page_num>/<int:page_size>/<string:query>',
                        endpoint='detail_service_endpoint')
myscan_api.add_resource(DetailSpider,
                        '/detail/spider/<string:search_type>/<string:current_domain_id>/<int:page_num>/<int:page_size>/<string:query>',
                        endpoint='detail_spider_endpoint')
myscan_api.add_resource(DetailCert,
                        '/detail/cert/<string:search_type>/<string:current_domain_id>/<int:page_num>/<int:page_size>/<string:query>',
                        endpoint='detail_cert_endpoint')
myscan_api.add_resource(DetailCseg,
                        '/detail/cseg/<string:search_type>/<string:current_domain_id>/<int:page_num>/<int:page_size>/<string:query>',
                        endpoint='detail_cseg_endpoint')
myscan_api.add_resource(DetailAsn,
                        '/detail/asn/<string:search_type>/<string:current_domain_id>/<int:page_num>/<int:page_size>/<string:query>',
                        endpoint='detail_asn_endpoint')
myscan_api.add_resource(DetailSimilar,
                        '/detail/similar/<string:search_type>/<string:current_domain_id>/<int:page_num>/<int:page_size>/<string:query>',
                        endpoint='detail_similar_endpoint')
# Webspace...
myscan_api.add_resource(DetailWebspace,
                        '/detail/webspace/<string:detail_type>/<string:search_type>/<string:current_domain_id>/<int:page_num>/<int:page_size>/<string:query>',
                        endpoint='detail_webspace_fofa_endpoint')
# Common...
myscan_api.add_resource(ExportIp, '/common/ip/<string:get_type>', endpoint='common_export_ip')
myscan_api.add_resource(ExportWebsite, '/common/website/export_website', endpoint='common_export_website')
myscan_api.add_resource(ExportSubDomain, '/common/subdomain/export_subdomain', endpoint='common_export_subdomain')

if __name__ == '__main__':
    # myscan_app.run()
    myscan_app.wsgi_app = ProxyFix(myscan_app.wsgi_app)
    myscan_app.run()