# coding=utf-8
# @Author   : zpchcbd HG team
# @Time     : 2021-08-26 13:46

from core.data import gLogger, config_dict
from spider import BaseSpider
import aiohttp
import re


class BeianSpider(BaseSpider):
    def __init__(self, domain, name):
        super().__init__()
        self.domain = domain
        self.name = name
        self.tb_name = 'domain_beian'
        self.source = 'BeianSpider'
        self.addr1 = 'https://apidatav2.chinaz.com/single/icp?key={}&domain={}'
        self.addr2 = 'https://micp.chinaz.com/Handle/AjaxHandler.ashx?action=GetBeiansl&query={}&type=host'
        self.api = config_dict['chinaz'] if config_dict['chinaz'] else ''

    async def spider(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=self.addr1.format(self.api, self.domain), headers=self.headers, timeout=self.reqTimeout, verify_ssl=False, allow_redirects=False) as response:
                    if response is not None:
                        ret_json = await response.json()
                        company_name = ret_json['Result']['CompanyName'] if ret_json['Result']['CompanyName'] else ''
                        if company_name:
                            try:
                                async with session.get(url=self.addr2.format(self.domain), headers=self.headers, timeout=self.reqTimeout, verify_ssl=False, allow_redirects=False) as response2:
                                    text = await response2.text()
                                    beian_result = re.findall('SiteLicense:"([^"]*)",SiteName:"([^"]*)",MainPage:"([^"]*)",VerifyTime:"([^"]*)"',text)
                                    if beian_result:
                                        for _ in beian_result:
                                            beian_id, site_name, new_domain, time = _
                                            if new_domain.startswith('www.'):
                                                new_domain = new_domain.replace("www.", '')
                                            self.res_list.append({'id': 'NULL', 'domain_id': self.name, 'license': beian_id, 'sitename': site_name, 'domain': new_domain, 'verify_time': time})
                            except Exception as e:
                                gLogger.myscan_error('curl {} error, {}'.format(self.addr2, e.args))
                        else:
                            gLogger.myscan_error('没有匹配到公司名')
        except Exception as e:
            gLogger.myscan_error('curl BeianSpider error, {}'.format(self.addr1.format(self.domain), e.args))
        self._is_continue = False
        # self.write_file(self.get_unique_list(self.res_list), 0)
        self.write_db(self.res_list)
        gLogger.myscan_info('[{}] [{}] {}'.format(self.source, len(self.res_list), self.res_list))

    async def main(self):
        await self.spider()


if __name__ == '__main__':
    import asyncio
    beian = asyncio.get_event_loop().run_until_complete(BeianSpider('huolala.cn', '').main())
