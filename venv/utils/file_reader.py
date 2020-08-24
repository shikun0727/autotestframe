#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Author: yangshikun
@Data: 2020/8/18
@File: file_reader.py
@Software: Pycharm
@version: Python 3.7.6
"""

import yaml, os, xlrd

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

class SheetTypeError(Exception):
    '''自定义一个异常类'''
    pass

class Excel_Reader():
    '''创建一个读取.xlsx格式文件的类'''
    def __init__(self, excel_file, sheet=0, title_line=True):
        if os.path.exists(excel_file):
            self.excel = excel_file
        else:
            raise FileNotFoundError('{}文件不存在！'.format(excel_file))
        self.sheet = sheet
        self.title_line = title_line
        self._data = []

    @property
    def data(self):
        if not self._data:
            workbook = xlrd.open_workbook(self.excel)
            if type(self.sheet) not in [int, str]:
                raise SheetTypeError('Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))
            elif type(self.sheet) is int:
                sheet_data = workbook.sheet_by_index(self.sheet)
            elif type(self.sheet) is str:
                sheet_data = workbook.sheet_by_name(self.sheet)
            # 判断title_line为True，则从第二行开始取值，反之则从第一行开始取值
            if self.title_line:
                # sheet_data.nrows表格最大行数，sheet_data.ncols表格最大列数
                for row in range(1, sheet_data.nrows):
                    # row_values(row)取整行的值，col_values(col)取整列的值
                    self._data.append(sheet_data.row_values(row))
            else:
                for row in range(sheet_data.nrows):
                    self._data.append(sheet_data.row_values(row))
        return self._data

if __name__ == '__main__':
    #yr = YamlReader(r'D:\GitCode\autotestframe\venv\config\config.yml')
    #print(yr.data)
    from utils.config import DATA_PATH
    er = Excel_Reader(os.path.join(DATA_PATH, 'data.xlsx'))
    print(er.data[0][0])