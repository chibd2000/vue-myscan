# coding: utf-8
import time

from sqlalchemy import Column, Integer, String, func
from sqlalchemy.schema import FetchedValue
from extension import db


class DomainSpider(db.Model):
    __tablename__ = 'domain_spider'

    id = Column(Integer, primary_key=True)
    domain_id = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, index=True, info='domainid')
    keyword = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='搜索语法')
    url = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='url地址')
    title = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='标题')
    type = Column(String(100, 'utf8mb3_unicode_ci'), nullable=False, info='类型')

    @staticmethod
    def init_data():
        test_data = [
            (1, "1679091c5a880faf6fb5e6087eb1b2dc", "inurl: login", 'http://www.baidu.com/login', '登陆界面', 'baidu'),
            (2, "1679091c5a880faf6fb5e6087eb1b2dc", "inurl: system", 'http://www.baidu.com/system', '系统界面', 'bing')]
        for data in test_data:
            domain_baidu_spider = DomainSpider()
            domain_baidu_spider.id = data[0]
            domain_baidu_spider.domain_id = data[1]
            domain_baidu_spider.keyword = data[2]
            domain_baidu_spider.url = data[3]
            domain_baidu_spider.title = data[4]
            domain_baidu_spider.type = data[5]
            db.session.add(domain_baidu_spider)
        db.session.commit()


class DomainCert(db.Model):
    __tablename__ = 'domain_cert'

    id = Column(Integer, primary_key=True)
    domain_id = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, index=True)
    subdomain = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False)
    cert = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False)


class DomainCseg(db.Model):
    __tablename__ = 'domain_cseg'

    id = Column(Integer, primary_key=True)
    domain_id = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, index=True)
    ip_segment = Column(String(100, 'utf8mb3_unicode_ci'), nullable=False)
    ips = Column(String(1024, 'utf8mb3_unicode_ci'), nullable=False)
    num = Column(Integer, nullable=False)

    @staticmethod
    def init_data():
        test_data = [
            (1, "1679091c5a880faf6fb5e6087eb1b2dc", '1.1.1.1/24', '', 0),
            (2, "1679091c5a880faf6fb5e6087eb1b2dc", '2.2.2.2/24', '2.2.2.4,2.2.2.5', 2)]
        for data in test_data:
            domain_cseg = DomainCseg()
            domain_cseg.id = data[0]
            domain_cseg.domain_id = data[1]
            domain_cseg.ip_segment = data[2]
            domain_cseg.ips = data[3]
            domain_cseg.num = data[4]
            db.session.add(domain_cseg)
        db.session.commit()


class DomainAsn(db.Model):
    __tablename__ = 'domain_asn'

    id = Column(Integer, primary_key=True)
    domain_id = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, index=True)
    asn = Column(Integer, nullable=False)

    @staticmethod
    def init_data():
        test_data = [
            (1, "1679091c5a880faf6fb5e6087eb1b2dc", 11111),
            (2, "1679091c5a880faf6fb5e6087eb1b2dc", 22222)]
        for data in test_data:
            domain_asn = DomainAsn()
            domain_asn.id = data[0]
            domain_asn.domain_id = data[1]
            domain_asn.asn = data[2]
            db.session.add(domain_asn)
        db.session.commit()


class DomainSimilar(db.Model):
    __tablename__ = 'domain_similar'

    id = Column(Integer, primary_key=True)
    domain_id = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, index=True)
    similar = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False)

    @staticmethod
    def init_data():
        test_data = [
            (1, "1679091c5a880faf6fb5e6087eb1b2dc", 'aaa.baidu.com,ccc.baidu.com')]
        for data in test_data:
            domain_similar = DomainSimilar()
            domain_similar.id = data[0]
            domain_similar.domain_id = data[1]
            domain_similar.similar = data[2]
            db.session.add(domain_similar)
        db.session.commit()


