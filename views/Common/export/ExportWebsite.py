from io import BytesIO
from ipaddress import ip_address

from flask import Response, request
from flask_jwt_extended import jwt_required
from models import DomainWebtitle
from views.MyscanResource import MyscanResource


class ExportWebsite(MyscanResource):

    @jwt_required()
    def post(self):
        export_data = ''''''
        domain_id_list = request.json.get('domain_id_list', [])
        for domain_id in domain_id_list:
            datas = DomainWebtitle.export_website_by_domainid(domain_id)
            for _ in datas:
                try:
                    export_data += _.url + '\n'
                except Exception:
                    pass
        return self.send_file('website', export_data)
