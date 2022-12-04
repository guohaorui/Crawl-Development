# -*- coding:utf-8 -*-
"""
@Author      :   Haorui Guo
@File        :   aiohttp_params6.py
@Contact     :   12032793@mail.sustech.edu.cn
@Modify Time :   2022/12/4
"""
from utils import *


async def main():
    params = {'name': 'henry', 'age': 18}
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.httpbin.org/get', params=params) as response:
            print(await response.text())


if __name__ == '__main__':
    asyncio.run(main())
