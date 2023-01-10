from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with
from models import MailConfig
from views.MyscanResource import MyscanResource


class Settings(MyscanResource):

    setgings_fields = {
        'wake_type': fields.String,
        'is_show': fields.Integer
    }

    resource_fields = {
        'status': fields.Boolean,
        'total': fields.Integer,
        'settings': fields.Nested(setgings_fields),
    }

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self):
        setting = MailConfig.query.first()
        data = {'wake_type': setting.wake_type, 'is_show': setting.is_show}
        return {'status': True, 'settings': data}

    @jwt_required()
    def post(self):
        args = self.get_parser()
        mail_config = MailConfig()
        mail_config.wake_type = args.wake_type if args.wake_type else ''
        mail_config.is_show = args.is_show if args.is_show else 0
        count = MailConfig.query.count()
        if count == 1:
            MailConfig.update_config(1, mail_config)
            MailConfig.query.session.commit()
            return {'status': True}
        elif count == 0:
            MailConfig.add_config(mail_config)
            MailConfig.query.session.commit()
            return {'status': True}
        else:
            return {'status': False}
