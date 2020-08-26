#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Author: yangshikun
@Data: 2020/8/25
@File: mail.py.py
@Software: Pycharm
@version: Python 3.7.6
"""

import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import gaierror, error
from utils.log import logger

class Email():
    '''
    创建一个邮件类，用来给指定用户发送邮件，支持多个收件人，可添加附件
    '''
    def __init__(self, server, sender, password, receiver, title, message=None, path=None):
        '''
        初始化Email
        :param server:邮件服务器
        :param sender:发件人
        :param password:发件人邮箱密码
        :param receiver:收件人，当有多个收件人时用‘;’隔开
        :param title:邮件主题
        :param message:邮件正文
        :param path:附件路径，可传入list(多附件)或str(单附件)
        '''
        self.server = server
        self.sender = sender
        self.password = password
        self.receiver = receiver
        self.title = title
        self.message = message
        self.files = path
        # 实例化可包含文本和附件的邮件消息
        self.msg = MIMEMultipart('related')

    def _attach_file(self, att_file):
        '''将单个文件加入附件列表中，每次只能加入一个附件'''
        att = MIMEText(open(att_file, 'rb').read(), 'base64', 'utf-8')
        att['Content-Type'] = 'application/octet-stream'
        file_name = os.path.basename(att_file)
        # 附件名称显示
        att["Content-Disposition"] = 'attachment; filename="%s"' % file_name
        # 将附件添加至邮件消息中
        self.msg.attach(att)
        logger.info('attach file {}'.format(att_file))

    def send(self):
        self.msg['Subject'] = self.title
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver

        if self.message:
            # 在消息中添加邮件内容
            self.msg.attach(MIMEText(self.message, 'plain', 'utf-8'))

        if self.files:
            if isinstance(self.files, list):
                for file in self.files:
                    self._attach_file(file)
            elif isinstance(self.files, str):
                self._attach_file(self.files)

        try:
            # 实例化邮件服务
            smtp_server = smtplib.SMTP(self.server)
        except (gaierror and error) as e:
            logger.exception('发送邮件失败,无法连接到SMTP服务器，检查网络以及SMTP服务器. %s', e)
        else:
            try:
                smtp_server.login(self.sender, self.password)
            except smtplib.SMTPAuthenticationError as e:
                logger.exception('用户名密码验证失败！%s', e)
            else:
                smtp_server.sendmail(self.sender, self.receiver.split(';'), self.msg.as_string())
            finally:
               smtp_server.quit()
               logger.info('发送邮件"{0}"成功! 收件人：{1}。如果没有收到邮件，请检查垃圾箱，'
                           '同时检查收件人地址是否正确'.format(self.title, self.receiver))

if __name__ == '__main__':
    import os, glob
    from utils.config import REPORT_PATH
    reports = [file for file in  glob.glob(os.path.join(REPORT_PATH, '*.html'))]
    em = Email(server='smtp.sina.com',
               sender='xiaokun0727@sina.com',
               receiver='xiaokun0727@sina.com',
               password='9c80e38376109298',
               title='自动化测试报告',
               message='这是今天的测试报告，请查收！',
               path=reports
               )
    em.send()