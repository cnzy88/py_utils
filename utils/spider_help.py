#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huang Wei
"""
方便爬虫的相关方法
"""
import os
import re
import sys
import random
import requests
from utils.regex import RegexHelp
from utils.xpath import XPathHtml

#支持python2
if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

def get_common_headers(new_headers=None):
    """
    获取通用的爬虫headers
    :param new_headers 要更新的headers
    :return:
    """
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
    headers['Accept-Encoding'] = 'gzip, deflate, br'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.9'

    if new_headers:
        headers.update(new_headers)
    return headers

def get_proxy_ip_list():
    """
    获取代理ip列表
    :return:
    """
    r = requests.get('https://www.xicidaili.com/nt/', headers=get_common_headers())
    if r.status_code == 200:
        content = r.content
        return RegexHelp.match_ip(content)
    else:
        return None

def generate_requests_proxy_ip():
    """
    # 为requests库随机生成一个代理ip
    生成代理ip列表
    :return:
    """
    proxy_ip_lists = []
    r = requests.get('https://www.xicidaili.com/nt/', headers=get_common_headers(), timeout=10)
    if r.status_code == 200:
        content = r.content
        xpath = XPathHtml(source_str=content)
        ips = xpath.get_customization_content('//*[@class="odd"]/td[position()=2]/text()')
        ports = xpath.get_customization_content('//*[@class="odd"]/td[position()=3]/text()')
        types = xpath.get_customization_content('//*[@class="odd"]/td[position()=6]/text()')
        active_days = xpath.get_customization_content('//*[@class="odd"]/td[last()-1]/text()')
        speeds = xpath.get_customization_content('//*[@class="odd"]/td[last()-3]/div/@title')
        connect_speeds = xpath.get_customization_content('//*[@class="odd"]/td[last()-2]/div/@title')
        for i in range(0, len(ips)):
            speed = speeds[i].replace('秒', '')
            if speed > '1':
                continue
            connect_speed = connect_speeds[i].replace('秒', '')
            if connect_speed > '1':
                continue
            active_day = active_days[i]
            if active_day.find('分钟') >= 0 or active_day.find('小时') >= 0:
                continue

            ip_dic = {types[i].lower(): '{0}:{1}'.format(ips[i], ports[i])}
            proxy_ip_lists.append(ip_dic)

        selected_ip = random.choice(proxy_ip_lists)
        print("selected ip: %s" % selected_ip)
        return selected_ip
    else:
        print('get proxy ips failed,status code: %s' % r.status_code)
        return None

def filter_str_html(s):
    """
    去掉字符串中一些html语法的字符，如<font color=#CC0000></font>
    tip: re.sub()  是将匹配到的字符从原始字符串中去除掉，保留剩下的。
    :return:
    """
    if not s:
        return None

    return re.sub(r'<.*?>','',s)

if __name__ == '__main__':
    # r = requests.get('http://sale.rocketai.cn/gw/crm/api/v1/logical/miniAppInsurance/detail?id=194&flag=1', proxies=generate_requests_proxy_ip(), timeout=10)
    # print(r.status_code)
    # xpath = XPathHtml(filepath='test.html')
    # print(xpath.get_customization_content('//*[@class="odd"]/td[last()-3]/div/@title'))
    # print(generate_requests_proxy_ip())
    # print(generate_requests_proxy_ip())
    s = '购买<font color=#CC0000>备哆分1号</font>_到底有多坑_为什么不建议买_优缺点深度剖析'
    print(filter_str_html(None))