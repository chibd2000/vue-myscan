
from flask import request
from flask_jwt_extended import jwt_required
from sqlalchemy import distinct

from extension import db
from models import DomainSubdomain
from views.MyscanResource import MyscanResource


class ExportSubDomain(MyscanResource):

    @jwt_required()
    def post(self):
        export_data = ''''''
        domain_id_list = request.json.get('domain_id_list', [])
        for domain_id in domain_id_list:
            datas = DomainSubdomain.export_subdomain_by_domainid(domain_id)
            for _ in datas:
                try:
                    export_data += _.subdomain + '\n'
                except Exception:
                    pass
        return self.send_file('subdomain', export_data)

