from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with

from views.MyscanResource import MyscanResource


# 菜单列表，这里写在后端，原因是防止模版以及信息泄漏
class UserMenu(MyscanResource):

    menu_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'path': fields.String
    }

    resource_fields = {
        'menus': fields.List(fields.Nested(menu_fields)),
    }

    @marshal_with(resource_fields)  # 关联返回字段信息
    @jwt_required()
    def get(self):
        menu_list = {'menus': [
            {
                'id': 1,
                'name': '任务管理',
                'path': '/task',
            },
            {
                'id': 2,
                "name": '漏洞验证',
                'path': '/verify',
            },
            {
                'id': 3,
                'name': '资产搜索',
                'path': '/search',
            },
            {
                'id': 4,
                "name": 'POC管理',
                'path': '/poc',
            },
            {
                'id': 5,
                "name": 'GIT监控',
                'path': '/git',
            },
            {
                'id': 6,
                "name": '系统设置',
                'path': '/settings',
            },
            # {
            #     'id': 7,
            #     "name": '日志操作',
            #     'path': '/log',
            # }
        ]}

        return menu_list
