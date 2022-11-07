#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/8 3:16
# @Author  : Haorui Guo
# @File    : xpath.py

# / 选取子节点
# //选取子孙节点
# @ 选取属性

from lxml import etree

html = etree.parse('./ex.html',etree.HTMLParser())
result = etree.tostring(html)
# print(result.decode('utf-8'))

# 选取节点下的text,注意返回的是列表
element = html.xpath('//*[@id="post-8489"]/header/h2/a')[0]
print(element.text)
# 选取节点对应的属性
print(str(html.xpath('//*[@id="post-8489"]/header/h2/a/@href')[0]))
# contains 属性多值匹配
element = html.xpath('//div[contains(@class,"archive-content")]')[0]
d = 1
# 多属性匹配
element = html.xpath('//a[@title="Jack Cui" and @rel="home"]')[0]