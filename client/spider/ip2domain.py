# coding=utf-8

from core.data import gLogger
from core.request.asynchttp import AsyncFetcher
from spider import BaseSpider
from ipaddress import ip_address
import aiohttp
import asyncio
import functools

limit_resolve_conn = 1


class Ip2domainSpider(BaseSpider):
    def __init__(self, domain, name, ip_list):
        super().__init__()
        self.name = name
        self.tb_name = 'domain_ip'
        self.source = 'Ip2domainSpider'
        self.domain = domain
        self.addr = 'https://api.webscan.cc/?action=query&ip={}'
        self.ip2domain_list = list()
        self.ip_list = list()
        for ip in ip_list:
            try:
                if ip_address(ip) and ip_address(ip).is_private:
                    gLogger.myscan_warn('scan host: %s is private, so skip it' % str(ip))
                    continue
                self.ip_list.append(ip)
                self.ip2domain_list.append({'id': 'NULL', 'domain_id': self.name, 'ip': ip, 'ip2domain': ''})
            except Exception:
                pass

    def resolve_callback(self, future, index, datas):
        try:
            result = future.result()
        except Exception as e:
            datas[index]['ip2domain'] = ''  # 解析错误会默认返回空， 获取报错信息str(e.args)
        else:
            if isinstance(result, list):
                if result:
                    datas[index]['ip2domain'] = ','.join(result)

    async def get_subdomain(self, semaphore, ip):
        try:
            async with semaphore:
                async with aiohttp.ClientSession() as session:
                    text = await AsyncFetcher.fetch(session=session, url=self.addr.format(ip), headers=self.headers)
                    if text != 'null':
                        results = eval(text)
                        domains = []
                        for each in results:
                            domains.append(each['domain'])
                            if self.domain in each['domain']:
                                self.res_list.append(each['domain'])
                        return domains
        except Exception as e:
            gLogger.myscan_error('curl api.webscan.cc error, the error is {}'.format(e.args))

    async def resolve(self):
        task_list = []
        semaphore = asyncio.Semaphore(limit_resolve_conn)
        for i, ip in enumerate(self.ip_list):
            task = asyncio.ensure_future(self.get_subdomain(semaphore, ip))
            task.add_done_callback(functools.partial(self.resolve_callback, index=i, datas=self.ip2domain_list))  # 回调填充
            task_list.append(task)
        if task_list:  # 任务列表里有任务不空时才进行解析
            await asyncio.wait(task_list)  # 等待所有task完成

    async def spider(self):
        await self.resolve()
        self._is_continue = False
        self.write_db(self.get_unique_list(self.ip2domain_list))
        self.res_list = list(set(self.res_list))
        gLogger.myscan_info('[{}] [{}] {}'.format(self.source, len(self.res_list), self.res_list))

    async def main(self):
        await self.spider()
        return self.res_list


if __name__ == '__main__':
    testList = ['61.153.52.11', '61.153.52.74', '61.153.52.57', '61.153.52.20', '211.80.146.74', '61.153.52.23',
                '211.80.146.57', '61.153.52.103', '61.153.52.24', '61.153.52.21', '61.153.52.68', '61.153.52.52']
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    w = Ip2domainSpider('zjhu.edu.cn', 'aaaaaass123', testList)
    t = loop.run_until_complete(w.main())
    print(t)
