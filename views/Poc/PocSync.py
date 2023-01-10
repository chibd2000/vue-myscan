import importlib
import os
import re

from flask import current_app
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from models import DomainPoc
from views.MyscanResource import MyscanResource


class PocSync(MyscanResource):
    resource_fields = {
        'status': fields.Boolean,
    }

    @jwt_required()
    @marshal_with(resource_fields)
    def get(self):

        if DomainPoc.clear_poc():
            flask_path = current_app.config.get('FLASK_PATH')
            poc_path = current_app.config.get('POC_PATH')
            for parent, dirnames, filename_list in os.walk(poc_path, followlinks=True):
                for filename in filename_list:
                    if filename[-3:] == 'pyc' or filename[:2] == '__' or filename[-5:] == '__.py' or filename[-3:] != '.py':
                        continue
                    file_path = os.path.join(parent, filename)
                    _python_module_object = importlib.import_module('.'.join(re.split('[\\\\/]', file_path[len(flask_path):-3])))
                    _script_module = getattr(_python_module_object, 'Script')(None)
                    _script_path = '.'.join(re.split('[\\\\/]', file_path[len(flask_path):-3]))
                    re_result = re.search(r'exploit\.scripts\.(.*)\.(.*)', _script_path)
                    domain_poc = DomainPoc()
                    domain_poc.parent = re_result.group(1).replace('.', '_')
                    domain_poc.name = re_result.group(2)
                    domain_poc.type = _script_module.bug_type
                    domain_poc.number = _script_module.bug_number if _script_module.bug_number else '-'
                    domain_poc.url = _script_path
                    domain_poc.info = _script_module.info if _script_module.info else '-'
                    DomainPoc.add_poc(domain_poc)
            return {'status': True}
        return {'status': False}