# 已经写好了
class DomainIp(db.Model):
    __tablename__ = 'domain_ip'

    id = Column(Integer, primary_key=True)
    domain_id = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, index=True)
    ip = Column(String(100, 'utf8mb3_unicode_ci'), nullable=False)
    ip2domain = Column(String(1024, 'utf8mb3_unicode_ci'), nullable=True)

    @staticmethod
    def init_data():
        test_data = [
            (1, '1679091c5a880faf6fb5e6087eb1b2dc', "61.153.52.52", 'libvpn.zjhu.edu.cn'),
            (2, '1679091c5a880faf6fb5e6087eb1b2dc', "61.153.52.57", "vpn.zjhu.edu.cn"),
            (3, '1679091c5a880faf6fb5e6087eb1b2dc', "61.153.52.20", 'rz.zjhu.edu.cn'),
            (4, '1679091c5a880faf6fb5e6087eb1b2dc', "61.153.52.48", 'lslnyjy.zjhu.edu.cn'),
            (5, '1679091c5a880faf6fb5e6087eb1b2dc', "61.153.52.31", 'rs.zjhu.edu.cn,xxcj.zjhu.edu.cn,dcard.zjhu.edu.cn')
        ]

        for data in test_data:
            domain_ip = DomainIp()
            domain_ip.id = data[0]
            domain_ip.domain_id = data[1]
            domain_ip.ip = data[2]
            domain_ip.ip2domain = data[3]
            db.session.add(domain_ip)
        db.session.commit()

    @staticmethod
    def export_ip_by_domainid(domain_id):
        return db.session.filter_by(domain_id=domain_id).all()


# 已经写好了
class DomainService(db.Model):
    __tablename__ = 'domain_service'

    id = Column(Integer, primary_key=True)
    domain_id = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, index=True)
    ip = Column(String(100, 'utf8mb3_unicode_ci'), nullable=False)
    port = Column(Integer, nullable=False)
    service = Column(String(100, 'utf8mb3_unicode_ci'), nullable=True)
    title = Column(String(100, 'utf8mb3_unicode_ci'), nullable=True)
    info = Column(String(1024, 'utf8mb3_unicode_ci'), nullable=True)

    @staticmethod
    def init_data():
        test_data = [
            (1, '1679091c5a880faf6fb5e6087eb1b2dc', '61.153.52.57', 443, 'http/ssl', 'HTTP/1.1 200 OK', 'None'),
            (2, '1679091c5a880faf6fb5e6087eb1b2dc', '61.153.52.57', 8080, 'apache tomcat 9.0', 'HTTP/1.1 200 OK',
             'None'),
            (3, '1679091c5a880faf6fb5e6087eb1b2dc', '61.153.52.11', 6379, 'redis', 'redis', 'redis store key'),
        ]

        # select
        for data in test_data:
            domain_service = DomainService()
            domain_service.id = data[0]
            domain_service.domain_id = data[1]
            domain_service.ip = data[2]
            domain_service.port = data[3]
            domain_service.service = data[4]
            domain_service.title = data[5]
            domain_service.info = data[6]
            db.session.add(domain_service)
        db.session.commit()

    @staticmethod
    def export_ip_port_by_domainid(domain_id):
        return db.session.filter_by(domain_id=domain_id).all()


class DomainEnterprise(db.Model):
    __tablename__ = 'domain_enterprise'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), info='企业名称')
    reg_name = Column(String(255), info='企业注册人姓名')
    reg_email = Column(String(255))
    reg_mobile = Column(String(255))
    enterprise_id = Column(String(255), info='企业ID')


