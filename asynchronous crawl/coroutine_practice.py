# -*- coding:utf-8 -*-
"""
@Author      :   Haorui Guo
@File        :   coroutine_practice.py
@Contact     :   12032793@mail.sustech.edu.cn
@Modify Time :   2022/12/4
"""
from utils import *

import time

start = time.time()
URL = 'https://www.httpbin.org/delay/5'


async def get(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    await response.text()
    await session.close()
    return response


async def request():
    print('Waiting for ', URL)
    response = await get(URL)
    print('Get response from ', URL, 'response', response)


tasks = [asyncio.ensure_future(request()) for _ in range(5)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
end = time.time()
print('Cost time', end - start)
