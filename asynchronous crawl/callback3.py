# -*- coding:utf-8 -*-
"""
@Author      :   Haorui Guo
@File        :   callback3.py
@Contact     :   12032793@mail.sustech.edu.cn
@Modify Time :   2022/12/4
"""

import asyncio
import requests


async def request():
    url = 'https://www.baidu.com'
    status = requests.get(url)
    return status


def callback(task):
    print('Status ', task.result())


coroutine = request()
task = asyncio.ensure_future(coroutine)
task.add_done_callback(callback)
print('Task ', task)

loop = asyncio.get_event_loop()
loop.run_until_complete(task)
print('Task ', task)
