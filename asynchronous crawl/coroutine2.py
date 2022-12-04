# -*- coding:utf-8 -*-
"""
@Author      :   Haorui Guo
@File        :   coroutine2.py
@Contact     :   12032793@mail.sustech.edu.cn
@Modify Time :   2022/12/4
"""
import asyncio


async def execute(x):
    print('Number ', x)


# 最完整的声明就是
# 1. 获取coroutine
coroutine = execute(1)
print('Coroutine', coroutine)
print('After calling execute')
# 2. 声明loop
loop = asyncio.get_event_loop()
# 3. 将coroutine声明成task，task多了运行状态如running, finished等
task = asyncio.ensure_future(coroutine)
print('Task', task)
loop.run_until_complete(task)
print('Task', task)
print('After calling loop')
# python3.7 之后就不需要显式的声明loop了直接运行下面一句就行
# asyncio.run(execute(1))
