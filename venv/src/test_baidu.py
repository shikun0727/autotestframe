#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Author: yangshikun
@Data: 2020/8/18
@File: test_baidu.py
@Software: Pycharm
@version: Python 3.7.6
"""

import time, unittest, traceback
from selenium import webdriver
from utils.config import Config
from utils.log import logger

class TestBaidu(unittest.TestCase):
    '''创建一个TestBaidu的测试类'''
    def setUp(self):
        self.url = Config().get('URL')
        driver_path = Config().get('driver')
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)

    def tearDown(self):
        self.driver.quit()

    def test_baidu(self):
        self.driver.get(self.url)
        time.sleep(2)
        self.driver.find_element_by_id('kw').send_keys('python')
        self.driver.find_element_by_id('su').click()
        time.sleep(2)
        title = self.driver.title
        try:
            self.assertEqual(title, 'python_百度搜索1')
        except AssertionError:
            logger.error('搜索页面与预期不符\n{}'.format(traceback.format_exc()))
            raise AssertionError

if __name__ == '__main__':
    unittest.main()