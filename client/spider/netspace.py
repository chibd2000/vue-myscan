# coding=utf-8

from core.parser.urlparser import UrlParser
from core.public import *
from core.exception.net import NetPageLimitError, NetPrivilegeError, NetSyntaxError, NetTokenError, NetIntegralError
from core.request.asynchttp import AsyncFetcher
from core.data import config_dict, gLogger
from core.utils.tools import get_port_service, get_url
from core.constant import COMMON_FAVICON_LIST
from spider import BaseSpider
from shodan import Shodan
import mmh3
import codecs
import hashlib
import aiohttp
import asyncio


class NetProperty:
    """
    封装空间引擎最终需要写入的字段
    """
    SPIDER_FIELD, SUBDOMAIN_FIELD, TITLE_FIELD, IP_FIELD, PORT_FIELD, IP_PORT_FIELD, DOMAIN_FIELD, WEBSERVICE_FIELD, PORTSERVICE_FIELD \
        , ASN_FIELD, SEARCHKEYWORD = 'spider', 'subdomain', 'title', 'ip', 'port', 'ip_port', 'domain', 'web_service', 'port_service', 'asn', 'search_keyword'


class HunterProperty:
    """
    封装每个对应的空间引擎所采集的字段
    """
    NAME_FIELD, SUBDOMAIN_FIELD, TITLE_FIELD, IP_FIELD, DOMAIN_FIELD, PORT_FIELD, WEBSERVICE_FIELD, \
        PORTSERVICE_FIELD, ASN_FIELD = 'HUNTER', 'domain', 'web_title', 'ip', 'url', 'port', 'component', 'port_service', ''

    def __init__(self, _, keyword):
        self.name = HunterProperty.NAME_FIELD
        self.subdomain = _.get(HunterProperty.SUBDOMAIN_FIELD, '')
        self.portService = get_port_service(_.get(HunterProperty.PORT_FIELD, ''))
        self.root_domain = UrlParser(_.get(HunterProperty.DOMAIN_FIELD, '')).rootdomain
        self.port = _.get(HunterProperty.PORT_FIELD, '')
        self.ip = _.get(HunterProperty.IP_FIELD, '')
        self.title = _.get(HunterProperty.TITLE_FIELD, '')
        self.webService = _.get(HunterProperty.WEBSERVICE_FIELD, '')
        self.asn = _.get(HunterProperty.ASN_FIELD, 0)
        self.keyword = keyword

    # @property
    # def info(self):
    #     return {NetProperty.SPIDER_FIELD: self.name, NetProperty.SUBDOMAIN_FIELD: self.subdomain,
    #             NetProperty.TITLE_FIELD: self.title, NetProperty.IP_PORT_FIELD: '{}:{}'.format(self.ip,self.port),
    #             NetProperty.DOMAIN_FIELD: self.root_domain, NetProperty.WEBSERVICE_FIELD: str(self.webService),
    #             NetProperty.PORTSERVICE_FIELD: self.portService, NetProperty.ASN_FIELD: self.asn, NetProperty.SEARCHKEYWORD: self.keyword}


class QuakeProperty:
    """
    封装每个对应的空间引擎所采集的字段
    """
    NAME_FIELD, SUBDOMAIN_FIELD, TITLE_FIELD, IP_FIELD, DOMAIN_FIELD, PORT_FIELD, WEBSERVICE_FIELD, \
        PORTSERVICE_FIELD, ASN_FIELD = 'QUAKE', 'subdomain', 'title', 'ip', 'domain', 'PORT', 'web_service', 'port_service', 'asn'

    def __init__(self):
        pass

    @property
    def info(self):
        return


class ShodanProperty:
    """
    封装每个对应的空间引擎所采集的字段
    """
    NAME = 'SHODAN'
    SUBDOMAIN = 'subdomain'
    TITLE = 'title'
    IP = 'ip'
    DOMAIN = 'domain'
    PORT = 'PORT'
    WEBSERVICE = 'web_service'
    PORTSERVICE = 'port_service'
    ASN = 'asn'

    def __init__(self):
        pass

    def getInfo(self):
        return