# 已经写好了
class DomainSubdomain(db.Model):
    __tablename__ = 'domain_subdomain'

    id = Column(Integer, primary_key=True)
    domain_id = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, index=True)
    subdomain = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False)
    resolve_type = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='域名解析类型')
    ip = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='域名解析记录')

    @staticmethod
    def init_data():
        test_data = [
            (1, '1679091c5a880faf6fb5e6087eb1b2dc', "libvpn.zjhu.edu.cn", 'A', '61.153.52.52'),
            (2, '1679091c5a880faf6fb5e6087eb1b2dc', "vpn.zjhu.edu.cn", 'A', "172.20.6.20"),
            (3, '1679091c5a880faf6fb5e6087eb1b2dc', "rz.zjhu.edu.cn", 'A', '172.20.13.37'),
            (4, '1679091c5a880faf6fb5e6087eb1b2dc', "lslnyjy.zjhu.edu.cn", 'A', '61.153.52.48)'),
            (5, '1679091c5a880faf6fb5e6087eb1b2dc', "rs.zjhu.edu.cn", 'A', '172.20.8.124')
        ]

        for data in test_data:
            domain_subdomain = DomainSubdomain()
            domain_subdomain.id = data[0]
            domain_subdomain.domain_id = data[1]
            domain_subdomain.subdomain = data[2]
            domain_subdomain.resolve_type = data[3]
            domain_subdomain.ip = data[4]
            db.session.add(domain_subdomain)
        db.session.commit()

    @staticmethod
    def export_subdomain_by_domainid(domain_id):
        return db.session.query(DomainSubdomain.subdomain).distinct(DomainSubdomain.subdomain).filter_by(
            domain_id=domain_id).all()


# 已经写好了
class DomainTask(db.Model):
    __tablename__ = 'domain_task'

    domain_id = Column(String(255, 'utf8mb3_unicode_ci'), primary_key=True, index=True)
    target = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='要扫描的目标')
    name = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='备注')
    create_time = Column(Integer, nullable=False, info='添加时间')
    is_ksubdomain = Column(Integer, server_default=FetchedValue(), info='web 域名爆破')
    is_websearch = Column(Integer, server_default=FetchedValue(), info='web 域名搜集')
    is_portscan = Column(Integer, server_default=FetchedValue(), info='IP 端口扫描')
    is_webscan = Column(Integer, server_default=FetchedValue(), info='web poc扫描')
    is_servicescan = Column(Integer, server_default=FetchedValue(), info='ip 端口服务利用')
    web_poc_scan_type = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='WEB扫描 attack / detect / exec')
    status = Column(Integer, nullable=False, server_default=FetchedValue(), info='默认 0未扫描等待中  1已扫描 2扫描中')
    module_status = Column(String(255, 'utf8mb3_unicode_ci'), nullable=True, info='运行到哪个模块')
    scanning_start_time = Column(Integer, info='扫描开始时间')
    scanning_end_time = Column(Integer, info='扫描结束时间')
    delete_status = Column(Integer, nullable=False, server_default=FetchedValue(), info='0代表未删除，1代表用户删除')
    is_verify = Column(Integer, nullable=False, server_default=FetchedValue(), info='默认为0')
    proxy = Column(String(255, 'utf8mb3_unicode_ci'), nullable=True, info='代理地址')

    @classmethod
    def find_by_task_name(cls, task_name):
        return cls.query.filter_by(name=task_name)

    @staticmethod
    def update_start_time(domain_id):
        db.session.query(DomainTask).filter_by(domain_id=domain_id).update({'scanning_start_time': int(time.time())})
        db.session.commit()
        return True

    @staticmethod
    def update_end_time(domain_id):
        db.session.query(DomainTask).filter_by(domain_id=domain_id).update({'scanning_start_time': int(time.time())})
        db.session.commit()
        return True

    @staticmethod
    def update_status(domain_id, status_value):
        db.session.query(DomainTask).filter_by(domain_id=domain_id).update({'status': status_value})
        db.session.commit()
        return True

    @staticmethod
    def update_module_status(domain_id, module_status_value):
        db.session.query(DomainTask).filter_by(domain_id=domain_id).update({'module_status': module_status_value})
        db.session.commit()
        return True

    @staticmethod
    def delete_task_by_domainid(domain_id):
        db.session.query(DomainSpider).filter_by(domain_id=domain_id).delete()
        db.session.query(DomainCert).filter_by(domain_id=domain_id).delete()
        db.session.query(DomainCseg).filter_by(domain_id=domain_id).delete()
        db.session.query(DomainAsn).filter_by(domain_id=domain_id).delete()
        db.session.query(DomainSimilar).filter_by(domain_id=domain_id).delete()
        db.session.query(DomainIp).filter_by(domain_id=domain_id).delete()
        db.session.query(DomainService).filter_by(domain_id=domain_id).delete()
        db.session.query(DomainWebspace).filter_by(domain_id=domain_id).delete()
        db.session.query(DomainSubdomain).filter_by(domain_id=domain_id).delete()
        db.session.query(DomainWebtitle).filter_by(domain_id=domain_id).delete()
        db.session.query(DomainBeian).filter_by(domain_id=domain_id).delete()
        db.session.query(DomainVuln).filter_by(domain_id=domain_id).delete()
        db.session.query(DomainTask).filter_by(domain_id=domain_id).delete()
        db.session.commit()
        return True

    @staticmethod
    def add_task(task):
        db.session.add(task)
        db.session.commit()
        return True

    @staticmethod
    def init_data():
        test_data = [
            ('1679091c5a880faf6fb5e6087eb1b2dc', "oplpo.com", "百度测试", 1670929453, 1, 1, 1, 0, 1, 'attack', 1,
             'finish', 1670929455,
             1670929490, 0, 0, 'http://127.0.0.1:7890'),
        ]

        for data in test_data:
            domain_task = DomainTask()
            domain_task.domain_id = data[0]
            domain_task.target = data[1]
            domain_task.name = data[2]
            domain_task.create_time = data[3]
            domain_task.is_ksubdomain = data[4]
            domain_task.is_websearch = data[5]
            domain_task.is_portscan = data[6]
            domain_task.is_webscan = data[7]
            domain_task.is_servicescan = data[8]
            domain_task.web_poc_scan_type = data[9]
            domain_task.status = data[10]
            domain_task.module_status = data[11]
            domain_task.scanning_start_time = data[12]
            domain_task.scanning_end_time = data[13]
            domain_task.delete_status = data[14]
            domain_task.is_verify = data[15]
            domain_task.proxy = data[16]
            db.session.add(domain_task)
        db.session.commit()


