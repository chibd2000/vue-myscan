# coding=utf-8
# @Author   : zpchcbd HG team
# @Time     : 2021-08-26 0:01

from core.request.asynchttp import AsyncFetcher
from core.data import gLogger, config_dict
from spider import BaseSpider
import aiohttp


class Jldc(BaseSpider):
    def __init__(self, domain):
        super().__init__()
        self.domain = domain
        self.addr = 'https://jldc.me/anubis/subdomains/{}'
        self.source = 'jidc'

    async def spider(self):
        gLogger.myscan_debug('Load {} api ...'.format(self.source))
        try:
            async with aiohttp.ClientSession() as session:
                text = await AsyncFetcher.fetch(session=session, url=self.addr.format(self.domain))
                result = eval(text)
                if result:
                    for _ in result:
                        self.res_list.append(_)
                else:
                    gLogger.myscan_warn('jldc api no subdomains.')
        except Exception as e:
            gLogger.myscan_error('curl jldc.me api error, the error is {}'.format(e.args))
        self._is_continue = False
        self.res_list = list(set(self.res_list))
        gLogger.myscan_info('[{}] [{}] {}'.format(self.source, len(self.res_list), self.res_list))
        return self.res_list


async def do(domain):
    alien = Jldc(domain)
    res = await alien.spider()
    return res

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(do('baidu.com'))
