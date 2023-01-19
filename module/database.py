# coding=utf-8
# @Author   : zpchcbd HG team
# @blog     : https://www.cnblogs.com/zpchcbd/
# @Time     : 2021-11-26 18:48

"""如果之后继续进行数据库整理的话，再把这个写上 created in 2021.11.26 18.54 @zpchcbd"""
from module.data import gLogger
import pymysql.cursors


# 参考文章：https://www.cnblogs.com/xueweisuoyong/archive/2019/11/13/11851246.html

class Database:
    """ Python连接到 MySQL 数据库及相关操作 """
    connected = False
    __conn = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_single_instance'):
            cls._single_instance = super(Database, cls).__new__(cls)
        return cls._single_instance

    # 构造函数，初始化时直接连接数据库
    def __init__(self, conf):
        if type(conf) is not dict:
            gLogger.myscan_error('错误: 参数不是字典类型！')
        else:
            for key in ['host', 'port', 'user', 'pass', 'db']:
                if key not in conf.keys():
                    gLogger.myscan_error('错误: 参数字典缺少 %s' % key)
            if 'charset' not in conf.keys():
                conf['charset'] = 'utf8'
        try:
            self.__conn = pymysql.connect(
                host=conf['host'],
                port=conf['port'],
                user=conf['user'],
                passwd=conf['pass'],
                db=conf['db'],
                charset=conf['charset'],
                cursorclass=pymysql.cursors.DictCursor)
            self.connected = True
        except pymysql.Error as e:
            gLogger.myscan_error('数据库连接失败:')

    # 插入数据到数据表
    def insert(self, table, val_obj):
        sql_top = 'INSERT INTO ' + table + ' ('
        sql_tail = ') VALUES ('
        try:
            for key, val in val_obj.items():
                sql_top += key + ','
                sql_tail += '"' + val + '"' + ',' if type(val) == str and val != 'NULL' else str(val) + ','
            sql = sql_top[:-1] + sql_tail[:-1] + ')'
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return self.__conn.insert_id()
        except pymysql.Error as e:
            gLogger.myscan_error(e.__str__())
            self.__conn.rollback()
            return False

    # 更新数据到数据表
    def update(self, table, val_obj, range_str):
        sql = 'UPDATE ' + table + ' SET '
        try:
            for key, val in val_obj.items():
                sql += key + '=' + '"' + val + '"' + ',' if type(val) == str and val != 'NULL' else key + '=' + str(
                    val) + ','
            sql = sql[:-1] + ' WHERE ' + range_str
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.rowcount
        except pymysql.Error as e:
            gLogger.myscan_error(e.__str__())
            self.__conn.rollback()
            return False

    # 删除数据在数据表中
    def delete(self, table, range_str):
        sql = 'DELETE FROM ' + table + ' WHERE ' + range_str
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.rowcount
        except pymysql.Error as e:
            gLogger.myscan_error(e.__str__())
            self.__conn.rollback()
            return False

    # 查询唯一数据在数据表中
    def select_one(self, table, factor_str, field='*'):
        sql = 'SELECT ' + field + ' FROM ' + table + ' WHERE ' + factor_str
        # print(sql)
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.fetchall()[0]
        except pymysql.Error as e:
            gLogger.myscan_error(e.__str__())
            return False

    # 查询多条数据在数据表中
    def select_more(self, table, range_str, field='*'):
        sql = 'SELECT ' + field + ' FROM ' + table + ' WHERE ' + range_str
        # print(sql)
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.fetchall()
        except pymysql.Error as e:
            gLogger.myscan_error(e.__str__())
            return False

    # 统计某表某条件下的总行数
    def count(self, table, range_str='1'):
        sql = 'SELECT count(*)res FROM ' + table + ' WHERE ' + range_str
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.fetchall()[0]['res']
        except pymysql.Error as e:
            gLogger.myscan_error(e.__str__())
            return False

    # 统计某字段（或字段计算公式）的合计值
    def sum(self, table, field, range_str='1'):
        sql = 'SELECT SUM(' + field + ') AS res FROM ' + table + ' WHERE ' + range_str
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.fetchall()[0]['res']
        except pymysql.Error as e:
            gLogger.myscan_error(e.__str__())
            return False

    # 销毁对象时关闭数据库连接
    def __del__(self):
        try:
            self.__conn.close()
        except pymysql.Error as e:
            gLogger.myscan_error(e.__str__())

    # 关闭数据库连接
    def close(self):
        self.__del__()


class MyscanDB(Database):

    def update_task_module_status(self, data, domain_id):
        self.update('domain_task', {'module_status': data}, 'domain_id="{}"'.format(domain_id))

    def update_task_start_time(self, data, domain_id):
        self.update('domain_task', {'scanning_start_time': data}, 'domain_id="{}"'.format(domain_id))

    def update_task_end_time(self, data, domain_id):
        self.update('domain_task', {'scanning_end_time': data}, 'domain_id="{}"'.format(domain_id))

    def update_task_status(self, data, domain_id):
        self.update('domain_task', {'status': data}, 'domain_id="{}"'.format(domain_id))


class GithubDB(Database):

    def get_monitor_task_by_monitorid(self, monitor_id=None):
        if monitor_id:
            return self.select_one('github_task', f'monitor_id="{monitor_id}"')
        else:
            return self.select_more('github_task', '1')

    def get_commit_by_monitorid(self, monitor_id, field='*'):
        return self.select_more('github_commit', f'monitor_id="{monitor_id}"', field)

    def get_issue_by_monitorid(self, monitor_id, field='*'):
        return self.select_more('github_issue', f'monitor_id="{monitor_id}"', field)

    def insert_commit(self, info):
        self.insert('github_commit', info)

    def insert_issue(self, info):
        self.insert('github_issue', info)

    def update_next_update_time(self, time, monitor_id):
        self.update('github_task', {'next_update_time': time, 'status': '0'}, f'monitor_id="{monitor_id}"')

    def update_last_update_time(self, time, monitor_id):
        self.update('github_task', {'last_update_time': time, 'status': '1'}, f'monitor_id="{monitor_id}"')


if __name__ == '__main__':
    # 测试单例模式
    # t = Database(1)
    # print(id(t))
    # c = Database(1)
    # print(id(c))

    # 测试Database
    conf = {'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'pass': 'Chiling.123', 'db': 'myscan'}
    database = MyscanDB(conf)

    # print(Database._single_instance.update('domain_task', {'name': '"aaaa"'} , 'domain_id="f236550506b0411aea1e8b1eff05392"'))

    # test = [{'id': 'NULL', 'domain_id': '1305e168496c3772742491e7659f658', 'url': 'http://sysjs.zjhu.edu.cn', 'status': 200, 'title': 'asdasd', 'x_powered_by': 'jetty'}]
    # for _ in test:
    #     t = database.insert('domain_ip', _)
    #     print(t)

    # 数据更新
    # print(database.update('domain_task', {'name': '"aaaa"'} , 'domain_id="f236550506b0411aea1e8b1eff05392"'))

    # 数据删除
    # print(Database().delete('domain_task', 'domain_id="f236550506b0411aea1e8b1eff05392"'))