# 已经写好了
class DomainUser(db.Model):
    __tablename__ = 'domain_user'

    userid = Column(Integer, primary_key=True)
    username = Column(String(255, 'utf8mb3_general_ci'), nullable=False, info='用户名')
    password = Column(String(255, 'utf8mb3_general_ci'), nullable=False, info='密码')
    ip = Column(String(100, 'utf8mb3_general_ci'), nullable=False, info='ip地址')
    start_time = Column(Integer, nullable=False, info='注册时间')
    status = Column(Integer, nullable=False, server_default=FetchedValue())
    img = Column(String(255, 'utf8mb3_unicode_ci'), server_default=FetchedValue())

    @classmethod
    def find_by_username(cls, username):
        #  参考：https://github.com/dickens88/flask-jwt-demo/blob/f6950e32c8eaa7e760886f5bd4a5264975db7312/models.py#L44
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def init_data():
        test_data = [(1, "admin", "admin", '192.168.1.1', 1670929455, False, '')]
        for data in test_data:
            domain_user = DomainUser()
            domain_user.userid = data[0]
            domain_user.username = data[1]
            domain_user.password = data[2]
            domain_user.ip = data[3]
            domain_user.start_time = data[4]
            domain_user.status = data[5]
            domain_user.img = data[6]
            db.session.add(domain_user)
        db.session.commit()


