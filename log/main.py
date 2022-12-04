# -*- coding:utf-8 -*-
"""
@Author      :   Haorui Guo
@File        :   main.py
@Contact     :   12032793@mail.sustech.edu.cn
@Modify Time :   2022/12/4
"""

# general usage
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
a = 1
b = 2
logging.info('test param 1 %s and param 2 %s', a, b)
