# coding=utf-8
# @Author   : zpchcbd HG team
# @Blog     : https://www.cnblogs.com/zpchcbd/
# @Time     : 2020-11-23 20:45
from core.component.targetmanager import TargetManager
from argparse import ArgumentParser
from core.component.variablemanager import GlobalVariableManager

import time
import asyncio
import sys

from core.myenums import TASK_STATUS

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def start(parser: ArgumentParser):
    loop = asyncio.get_event_loop()
    args = parser.parse_args()
    task_name = args.taskflag
    try:

        g_db = GlobalVariableManager.get_value('g_db')
        g_db.update_task_status(2, task_name)
        g_db.update_task_module_status(TASK_STATUS.LOADING, task_name)
        g_db.update_task_start_time(int(time.time()), task_name)

        target_manager = TargetManager.create_target_manager(task_name, parser)
        loop.run_until_complete(target_manager.search())
        loop.run_until_complete(target_manager.scan())

        g_db.update_task_status(1, task_name)
        g_db.update_task_module_status(TASK_STATUS.SUCCESS, task_name)
        g_db.update_task_end_time(int(time.time()), task_name)
    except KeyboardInterrupt:
        pass
