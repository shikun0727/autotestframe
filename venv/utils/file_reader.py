#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Author: yangshikun
@Data: 2020/8/18
@File: file_reader.py
@Software: Pycharm
@version: Python 3.7.6
"""

import yaml, os

class YamlReader():
    '''创建一个读取yaml格式文件的类'''

    def __init__(self, yamlf):
        # 检查配置文件路径有效性
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError('{}文件不存在！'.format(yamlf))
        self._data = None

    @property
    def data(self):
        # 读取yaml文档的配置参数，返回列表
        # 如果是第一次调用data，读取yaml文档，否则直接返回之前保存的数据
        if not self._data:
            with open(self.yamlf) as f:
                self._data = list(yaml.safe_load_all(f))
            return self._data


if __name__ == '__main__':
    yr = YamlReader(r'D:\GitCode\autotestframe\venv\config\config.yml')
    print(yr.data)