class NetSpider(BaseSpider):
    def __init__(self, domain, name):
        super().__init__()
        self.source = 'WebspaceSpider'
        self.domain = domain
        self.name = name

        self.tb_name = 'domain_webspace'

        self.fofaAddr = "https://fofa.info/api/v1/search/all?email={USER_NAME}&key={API_KEY}&qbase64={B64_DATA}&fields=host,ip,domain,port,server,protocol,as_number,title&size=10000"
        self.shodanAddr = "https://api.shodan.io/shodan/host/search?key={API_KEY}&query={QUERY}&minify=true&page=1"
        self.quakeAddr = "https://quake.360.cn/api/v3/search/quake_service"
        self.hunterAddr = "https://hunter.qianxin.com/openApi/search?username={USER_NAME}&api-key={API_KEY}&search={B64_DATA}&page={PAGE}&page_size=100"

        self.asn_list = []
        self.ip_list = []
        self.ip_port_list = []

        self.fofa_api = config_dict['fofa']['fofa_api']
        self.fofa_user = config_dict['fofa']['fofa_email']
        self.hunter_api = config_dict['hunter']['hunter_api']
        self.hunter_name = config_dict['hunter']['hunter_name']
        self.quake_api = config_dict['quake']
        self.shodan_api = config_dict['shodan']


    async def _init(self):
        is_get_favicon_md5 = await self._get_favicon_and_md5()
        # is_get_beian_company = self._get_beian_company()

        self.fofa_keyword_list = ['domain="{}"'.format(self.domain), 'host="{}"'.format(self.domain),
                                  'cert="{}"'.format(self.domain)]
        self.quake_keyword_list = ['domain:"{}"'.format(self.domain), 'host:"{}"'.format(self.domain),
                                   'cert:"{}"'.format(self.domain)]
        self.shodan_keyword_list = ['hostname:"{}"'.format(self.domain), 'ssl:"{}"'.format(self.domain)]
        self.hunter_keyword_list = ['domain="{}"'.format(self.domain), 'cert="{}"'.format(self.domain)]

        if is_get_favicon_md5:
            self.fofa_keyword_list.append('icon_hash="{}"'.format(self.favicon_mmh3_hash))
            self.quake_keyword_list.append('favicon:"{}"'.format(self.favicon_md5))
            self.shodan_keyword_list.append('http.favicon.hash:{}'.format(self.favicon_mmh3_hash))
            self.hunter_keyword_list.append('web.icon="{}"'.format(self.favicon_md5))

    async def _get_favicon_and_md5(self):
        favicon_md5 = False
        favicon_codecs = False
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(get_url(self.domain) + '/favicon.ico', headers=self.headers, timeout=5,
                                       verify_ssl=False) as response:
                    if response.status == 200:
                        m1 = hashlib.md5()
                        content = await response.read()
                        m1.update(content)
                        favicon_md5 = m1.hexdigest()
                        favicon_codecs = codecs.encode(content, 'base64')
                        self.favicon_mmh3_hash = mmh3.hash(favicon_codecs)
                        self.favicon_md5 = favicon_md5
                    else:
                        raise Exception from None
            except Exception as e:
                gLogger.myscan_error('_get_favicon_and_md5 first failed, error is {}'.format(e.args))
                gLogger.myscan_warn('_get_favicon_and_md5 second ...')
                try:
                    async with session.get(get_url('www.' + self.domain) + '/favicon.ico', headers=self.headers,
                                           timeout=5, verify_ssl=False) as response_:
                        if response_.status == 200:
                            m1_ = hashlib.md5()
                            content_ = await response_.read()
                            m1_.update(content_)
                            favicon_md5 = m1_.hexdigest()
                            favicon_codecs = codecs.encode(content_, 'base64')
                            self.favicon_mmh3_hash = mmh3.hash(favicon_codecs)
                            self.favicon_md5 = favicon_md5
                        else:
                            raise Exception from None
                except Exception as e:
                    favicon_md5 = False
                    favicon_codecs = False
                    gLogger.myscan_error('_get_favicon_and_md5 second failed, the error is {}'.format(e.args))

        if favicon_md5 and favicon_codecs:
            if self.favicon_md5 in COMMON_FAVICON_LIST:
                return False
            gLogger.myscan_info('get iconHash: %s' % self.favicon_mmh3_hash)
            gLogger.myscan_info('get iconMD5: %s' % self.favicon_md5)
            return True
        return False

    # def _get_beian_company(self):
    #     beian = False
    #     async with aiohttp.ClientSession() as session:
    #         try:
    #             url = 'https://micp.chinaz.com/?query={}'.format(self.domain)
    #             text = AsyncFetcher.fetch(session=session, url=url, headers=self.headers, timeout=5)
    #             if text is not None:
    #                 html = etree.HTML(text)
    #                 company_name = html.xpath('//*[@id="icp-cont"]/div[4]/table/tbody/tr[1]/td[2]/text()')
    #                 if company_name == '':
    #                     company_name = 'xxxxxxxxxxxxxxx'
    #                 beian = company_name[0]
    #         except IndexError as e:
    #             beian = False
    #             gLogger.myscan_error('curl beian no company, the error is {}'.format(e.args))
    #         except Exception as e:
    #             beian = False
    #             gLogger.myscan_error('curl chinaz.com error, the error is {}'.format(e.args))
    #     if beian:
    #         self.beian = beian
    #         return True
    #     return False

    async def fofa_domain_spider(self):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            for keyword in self.fofa_keyword_list:
                url, domain_list = self.fofaAddr.format(USER_NAME=self.fofa_user, API_KEY=self.fofa_api, B64_DATA=base64.b64encode(keyword.encode()).decode()), []
                try:
                    ret_json = await AsyncFetcher.fetch(session=session, url=url, json=True)
                    if 'FOFA Query Syntax Incorrect' in str(ret_json):
                        raise NetSyntaxError('query syntax incorrect') from None
                    elif 'Account Invalid' in str(ret_json):
                        raise NetTokenError("query token error") from None
                    elif 'must be between' in str(ret_json):
                        raise NetPageLimitError("page limit error") from None
                    elif 'F Coins Insufficient' in str(ret_json):
                        raise NetPrivilegeError("privilege error") from None
                    result = ret_json.get('results', '')
                    if result:
                        for _ in result:
                            host, ip, domain, port, server, protocol, as_number, title = _[0], _[1], _[2], _[3], _[4], _[5], _[6], _[7]
                            subdomain = host.split('//')[1] if 'http' in host else host
                            port_service = get_port_service(port) if server == '' else protocol
                            subdomain_info = {'id': 'NULL', 'domain_id': self.name,
                                              'spider': 'FOFA', 'subdomain': subdomain, 'title': title,
                                              'ip_port': '{}:{}'.format(str(ip), str(port)), 'domain': domain,
                                              'web_service': server, 'port_service': port_service, 'asn': as_number,
                                              'search_keyword': keyword.replace('"', '\\"')}
                            self.ip_list.append(ip)
                            self.asn_list.append(str(as_number))
                            self.res_list.append(subdomain)
                            domain_list.append(subdomain_info)
                except NetPageLimitError as e:
                    gLogger.myscan_error('FofaSearch - {} - {}'.format(keyword, e.__str__()))
                    return
                except NetPrivilegeError as e:
                    gLogger.myscan_error('FofaSearch - {} - {}'.format(keyword, e.__str__()))
                    return
                except NetSyntaxError as e:
                    gLogger.myscan_error('FofaSearch - {} - {}'.format(keyword, e.__str__()))
                    return
                except NetTokenError as e:
                    gLogger.myscan_error('FofaSearch - {} - {}'.format(keyword, e.__str__()))
                    return
                except Exception as e:
                    gLogger.myscan_error('FofaSearch - {} - {}'.format(keyword, e.args))
                    continue

                gLogger.myscan_info('Fofa - {} - catch success'.format(keyword))
                self._flush_result(domain_list)
                # self.write_file(self.get_unique_list(domain_list), 8)
                self.write_db(self.get_unique_list(domain_list))

    async def hunter_domain_spider(self):
        """write time: 2021.11.24 0.12 - zpchcbd"""
        # host, title, ip, domain, port, server, protocol, as_number
        async with aiohttp.ClientSession() as session:
            for keyword in self.hunter_keyword_list:
                domain_list, page = [], 1
                url = self.hunterAddr.format(USER_NAME=self.hunter_name, API_KEY=self.hunter_api, B64_DATA=base64.urlsafe_b64encode(keyword.encode()).decode(), PAGE=page)
                try:
                    ret_json = await AsyncFetcher.fetch(session=session, url=url, json=True)
                    if ret_json['code'] == 401:
                        raise NetPrivilegeError from None
                    if ret_json['code'] == 400:
                        raise NetPageLimitError from None
                    if ret_json['code'] == 40204:
                        raise NetIntegralError from None
                    pages = (ret_json['data'].get('total', 0)) // 100 + 1
                    while page <= pages:
                        url = self.hunterAddr.format(USER_NAME=self.hunter_name, API_KEY=self.hunter_api, B64_DATA=base64.urlsafe_b64encode(keyword.encode()).decode(), PAGE=page)
                        ret_json = await AsyncFetcher.fetch(session=session, url=url, json=True)
                        if ret_json['code'] == 401:
                            raise NetPrivilegeError("privilege error") from None
                        if ret_json['code'] == 400:
                            raise NetPageLimitError("page limit error") from None
                        if ret_json['code'] == 40204:
                            raise NetIntegralError("integral limit error") from None
                        result = ret_json['data'].get('arr', '')
                        if result:
                            for _ in result:
                                hunter = HunterProperty(_, keyword)
                                self.ip_list.append(hunter.ip)
                                self.res_list.append(hunter.subdomain)
                                domain_list.append(
                                    {
                                        'id': 'NULL',
                                        'domain_id': self.name,
                                        NetProperty.SPIDER_FIELD: hunter.name,
                                        NetProperty.SUBDOMAIN_FIELD: hunter.subdomain,
                                        NetProperty.TITLE_FIELD: hunter.title,
                                        NetProperty.IP_PORT_FIELD: '{}:{}'.format(hunter.ip, hunter.port),
                                        NetProperty.DOMAIN_FIELD: hunter.root_domain,
                                        NetProperty.WEBSERVICE_FIELD: str(hunter.webService),
                                        NetProperty.PORTSERVICE_FIELD: hunter.portService,
                                        NetProperty.ASN_FIELD: hunter.asn,
                                        NetProperty.SEARCHKEYWORD: hunter.keyword.replace('"', '\\"')
                                    }
                                )
                        page += 1
                except NetPageLimitError as e:
                    gLogger.myscan_error('HunterSearch - {} - {}'.format(keyword, e.__str__()))
                    return
                except NetPrivilegeError as e:
                    gLogger.myscan_error('HunterSearch - {} - {}'.format(keyword, e.__str__()))
                    return
                except NetSyntaxError as e:
                    gLogger.myscan_error('HunterSearch - {} - {}'.format(keyword, e.__str__()))
                    return
                except NetTokenError as e:
                    gLogger.myscan_error('HunterSearch - {} - {}'.format(keyword, e.__str__()))
                    return
                except NetIntegralError as e:
                    gLogger.myscan_error('HunterSearch - {} - {}'.format(keyword, e.__str__()))
                    return
                except Exception as e:
                    gLogger.myscan_error('HunterSearch - {} - {}'.format(keyword, e.__str__()))
                    continue

                gLogger.myscan_info('HunterSearch - {} - catch success'.format(keyword))
                self._flush_result(domain_list)
                # self.write_file(self.get_unique_list(domain_list), 9)
                self.write_db(self.get_unique_list(domain_list))

    async def quake_domain_spider(self):
        headers = {'X-QuakeToken': self.quake_api, 'Content-Type': 'application/json'}
        async with aiohttp.ClientSession(headers=headers) as session:
            for keyword in self.quake_keyword_list:
                domain_list, params = [], {'query': keyword, 'size': 2000, 'ignore_cache': True, 'include': ['ip', 'port', 'asn', 'service.name', 'service.http.host', 'service.http.title']}
                try:
                    ret_json = await AsyncFetcher.post_fetch(session=session, url=self.quakeAddr,
                                                             data=json.dumps(params), json=True)
                    for _ in ret_json['data']:
                        # http_module = _['service'].get('name', '')  # http， http-simple-new
                        http_module, ip, port, port_service, asn = _['service'].get('name', ''), _.get('ip', ''), _.get('port', ''), get_port_service(_.get('port', '')), _.get('asn', '')
                        if 'http' in http_module:
                            http = _['service'].get('http', '')
                            if http:
                                subdomain_info = {
                                    'id': 'NULL',
                                    'domain_id': self.name,
                                    'spider': 'QUAKE',
                                    'subdomain': http.get('host', ''),
                                    'title': http.get('title', ''),
                                    'ip_port': '{}:{}'.format((str(ip)), str(port)),
                                    'domain': '',
                                    'web_service': '',
                                    'port_service': port_service,
                                    'asn': _['asn'],
                                    'search_keyword': keyword.replace('"', '\\"')
                                }
                                if _['ip'] == http['host']:
                                    self.ip_list.append(ip)
                                    self.asn_list.append(str(asn))
                                else:
                                    self.ip_list.append(ip)
                                    self.asn_list.append(str(asn))
                                    self.res_list.append(http['host'])
                                domain_list.append(subdomain_info)
                        else:
                            subdomain_info = {
                                'id': 'NULL',
                                'domain_id': self.name,
                                'spider': 'QUAKE',
                                'subdomain': '',
                                'title': '',
                                'ip_port': '{}:{}'.format(str(ip), str(port)),
                                'domain': '',
                                'web_service': '',
                                'port_service': port_service,
                                'asn': _['asn'],
                                'search_keyword': keyword.replace('"', '\\"')
                            }
                            self.ip_list.append(ip)
                            self.asn_list.append(str(asn))
                            domain_list.append(subdomain_info)
                except NetPageLimitError as e:
                    gLogger.myscan_error('QuakeSearch - {} - {}'.format(keyword, e.__str__()))
                    return
                except NetPrivilegeError as e:
                    gLogger.myscan_error('QuakeSearch - {} - {}'.format(keyword, e.__str__()))
                    return
                except NetSyntaxError as e:
                    gLogger.myscan_error('QuakeSearch - {} - {}'.format(keyword, e.__str__()))
                    return
                except NetTokenError as e:
                    gLogger.myscan_error('QuakeSearch - {} - {}'.format(keyword, e.__str__()))
                    return
                except Exception as e:
                    gLogger.myscan_error('QuakeSearch - {} - {}'.format(keyword, e.args))
                    continue

                gLogger.myscan_info('Quake - {} - catch success'.format(keyword))
                self._flush_result(domain_list)
                # self.write_file(self.get_unique_list(domain_list), 10)
                self.write_db(self.get_unique_list(domain_list))

    async def shodan_domain_spider(self):
        # 这里用shodan模块的原因是正常请求会存在cloudflare导致请求失败，具体原因没研究
        # 所以就直接用shodan模块会方便，但是会十分降低速度，无法避免
        shodan_api = Shodan(self.shodan_api)
        # ipinfo = api.host('8.8.8.8')
        for keyword in self.shodan_keyword_list:
            domain_list = []
            try:
                if keyword == 'ssl:"{}"'.format(self.domain):
                    count_info = shodan_api.count(keyword)
                    if count_info['total'] > 1000:
                        gLogger.myscan_info('hodan skip ssl search...')
                        continue
                for _ in shodan_api.search_cursor(keyword):
                    http_module = _['_shodan'].get('module', '')  # http， http-simple-new
                    if 'http' in http_module:
                        http = _.get('http', '')
                        if http:
                            subdomain_info = {
                                'id': 'NULL',
                                'domain_id': self.name,
                                'spider': 'SHODAN',
                                'subdomain': str(_['hostnames']),
                                'title': http['title'],
                                'ip_port': '{}:{}'.format(str(_['ip_str']), str(_['port'])),
                                'domain': '',
                                'web_service': http['server'],
                                'port_service': get_port_service(_['port']),
                                'asn': _['asn'][2:],
                                'search_keyword': keyword.replace('"', '\\"')
                            }
                            self.ip_list.append(_['ip_str'])
                            self.asn_list.append(int(_['asn'][2:]))
                            for _ in _['hostnames']:
                                self.res_list.append(_)
                            domain_list.append(subdomain_info)
                    else:
                        subdomain_info = {
                            'id': 'NULL',
                            'domain_id': self.name,
                            'spider': 'SHODAN',
                            'subdomain': str(_['hostnames']),
                            'title': '',
                            'ip_port': '{}:{}'.format(str(_['ip_str']), str(_['port'])),
                            # 'ip': str(_['ip_str']),
                            # 'port': str(_['port']),
                            'domain': '',
                            'web_service': '',
                            'port_service': get_port_service(_['port']),
                            'asn': _['asn'][2:],
                            'search_keyword': keyword.replace('"', '\\"')
                        }
                        self.ip_list.append(_['ip_str'])
                        self.asn_list.append(str(int(_['asn'][2:])))
                        if _['hostnames']:
                            for _ in _['hostnames']:
                                self.res_list.append(_)
                        domain_list.append(subdomain_info)
            except Exception as e:
                gLogger.myscan_error('ShodanSearch - {} - {}'.format(keyword, e.args))
                continue
            gLogger.myscan_info('Shodan - {} - catch success'.format(keyword))
            self._flush_result(domain_list)
            # self.write_file(self.get_unique_list(domain_list), 11)
            self.write_db(self.get_unique_list(domain_list))

    def _flush_result(self, domain_list):
        for i in domain_list:

            # 防止ipv6影响清洗数据
            if len(i['ip_port'].split(':')) > 2:
                continue

            _ip, _port = i['ip_port'].split(':')[0], i['ip_port'].split(':')[1]
            flag = True
            for j in self.ip_port_list:
                if j['ip'] == _ip:
                    flag = False
            if flag:
                self.ip_port_list.append({'ip': _ip, 'port': [int(_port)]})

        for j in domain_list:

            # 防止ipv6影响清洗数据
            if len(j['ip_port'].split(':')) > 2:
                continue

            _ip, _port = j['ip_port'].split(':')[0], j['ip_port'].split(':')[1]

            if int(_port) == 443 or int(_port) == 80:
                continue
            flag = True
            for k in self.ip_port_list:
                if k['ip'] == _ip:
                    for m in k['port']:
                        if int(m) == int(_port):
                            flag = False
            if flag:
                for p in self.ip_port_list:
                    if p['ip'] == _ip:
                        p['port'].append(int(_port))

    # 域名爬取处理函数
    async def spider(self):
        task_list = [
            asyncio.create_task(self.fofa_domain_spider()),
            asyncio.create_task(self.hunter_domain_spider()),
            asyncio.create_task(self.quake_domain_spider()),
            asyncio.create_task(self.shodan_domain_spider())
        ]
        await asyncio.gather(*task_list)
        self._is_continue = False

    # main start
    async def main(self):
        await self._init()
        await self.spider()
        self.res_list, self.asn_list, self.ip_list = list(set(self.res_list)), list(set(self.asn_list)), list(
            set(self.ip_list))
        return self.res_list, self.asn_list, self.ip_list, self.ip_port_list


if __name__ == '__main__':
    start = time.time()
    NetSpider('zjhu.edu.cn', 'test').main()
    print(time.time() - start)
