from flask_restful import fields, Resource, marshal_with


class ArticleView(Resource):  # 类视图不同于之前继承View,这里需要继承Resource
    menu_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'path': fields.String
    }

    resource_fields = {
        'menu_list': fields.List(fields.Nested(menu_fields)),
    }

    @marshal_with(resource_fields)  # 关联返回字段信息
    def get(self):
        menu_list = {'menu_list': [
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
                "name": '系统设置',
                'path': '/settings',
            },
            {
                'id': 6,
                "name": 'GIT监控',
                'path': '/git',
            },
            # {
            #     'id': 7,
            #     "name": '日志操作',
            #     'path': '/log',
            # }
        ]}

        return menu_list
