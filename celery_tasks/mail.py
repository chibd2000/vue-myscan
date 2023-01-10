import asyncio

from celery_tasks.main import cel
from module.mail import get_mail_type
from module.mail import send_qq_mail, send_weixin_mail


def run_async(coro):
    return asyncio.run(coro)


@cel.task()
def send_mail(content):
    type = get_mail_type()
    if type == 'qq':
        send_qq_mail(content)
    elif type == 'weixin':
        run_async(send_weixin_mail(content))
    return 'ok'