class DomainUserIpLog(db.Model):
    __tablename__ = 'domain_user_ip_logs'

    id = Column(Integer, primary_key=True)
    ip = Column(String(255, 'utf8mb3_general_ci'))
    time = Column(String(255, 'utf8mb3_general_ci'))
    userid = Column(String(255, 'utf8mb3_general_ci'))


# 已经写好了
class DomainVuln(db.Model):
    __tablename__ = 'domain_vuln'

    id = Column(Integer, primary_key=True)
    domain_id = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False)
    name = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='漏洞名字')
    url = Column(String(255, 'utf8mb3_unicode_ci'), info='漏洞地址')
    software = Column(String(255, 'utf8mb3_unicode_ci'), info='漏洞类型')

    @staticmethod
    def init_data():
        test_data = [
            (1, "1679091c5a880faf6fb5e6087eb1b2dc", 'testtest', 'http://www.baidu.com', 'yonyou'),
            (2, "1679091c5a880faf6fb5e6087eb1b2dc", 'qweqwe', 'http://www.hll.cn', 'weblogic'),
        ]

        for data in test_data:
            domain_vuln = DomainVuln()
            domain_vuln.id = data[0]
            domain_vuln.domain_id = data[1]
            domain_vuln.name = data[2]
            domain_vuln.url = data[3]
            domain_vuln.software = data[4]
            db.session.add(domain_vuln)
        db.session.commit()


class MailConfig(db.Model):
    __tablename__ = 'mail_config'

    id = Column(Integer, primary_key=True)
    wake_type = Column(String(255, 'utf8mb3_unicode_ci'), nullable=True, info='提醒类型')
    is_show = Column(Integer, nullable=False)

    @staticmethod
    def add_config(config):
        db.session.add(config)
        db.session.commit()
        return True

    @staticmethod
    def update_config(id, config):
        db.session.query(MailConfig).filter_by(id=id).update(
            {'wake_type': config.wake_type, 'is_show': config.is_show})
        db.session.commit()
        return True

    @staticmethod
    def init_data():
        data = (1, 'qq', 1)
        domain_config = MailConfig()
        domain_config.id = data[0]
        domain_config.wake_type = data[1]
        domain_config.is_show = data[2]
        db.session.add(domain_config)
        db.session.commit()


# 已经写好了
class DomainBeian(db.Model):
    __tablename__ = 'domain_beian'

    id = Column(Integer, primary_key=True)
    domain_id = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False)
    license = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='备案号')
    sitename = Column(String(255, 'utf8mb3_unicode_ci'), info='网站名称', nullable=False)
    domain = Column(String(255, 'utf8mb3_unicode_ci'), info='域名', nullable=False)
    verify_time = Column(String(255, 'utf8mb3_unicode_ci'), info='验证时间', nullable=False)

    @staticmethod
    def init_data():
        test_data = [
            (1, '1679091c5a880faf6fb5e6087eb1b2dc', '粤ICP备14091972号-27', '拉货就找货拉拉', 'www.hllw.cn',
             '2021-09-09'),
            (2, '1679091c5a880faf6fb5e6087eb1b2dc', '粤ICP备14091972号-26', '拉货就找货拉拉', 'www.hll.net',
             '2021-09-09'),
        ]

        for data in test_data:
            domain_beian = DomainBeian()
            domain_beian.id = data[0]
            domain_beian.domain_id = data[1]
            domain_beian.license = data[2]
            domain_beian.sitename = data[3]
            domain_beian.domain = data[4]
            domain_beian.verify_time = data[5]
            db.session.add(domain_beian)
        db.session.commit()


