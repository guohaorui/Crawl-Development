#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/8 3:33
# @Author  : Haorui Guo
# @File    : bs.py

# 支持html，xml
from bs4 import BeautifulSoup

soup = BeautifulSoup('./ex.html','lxml')
print(soup.prettify())
print(soup.title.string)
d = 1