from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from models import DomainService, DomainWebtitle, DomainSubdomain, DomainIp, DomainBeian, DomainWebspace, DomainCseg, \
    DomainAsn, DomainSimilar, DomainVuln
from views.MyscanResource import MyscanResource


class DetailOverview(MyscanResource):
    detail_fields = {
        'webtitle': fields.Integer,
        'subdomain': fields.Integer,
        'ip': fields.Integer,
        'beian': fields.Integer,
        'webspace': fields.Integer,
        'service': fields.Integer,
        'cseg': fields.Integer,
        'asn': fields.Integer,
        'similar': fields.Integer,
        'vuln': fields.Integer,
    }

    resource_fields = {
        'status': fields.Boolean,
        'counts': fields.Nested(detail_fields),
    }

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self, current_domain_id):
        if request.method == 'GET':
            webtitle = DomainWebtitle.query.filter_by(domain_id=current_domain_id).count()
            subdomain = DomainSubdomain.query.filter_by(domain_id=current_domain_id).count()
            ip = DomainIp.query.filter_by(domain_id=current_domain_id).count()
            beian = DomainBeian.query.filter_by(domain_id=current_domain_id).count()
            webspace = DomainWebspace.query.filter_by(domain_id=current_domain_id).count()
            service = DomainService.query.filter_by(domain_id=current_domain_id).count()
            cseg = DomainCseg.query.filter_by(domain_id=current_domain_id).count()
            asn = DomainAsn.query.filter_by(domain_id=current_domain_id).count()
            similar = DomainSimilar.query.filter_by(domain_id=current_domain_id).count()
            vuln = DomainVuln.query.filter_by(domain_id=current_domain_id).count()
            data = {'webtitle': webtitle, 'subdomain':subdomain, 'ip':ip, 'beian':beian, 'webspace':webspace,
                    'service': service, 'cseg': cseg, 'asn': asn, 'similar': similar, 'vuln': vuln}
            return {'status': True, 'counts': data}
