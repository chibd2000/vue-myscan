# coding=utf-8
from core.component.variablemanager import GlobalVariableManager
from spider import BaseSpider
from core.utils.tools import is_subdomain
import functools
import asyncio
import aiodns

resolver_nameservers = ['114.114.114.114', '114.114.115.115']
resolver_timeout = 5.0
limit_resolve_conn = 100


def aiodns_resolver():
    return aiodns.DNSResolver(nameservers=resolver_nameservers, timeout=resolver_timeout)


class Domain2ipSpider(BaseSpider):
    def __init__(self, domain, name, domain_list):
        super().__init__()
        self.source = 'Domain2ipSpider'
        self.tb_name = 'domain_subdomain'
        self.domain = domain
        self.name = name
        for _ in domain_list:
            if is_subdomain(_, domain):
                self.res_list.append(
                    {'id': 'NULL', 'domain_id': self.name, 'subdomain': _, 'resolve_type': 'A记录', 'ip': ''})

    def resolve_callback(self, future, index, datas):
        try:
            result = future.result()
        except Exception as e:
            datas[index]['ip'] = ''  # 解析错误会默认返回空， 获取报错信息str(e.args)
        else:
            if isinstance(result, tuple):
                _, answers = result
                if answers:
                    ips = answers[0].host  # 这里解析到的ip就拿一个
                    datas[index]['ip'] = str(ips)

    async def aiodns_query_a(self, hostname, semaphore=None):
        if semaphore is None:
            resolver = aiodns_resolver()
            answers = await resolver.query(hostname, 'A')
            return hostname, answers
        else:
            async with semaphore:
                resolver = aiodns_resolver()
                answers = await resolver.query(hostname, 'A')
                return hostname, answers

    async def bulk_query_a(self):
        task_list = []
        semaphore = asyncio.Semaphore(limit_resolve_conn)
        for i, data in enumerate(self.res_list):
            if not data.get('ip'):
                subdomain = data.get('subdomain')
                task = asyncio.ensure_future(self.aiodns_query_a(subdomain, semaphore))
                task.add_done_callback(functools.partial(self.resolve_callback, index=i, datas=self.res_list))  # 回调填充
                task_list.append(task)

        if task_list:  # 任务列表里有任务不空时才进行解析
            await asyncio.wait(task_list)  # 等待所有task完成

    async def spider(self):
        await self.bulk_query_a()
        self.res_list = self.get_unique_list(self.res_list)
        self._is_continue = False
        self.write_db(self.res_list)
        # self.write_file(self.get_unique_list(self.res_list), 4)

    async def main(self):
        await self.spider()
        return self.res_list


if __name__ == '__main__':
    domainList = ['test.com']
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    dddd = Domain2ipSpider('zjhu.edu.cn', 'test', domainList)
    t = loop.run_until_complete(dddd.main())
    print(t)
