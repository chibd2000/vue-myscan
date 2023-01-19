from email.header import Header
from email.mime.text import MIMEText

from module.asynchttp import AsyncFetcher
from module.database import Database
from utils.conf_reader import get_database_conf, get_qq_mail_conf, get_weixin_mail_conf
from module.data import gLogger

import json
import smtplib
import aiohttp


def get_mail_type():
    db_conf = get_database_conf()
    db_conn = Database(db_conf)
    t = db_conn.select_one('mail_config', '1')
    return t['wake_type']


async def send_weixin_mail(content):
    conf = get_weixin_mail_conf()
    url_token = 'https://api.weixin.qq.com/cgi-bin/token?'
    url_custom_msg = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?'
    url_template_msg = 'https://api.weixin.qq.com/cgi-bin/message/template/send?'
    try:
        async with aiohttp.ClientSession() as session:
            ret_json = await AsyncFetcher.fetch(session=session, url=url_token, params={
                'grant_type': 'client_credential',
                'appid': conf['app_id'],
                'secret': conf['app_secret'],
            }, json=True)
            token = ret_json.get('access_token')
            if token:
                headers = {'Content-Type': 'application/json'}
                body = {"touser": conf['user_id'], "msgtype": "text", "text": {"content": content}}
                ret_json = await AsyncFetcher.post_fetch(session=session, url=url_custom_msg,
                                                         params={'access_token': token},
                                                         data=json.dumps(body, ensure_ascii=False).encode('utf-8'),
                                                         headers=headers, json=True)
                print(ret_json)
                if ret_json.get('errcode', 0) == 45047:
                    body = {"touser": conf['user_id'], "template_id": conf['template_id'],
                            "url": "http://weixin.qq.com/download",
                            "topcolor": '#FF0000', "data": {"text": {"value": content, "color": '#FF0000'}}}
                    await AsyncFetcher.post_fetch(session=session, url=url_template_msg, params={'access_token': token},
                                                  data=json.dumps(body, ensure_ascii=False).encode('utf-8'),
                                                  headers=headers, json=True)
    except Exception as e:
        gLogger.myscan_error(e.__str__())


def send_qq_mail(content):
    smtp_server = 'smtp.qq.com'
    try:
        mail_config = get_qq_mail_conf()
        to_addrs = mail_config['target'].split(',')
        from_addr = mail_config['sender']
        auth_password = mail_config['qq_mail_key']
        msg = MIMEText(str(content), 'plain', 'utf-8')
        msg['From'] = Header(mail_config['sender'])
        msg['To'] = Header(mail_config['receiver'])
        msg['Subject'] = Header('Github监控提醒')
        server = smtplib.SMTP_SSL(smtp_server)
        server.connect(smtp_server, 465)
        server.login(from_addr, auth_password)
        server.sendmail(from_addr, to_addrs, msg.as_string())
        server.quit()
    except Exception as e:
        gLogger.myscan_error(e.__str__())
