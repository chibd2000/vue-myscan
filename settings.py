
# 动态追踪修改设置，如未设置只会提示警告,也就是说你在数据库修改的会在models中同步
# SQLALCHEMY_TRACK_MODIFICATIONS = True
from app import myscan_app
from utils.conf_reader import get_sqlalchemy_conf, get_jwt_secret

# 设置连接数据库的url
SQLALCHEMY_DATABASE_URI = get_sqlalchemy_conf()
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@myscan_mysql:3306/myscan'

# SQL语句输出
# SQLALCHEMY_ECHO = True

# 调试，支持热加载
DEBUG = True

# 环境
FLASK_ENV = 'production'

SECRET_KEY = get_jwt_secret()

# 接口路径
APPLICATION_ROOT = '/myscan-api'

# token有效时间
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
