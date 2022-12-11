# -*- coding:utf-8 -*-
"""
@Author      :   Haorui Guo
@File        :   practice.py
@Contact     :   12032793@mail.sustech.edu.cn
@Modify Time :   2022/12/9
"""
# 目标网站 https://antispider5.scrape.center/
# 1. 构造redis爬取队列，用队列存取请求，请求用Request对象表示，在存取时用pickle进行序列化和反序列化
# 2. 实现异常处理，把失败的请求重新加入队列
# 3. 解析列表页的数据，将爬取详情页和下一页的请求加入队列
# 4. 解析详情页的数据

TIMEOUT = 10
from requests import Request


class MovieRequest(Request):
    def __init__(self, url, callback, method='GET', headers=None, need_proxy=False, fail_time=0, timeout=TIMEOUT):
        Request.__init__(self, method, url, headers)
        self.callback = callback
        self.fail_time = fail_time
        self.timeout = timeout

