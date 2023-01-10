import time

from flask_restful import Resource, reqparse
from io import BytesIO

from werkzeug import Response


class MyscanResource(Resource):

    def get_parser(self):
        parser = reqparse.RequestParser()
        # login
        parser.add_argument('username', type=str, help='Rate to charge for this resource')
        parser.add_argument('password', type=str, help='Rate to charge for this resource')
        # domain task
        parser.add_argument('domain_id', type=str, help='Rate to charge for this resource')
        parser.add_argument('task_name', type=str, help='Rate to charge for this resource')
        parser.add_argument('task_target', type=str, help='Rate to charge for this resource')
        parser.add_argument('task_port_content', type=str, help='Rate to charge for this resource')
        parser.add_argument('task_port', type=bool, help='Rate to charge for this resource')
        parser.add_argument('task_ksubdomain', type=bool, help='Rate to charge for this resource')
        parser.add_argument('task_service', type=bool, help='Rate to charge for this resource')
        parser.add_argument('task_web', type=bool, help='Rate to charge for this resource')
        parser.add_argument('task_web_poc_type', type=str, help='Rate to charge for this resource')
        parser.add_argument('task_verify', type=bool, help='Rate to charge for this resource')
        parser.add_argument('task_proxy', type=str, help='Rate to charge for this resource')
        parser.add_argument('task_websearch', type=str, help='Rate to charge for this resource')
        # verify
        parser.add_argument('task_web_poc', type=str, help='Rate to charge for this resource')
        parser.add_argument('task_verify_type', type=str, help='Rate to charge for this resource')
        parser.add_argument('task_verify_space', type=str, help='Rate to charge for this resource')
        # commit
        parser.add_argument('monitor_id', type=str, help='Rate to charge for this resource')
        parser.add_argument('git_type', type=str, help='Rate to charge for this resource')
        # settings config
        parser.add_argument('wake_type', type=str, help='Rate to charge for this resource')
        parser.add_argument('is_show', type=int, help='Rate to charge for this resource')

        return parser.parse_args()

    def send_file(self, export_type, data):
        output = BytesIO()
        output.write(data.encode())
        output.seek(0)
        response = Response(output, content_type='application/octet-stream')
        response.headers['Content-disposition'] = 'attachment; filename={type}_{time}.txt'.format(type=export_type, time=int(time.time()))
        return response

    def save_file(self):
        pass


