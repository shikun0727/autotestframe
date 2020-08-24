#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Author: yangshikun
@Data: 2020/8/19
@File: log.py
@Software: Pycharm
@version: Python 3.7.6
"""

import os, logging
from logging.handlers import TimedRotatingFileHandler
from utils.config import Config, LOG_PATH

class Logger():
    '''
    使用logging日志模块重新封装一个Logger类
    WARNING级别的日志输出至控制台
    DEBUG级别的日志输出至文件
    '''
    def __init__(self):
        c = Config().get('log')
        self.logger = logging.getLogger(__name__)
        # 初始化日志级别为NOTSET
        logging.root.setLevel(logging.NOTSET)
        # 设置日志文件名称
        self.logger_file_name = c.get('log_file_name') if c.get('log_file_name') else 'test.log'
        # 设置最大保存的日志数量
        self.backup_count = c.get('backup_count') if c.get('backup_count') else 5
        # 设置日志输出级别
        self.console_output_level = c.get('console_lv') if c.get('console_lv') else 'WARNING'
        self.file_output_level = c.get('file_lv') if c.get('file_lv') else 'DEBUG'
        # 设置日志输出格式
        pattern = c.get('pattern') if c.get('pattern') else '%(asctime)s--%(name)s--%(levelname)s--%(message)s'
        self.formatter = logging.Formatter(pattern)

    def get_logger(self):
        if not self.logger.handlers:
            # 实例化控制台日志句柄，并设置级别和输出格式，并添加至logger中
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.console_output_level)
            console_handler.setFormatter(self.formatter)
            self.logger.addHandler(console_handler)
            # 实例化文件日志句柄，并设置级别和输出格式，并添加至logger中
            file_handler = TimedRotatingFileHandler(filename=os.path.join(LOG_PATH, self.logger_file_name),
                                                    when='D',
                                                    interval=1,
                                                    backupCount=self.backup_count,
                                                    delay=True,
                                                    encoding='utf-8'
                                                    )
            file_handler.setLevel(self.file_output_level)
            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)
        return self.logger

logger = Logger().get_logger()

if __name__ == '__main__':
    logger.debug('这是一个debug')
    logger.info('这是一个info')
    logger.warning('这是一个warining')
    logger.error('这是一个error')