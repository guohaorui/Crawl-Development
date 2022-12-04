# -*- coding:utf-8 -*-
"""
@Author      :   Haorui Guo
@File        :   multi_coroutine4.py
@Contact     :   12032793@mail.sustech.edu.cn
@Modify Time :   2022/12/4
"""
from utils import *


async def request():
    url = 'https://www.baidu.com'
    status = requests.get(url)
    return status


tasks = [asyncio.ensure_future(request()) for _ in range(5)]
print('Tasks', tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

for task in tasks:
    print('Task results:', task.result())
