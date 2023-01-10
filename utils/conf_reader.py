import os
import yaml


def read_yaml_to_dict(yaml_path: str):
    try:
        with open(yaml_path, 'rb') as file:
            config_dict = yaml.load(file.read(), Loader=yaml.FullLoader)
            return config_dict
    except Exception as e:
        exit(print("[-] read_yaml_to_dict error, the error is {}".format(e.args)))


def get_celery_conf():
    yaml_config_dict = read_yaml_to_dict(os.getcwd() + os.path.sep + 'config/conf.yaml')
    return {'schedule': yaml_config_dict['celery']['schedule'] if yaml_config_dict['celery']['schedule'] else 60}


def get_database_conf():
    yaml_config_dict = read_yaml_to_dict(os.getcwd() + os.path.sep + 'config/conf.yaml')
    return {'host': yaml_config_dict['db']['addr'],
            'port': yaml_config_dict['db']['port'],
            'user': yaml_config_dict['db']['user'],
            'pass': yaml_config_dict['db']['pass'],
            'db': yaml_config_dict['db']['db']}


def get_qq_mail_conf():
    yaml_config_dict = read_yaml_to_dict(os.getcwd() + os.path.sep + 'config/conf.yaml')
    return {'key': yaml_config_dict['mail']['qq']['key'],
            'receiver': yaml_config_dict['mail']['qq']['receiver'],
            'sender': yaml_config_dict['mail']['qq']['sender']}


def get_github_conf():
    yaml_config_dict = read_yaml_to_dict(os.getcwd() + os.path.sep + 'config/conf.yaml')
    return {'api': yaml_config_dict['github']['api']}


def get_weixin_mail_conf():
    yaml_config_dict = read_yaml_to_dict(os.getcwd() + os.path.sep + 'config/conf.yaml')
    return {'app_id': yaml_config_dict['mail']['weixin']['app_id'],
            'app_secret': yaml_config_dict['mail']['weixin']['app_secret'],
            'user_id': yaml_config_dict['mail']['weixin']['user_id'],
            'template_id': yaml_config_dict['mail']['weixin']['template_id']}


def get_sqlalchemy_conf():
    yaml_config_dict = read_yaml_to_dict(os.getcwd() + os.path.sep + 'config/conf.yaml')
    return 'mysql+pymysql://' + yaml_config_dict['db']['user'] + ':' + yaml_config_dict['db']['pass'] + '@' + \
        yaml_config_dict['db']['addr'] + ':' + str(yaml_config_dict['db']['port']) + '/' + yaml_config_dict['db']['db']


def get_jwt_secret():
    return b'_5#y2L"F4Q8z\n\xec]/'
