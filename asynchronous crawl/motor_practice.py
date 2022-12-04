# -*- coding:utf-8 -*-
"""
@Author      :   Haorui Guo
@File        :   motor_practice.py
@Contact     :   12032793@mail.sustech.edu.cn
@Modify Time :   2022/12/5
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_CONNECTION_STRING = 'mongodb://admin:123456@180.76.106.23:27017'
MONGO_DB_NAME = 'crawl_test'
MONGO_COLLECTION_NAME = 'spa5_books'
client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]


async def save(num):
    await collection.update_one({
        'id': num
    }, {
        '$set': {num: num}
    }, upsert=True)


if __name__ == '__main__':
    asyncio.run(save('1'))