# 已经写好了
class DomainPoc(db.Model):
    __tablename__ = 'domain_poc'

    id = Column(Integer, primary_key=True)
    parent = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='影响框架')
    name = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='漏洞名称')
    type = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='漏洞类型')
    number = Column(String(255, 'utf8mb3_unicode_ci'), nullable=True, info='漏洞编号')
    url = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='漏洞地址')
    info = Column(String(1024, 'utf8mb3_unicode_ci'), nullable=False, info='漏洞信息')

    @staticmethod
    def add_poc(poc):
        db.session.add(poc)
        db.session.commit()
        return True

    @staticmethod
    def clear_poc():
        db.session.execute('truncate table `domain_poc`')
        db.session.commit()
        return True

    @staticmethod
    def get_poc_by_id(pocs):
        return db.session.query(DomainPoc).with_entities(func.group_concat(DomainPoc.url)).filter(
            DomainPoc.id.in_(pocs.split(','))).all()[0][0]

    @staticmethod
    def init_data():
        test_data = [
            (1, "SpringBoot", 'actuator接口未授权', 'Unauth', None, 'exploit.scripts.SpringBoot.actuator_unauth',
             'test1'),
            (2, "Weblogic", 'CVE_2020_14882', 'Remote Code Execution', 'CVE_2020_14882',
             'exploit.scripts.Weblogic.unauth_rce_CVE_2020_14882', 'test2'),
            (3, "Weblogic", 'CVE_2020_14883', 'Remote Code Execution', 'CVE_2020_14883',
             'exploit.scripts.Weblogic.unauth_rce_CVE_2020_14883', 'test3'),
            (4, "Weblogic", 'CVE_2020_14884', 'Remote Code Execution', 'CVE_2020_14884',
             'exploit.scripts.Weblogic.unauth_rce_CVE_2020_14884', 'test4'),
            (5, "Eyou", 'eyou代码执行', 'Remote Code Execution', 'CNVD-2021-26422',
             'exploit.scripts.Mail.Eyou.CNVD-2021-26422', 'test5'),
        ]

        for data in test_data:
            domain_poc = DomainPoc()
            domain_poc.id = data[0]
            domain_poc.parent = data[1]
            domain_poc.name = data[2]
            domain_poc.type = data[3]
            domain_poc.number = data[4]
            domain_poc.url = data[5]
            domain_poc.info = data[6]
            db.session.add(domain_poc)
        db.session.commit()


class DomainWebspace(db.Model):
    __tablename__ = 'domain_webspace'

    id = Column(Integer, primary_key=True)
    domain_id = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, index=True)
    spider = Column(String(50, 'utf8mb3_unicode_ci'), nullable=False, info='引擎类型')
    subdomain = Column(String(100, 'utf8mb3_unicode_ci'), info='子域名')
    title = Column(String(255, 'utf8mb3_unicode_ci'), nullable=True, info='标题')
    ip_port = Column(String(100, 'utf8mb3_unicode_ci'), nullable=False, info='ip:port')
    domain = Column(String(100, 'utf8mb3_unicode_ci'), nullable=True, info='domain')
    web_service = Column(String(100, 'utf8mb3_unicode_ci'), nullable=True, info='端口服务')
    port_service = Column(String(100, 'utf8mb3_unicode_ci'), nullable=True, info='协议')
    asn = Column(Integer, nullable=True, info='asn')
    search_keyword = Column(String(100, 'utf8mb3_unicode_ci'), nullable=False, info='查询语法')

    @staticmethod
    def init_data():
        test_data = [
            (1, '1679091c5a880faf6fb5e6087eb1b2dc', 'FOFA', 'lslasdnyjy.zjhu.edu.cn', '撒打算打算的', '61.153.52.48:80',
             'zjhu.edu.cn', 'Apache-Coyote/1.1', 'http', 4134, 'domain="zjhu.edu.cn"'),
            (2, '1679091c5a880faf6fb5e6087eb1b2dc', 'HUNTER', 'lslnyjaaay.zjhu.edu.cn', '撒打算打算的',
             '61.153.52.48:80',
             'zjhu.edu.cn', 'Apache-Coyote/1.1', 'http', 4134, 'domain="zjhu.edu.cn"'),
            (
                3, '1679091c5a880faf6fb5e6087eb1b2dc', 'QUAKE', 'lslnyjbbby.zjhu.edu.cn', '撒打算打算的',
                '61.153.52.48:80',
                'zjhu.edu.cn', 'Apache-Coyote/1.1', 'http', 4134, 'domain="zjhu.edu.cn"'),
            (4, '1679091c5a880faf6fb5e6087eb1b2dc', 'SHODAN', 'lslcccnyjy.zjhu.edu.cn', '撒打算打算的',
             '61.153.52.48:80',
             'zjhu.edu.cn', 'Apache-Coyote/1.1', 'http', 4134, 'domain="zjhu.edu.cn"'),
        ]

        for data in test_data:
            domain_webspace = DomainWebspace()
            domain_webspace.id = data[0]
            domain_webspace.domain_id = data[1]
            domain_webspace.spider = data[2]
            domain_webspace.subdomain = data[3]
            domain_webspace.title = data[4]
            domain_webspace.ip_port = data[5]
            domain_webspace.domain = data[6]
            domain_webspace.web_service = data[7]
            domain_webspace.port_service = data[9]
            domain_webspace.asn = data[9]
            domain_webspace.search_keyword = data[10]
            db.session.add(domain_webspace)
        db.session.commit()


