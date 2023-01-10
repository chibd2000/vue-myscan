from ipaddress import ip_address

from flask import request
from flask_jwt_extended import jwt_required
from models import DomainIp, DomainService
from views.MyscanResource import MyscanResource


class ExportIp(MyscanResource):

    @jwt_required()
    def post(self, get_type):
        export_data = ''''''
        domain_id_list = request.json.get('domain_id_list', [])
        for domain_id in domain_id_list:
            if get_type == 'export_private_ip':
                for _ in DomainIp.export_ip_by_domainid(domain_id):
                    try:
                        if ip_address(_.ip) and ip_address(_.ip).is_private:
                            export_data += _.ip + '\n'
                    except Exception:
                        pass
                return self.send_file('private_ip', export_data)
            elif get_type == 'export_ip_port':
                for _ in DomainService.export_ip_port_by_domainid(domain_id):
                    export_data += _.ip + ':' + str(_.port) + '\n'
                return self.send_file('ip_port', export_data)
            else:
                return 'null'
