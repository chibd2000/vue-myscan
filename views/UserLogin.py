from datetime import timedelta

from flask import jsonify, current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from models import DomainUser
from views.MyscanResource import MyscanResource


class UserLogin(MyscanResource):
    def post(self):
        args = self.get_parser()
        if args.username is not None and \
                args.username != '' and \
                args.password is not None and \
                args.password != '':
            current_user = DomainUser.find_by_username(args.username)
            if current_user is not None and args.password == current_user.password:
                access_jwt_expire = current_app.config.get('ACCESS_TOKEN_EXPIRE_MINUTES')
                access_token_expires = timedelta(minutes=access_jwt_expire)
                access_token = create_access_token(identity=args.username, expires_delta=access_token_expires)
                refresh_token = create_refresh_token(identity=args.username)
                return jsonify(access_token=access_token, refresh_token=refresh_token, status=True,
                               message='Logged in as {}'.format(current_user.username))
            else:
                return jsonify(status=False, message='username / password is incorrect')