# 已经写好了
class DomainWebtitle(db.Model):
    __tablename__ = 'domain_webtitle'

    id = Column(Integer, primary_key=True)
    domain_id = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, index=True)
    url = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='url地址')
    status = Column(Integer, nullable=False, info='状态')
    title = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='标题')
    header = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='header中的特征')

    @staticmethod
    def init_data():
        test_data = [
            (1, "1679091c5a880faf6fb5e6087eb1b2dc", "http://zcjy.zjhu.edu.cn", 200, "湖州师范学院-资产经营公司", ""),
            (2, "1679091c5a880faf6fb5e6087eb1b2dc", "http://xlcp.zjhu.edu.cn", 200, "IIS Windows Server", "ASP.NET"),
            (3, "1679091c5a880faf6fb5e6087eb1b2dc", "http://rsc.zjhu.edu.cn", 200, "人事处", "ThinkPHP")
        ]
        for data in test_data:
            domain_title = DomainWebtitle()
            domain_title.id = data[0]
            domain_title.domain_id = data[1]
            domain_title.url = data[2]
            domain_title.status = data[3]
            domain_title.title = data[4]
            domain_title.header = data[5]
            db.session.add(domain_title)
        db.session.commit()

    @staticmethod
    def export_website_by_domainid(domain_id):
        return db.session.filter_by(domain_id=domain_id).all()


# 下面是github的扩展模块

class GithubTask(db.Model):
    __tablename__ = 'github_task'

    monitor_id = Column(String(255, 'utf8mb3_unicode_ci'), primary_key=True, index=True)
    target = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='目标仓库')
    name = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='备注名称')
    not_visited = Column(Integer, nullable=False, info='等待查看的条目')
    status = Column(Integer, nullable=False, info='运行状态')
    last_update_time = Column(Integer, nullable=True, info='上次扫描时间')
    next_update_time = Column(Integer, nullable=True, info='下次扫描时间')
    create_time = Column(Integer, nullable=False, info='任务添加时间')

    @staticmethod
    def add_task(github_task):
        db.session.add(github_task)
        db.session.commit()
        return True

    @staticmethod
    def delete_task_by_mointorid(monitor_id):
        db.session.query(GithubCommit).filter_by(monitor_id=monitor_id).delete()
        db.session.query(GithubTask).filter_by(monitor_id=monitor_id).delete()
        db.session.commit()
        return True

    @staticmethod
    def init_data():
        test_data = [
            ("1679091c5a880faf6fb5e6087eb1b2dc", "chibd2000/myscan", 'zpchcbd的myscan工程', 2, 0, 1670929455, None,
             None),
        ]

        for data in test_data:
            github_task = GithubTask()
            github_task.monitor_id = data[0]
            github_task.target = data[1]
            github_task.name = data[2]
            github_task.not_visited = data[3]
            github_task.status = data[4]
            github_task.create_time = data[5]
            github_task.last_update_time = data[6]
            github_task.next_update_time = data[7]
            db.session.add(github_task)
        db.session.commit()


