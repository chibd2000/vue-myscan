# coding=utf-8
# @Author   : zpchcbd HG team
# @Time     : 2021-10-11 18:30
from core.data import config_dict
import random
import aiohttp
import asyncio

from core.request.asynchttp import AsyncFetcher


class ProxyProvider(object):
    def __init__(self, keywords):
        self.addr = 'https://api.proxyscrape.com/?request=displayproxies&proxytype=http&country=all&anonymity=all&ssl=yes&timeout=10000'
        self.verifyAddr = 'https://aiqicha.baidu.com/detail/icpinfoajax?p=1&size=20&pid=66382451531594'
        self.proxyAddrList = []
        self.enableProxyList = []
        self.keywords = keywords

    async def getProxy(self):
        try:
            async with aiohttp.ClientSession() as session:
                text = await AsyncFetcher.fetch(session=session, url=self.addr, timeout=10)
                if text is not None:
                    self.proxyAddrList = [x for x in text.split('\r\n') if x != '']
                    print('[+] api.proxyscrape.com grabbed proxy.')
                else:
                    print('[-] api.proxyscrape.com No proxy.')
            print('[+] verifying proxy is enable...')
            await self.testProxy()
        except aiohttp.ClientHttpProxyError:
            print('[-] curl api.proxyscrape.com need outer proxy.')
            return []
        except asyncio.TimeoutError:
            print("[-] curl {} Timeout, check your proxy.".format(self.addr))
        except Exception as e:
            pass
            # print("[-] curl {} error, {}".format(self.addr, e.__str__()))

    async def verifyProxy(self, session, testHttp):
        try:
            # print(testHttp)
            async with session.get(url=self.verifyAddr, verify_ssl=False, timeout=10, proxy=testHttp) as response:
                if response is not None and response.status == 200:
                    text = await response.text()
                    if self.keywords in text:
                        self.enableProxyList.append(testHttp)
        except asyncio.TimeoutError:
            print("[-] curl {} Timeout.".format(testHttp))
        except Exception as e:
            pass
            # print("[-] curl {} error, {}".format(testHttp, e.__str__()))

    async def testProxy(self):
        task_list = []
        async with aiohttp.ClientSession() as session:
            for _ in self.proxyAddrList:
                a_proxy = f'http://{_}'
                task_list.append(asyncio.create_task(self.verifyProxy(session, a_proxy)))
            await asyncio.gather(*task_list)
        print(self.enableProxyList)

    def getRandomOneProxy(self):
        # print(len(self.enableProxyList))
        return self.enableProxyList[random.randint(1, len(self.enableProxyList)-1)]

    def getAllProxy(self):
        return self.enableProxyList


if __name__ == '__main__':
    spider = ProxyProvider('')
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(spider.getProxy())
