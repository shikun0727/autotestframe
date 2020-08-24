#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Author: yangshikun
@Data: 2020/8/18
@File: config.py
@Software: Pycharm
@version: Python 3.7.6
"""

import os
from utils.file_reader import YamlReader

'''
BASE_PATH: 当前工程的根目录
CONFIG_PATH: 配置文件config所在路径
DATA_PATH: 数据文件data所在路径
DRIVERS_PATH: 浏览器驱动所在路径
LOG_PATH: 日志文件路径
REPORT_PATH: 测试报告路径
UTILS_PATH: 公共方法路径
'''
BASE_PATH = os.path.split(os.path.dirname(__file__))[0]
CONFIG_PATH = os.path.join(BASE_PATH, 'config')
DATA_PATH = os.path.join(BASE_PATH, 'data')
DRIVERS_PATH = os.path.join(BASE_PATH, 'drivers')
LOG_PATH = os.path.join(BASE_PATH, 'log')
REPORT_PATH = os.path.join(BASE_PATH, 'report')
UTILS_PATH = os.path.join(BASE_PATH, 'utils')

class Config():
    '''创建一个Config类'''
    # 利用YamlReader类读取yaml文档中的内容，并初始化
    def __init__(self):
        self.data = YamlReader(os.path.join(CONFIG_PATH, 'config.yml')).data

    def get(self, element, index=0):
        return self.data[index].get(element)

if __name__ == '__main__':
    c = Config()
    print(c.get('log').get('log_file_name'))