class GithubCommit(db.Model):
    __tablename__ = 'github_commit'

    commit_sha = Column(String(255, 'utf8mb3_unicode_ci'), primary_key=True, index=True)
    monitor_id = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, index=True)
    commit_url = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='url地址')
    commit_message = Column(String(2048, 'utf8mb3_unicode_ci'), nullable=False, info='commit信息')
    commit_author_name = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='commit信息')
    commit_author_date = Column(Integer, nullable=False, info='时间')
    commit_committer_name = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='commit信息')
    commit_committer_date = Column(Integer, nullable=False, info='时间')
    # commit_file = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='标题')
    # commit_status = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='状态')
    commit_branch = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='分支')
    commit_level = Column(Integer, nullable=False, info='程度')
    is_visited = Column(Integer, nullable=False, info='是否已经阅读')

    @staticmethod
    def update_visited(monitor_id):
        db.session.query(GithubCommit).filter_by(monitor_id=monitor_id, is_visited=0).update({'is_visited': 1})
        db.session.commit()
        return True

    @staticmethod
    def init_data():
        test_data = [
            ("4d6ef48e73e31a2c1cc7ce8c70d4f3863b91cc07", "1679091c5a880faf6fb5e6087eb1b2dc",
             "https://api.github.com/repos/chibd2000/myscan/commits/4d6ef48e73e31a2c1cc7ce8c70d4f3863b91cc07",
             'fix bug', 'chibd2000', 1670929455, 'GitHub', 1670929455, 'master', 1, 1),
            ("4d6ef48e73e31a2c1cc7ce8c70d4f3863b91cc08", "1679091c5a880faf6fb5e6087eb1b2dc",
             "https://api.github.com/repos/chibd2000/myscan/commits/4d6ef48e73e31a2c1cc7ce8c70d4f3863b91cc07",
             'fix bug', 'chibd2000', 1670929455, 'GitHub', 1670929455, 'master', 0, 0),
        ]

        for data in test_data:
            github_commit = GithubCommit()
            github_commit.commit_sha = data[0]
            github_commit.monitor_id = data[1]
            github_commit.commit_url = data[2]
            github_commit.commit_message = data[3]
            github_commit.commit_author_name = data[4]
            github_commit.commit_author_date = data[5]
            github_commit.commit_committer_name = data[6]
            github_commit.commit_committer_date = data[7]
            github_commit.commit_branch = data[8]
            github_commit.commit_level = data[9]
            github_commit.is_visited = data[10]
            # github_commit.commit_file = data[8]
            # github_commit.commit_status = data[9]
            db.session.add(github_commit)
        db.session.commit()


class GithubIssue(db.Model):
    __tablename__ = 'github_issue'

    issue_id = Column(Integer, primary_key=True)
    monitor_id = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, index=True)
    issue_url = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='地址')
    issue_create_user = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='问题创建用户')
    issue_create_date = Column(Integer, nullable=False, info='问题创建时间')
    issue_status = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='状态')
    issue_level = Column(Integer, nullable=False, info='程度')
    issue_title = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='标题')
    issue_body = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='内容')
    type = Column(String(255, 'utf8mb3_unicode_ci'), nullable=False, info='is pr or issue')
    is_visited = Column(Integer, nullable=False, info='是否已经阅读')

    @staticmethod
    def update_visited(monitor_id):
        db.session.query(GithubIssue).filter_by(monitor_id=monitor_id, is_visited=0).update({'is_visited': 1})
        db.session.commit()
        return True


