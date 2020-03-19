#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huang Wei
import smtplib
import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

EMAIL_CONFIG = {}
EMAIL_CONFIG["email"] = "service@rocketai.cn"
EMAIL_CONFIG["host"] = "smtp.exmail.qq.com"
EMAIL_CONFIG["port"] = 465
EMAIL_CONFIG["user"] = "service@rocketai.cn"
EMAIL_CONFIG["password"] = "Bxb666"

class MailSend(object):
    """
    发送邮件的类
    """

    @staticmethod
    def send_mail(receiver, subject, content, cc=''):
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = EMAIL_CONFIG["email"]
        msg.add_header('To', receiver)
        if cc:
            msg.add_header('Cc', cc)

        txt = MIMEText(content, 'html', 'utf-8')
        msg.attach(txt)

        to_addrs = receiver + cc
        if to_addrs.find(','):
            to_addrs = to_addrs.split(',')

        smtp = smtplib.SMTP_SSL(EMAIL_CONFIG["host"], EMAIL_CONFIG["port"])
        smtp.login(EMAIL_CONFIG["email"], EMAIL_CONFIG["password"])
        smtp.sendmail(from_addr=EMAIL_CONFIG["email"], to_addrs=to_addrs, msg=msg.as_string())
        smtp.quit()

    @staticmethod
    def send_mail_with_file(receiver, subject, content, filename, cc=''):
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = EMAIL_CONFIG["email"]
        msg.add_header('To', receiver)
        if cc:
            msg.add_header('Cc', cc)

        to_addrs = receiver + cc
        if to_addrs.find(','):
            to_addrs = to_addrs.split(',')

        txt = MIMEText(content, 'html', 'utf-8')
        msg.attach(txt)
        part = MIMEApplication(open(filename, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(part)

        smtp = smtplib.SMTP_SSL(EMAIL_CONFIG["host"], EMAIL_CONFIG["port"])
        smtp.login(EMAIL_CONFIG["email"], EMAIL_CONFIG["password"])
        smtp.sendmail(from_addr=EMAIL_CONFIG["email"], to_addrs=to_addrs, msg=msg.as_string())
        smtp.quit()

if __name__ == '__main__':
    MailSend.send_mail('ethan@rocketai.cn', 'test', '11111')