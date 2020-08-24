#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Author: yangshikun
@Data: 2020/8/18
@File: test_baidu.py
@Software: Pycharm
@version: Python 3.7.6
"""

import time, unittest, traceback, os
from selenium import webdriver
from utils.config import Config, DATA_PATH
from utils.log import logger
from utils.file_reader import Excel_Reader

class TestBaidu(unittest.TestCase):
    '''创建一个TestBaidu的测试类'''
    def setUp(self):
        self.url = Config().get('URL')
        driver_path = Config().get('driver')
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)
        self.excel = os.path.join(DATA_PATH, 'data.xlsx')
        self.driver.get(self.url)
        time.sleep(2)

    def tearDown(self):
        self.driver.quit()

    def test_baidu(self):
        datas = Excel_Reader(self.excel).data
        for row_data in datas:
            with self.subTest(data=row_data):
                self.driver.find_element_by_id('kw').clear()
                self.driver.find_element_by_id('kw').send_keys(row_data[0])
                self.driver.find_element_by_id('su').click()
                time.sleep(2)
                title = self.driver.title
                try:
                    self.assertEqual(title, row_data[1])
                    logger.info('页面标题：{}'.format(title))
                except AssertionError:
                    logger.error('搜索页面与预期不符\n{}'.format(traceback.format_exc()))
                    raise AssertionError

if __name__ == '__main__':
    unittest.main(verbosity=2)