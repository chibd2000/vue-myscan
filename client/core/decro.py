from core.component.variablemanager import GlobalVariableManager


def db_update_status(tb_name):
    def inner(func):
        async def wrapper(*args, **kwargs):
            g_db = GlobalVariableManager.get_value('g_db')
            g_db.update(tb_name, {'name': '"aaaa"'}, 'domain_id="f236550506b0411aea1e8b1eff05392"')
            await func(*args, **kwargs)
        return wrapper
    return inner

# def async_decorators(method):
#     @functools.wraps(method)
#     async def wrapper(*args, **kwargs):
#         await method(*args, **kwargs)
#
#     return wrapper
#
#
# @db_record_domain('domain_webtitle')
# async def test(time):
#     await asyncio.sleep(time)
#
#
# if __name__ == '__main__':
#     asyncio.get_event_loop().run_until_complete(test(2))
