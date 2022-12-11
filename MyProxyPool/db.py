# -*- coding:utf-8 -*-
"""
@Author      :   Haorui Guo
@File        :   db.py
@Contact     :   12032793@mail.sustech.edu.cn
@Modify Time :   2022/12/9
"""
from redis import StrictRedis
from pickle import dumps, loads
from practice import MovieRequest

REDIS_HOST = '180.76.106.23'
REDIS_PASSWORD = 'guohaorui'
REDIS_PORT = 6379
REDIS_KEY = 'anti_scrape5'


class RedisQueue():
    def __init__(self):
        self.db = StrictRedis(host=REDIS_HOST, password=REDIS_PASSWORD, port=REDIS_PORT)

    def add(self, req):
        if isinstance(req, MovieRequest):
            return self.db.rpush(REDIS_KEY, dumps(req))
        return False

    def pop(self):
        if self.db.llen(REDIS_KEY):
            return loads(self.db.lpop(REDIS_KEY))
        return False

    def empty(self):
        return self.db.llen(REDIS_KEY) == 0
