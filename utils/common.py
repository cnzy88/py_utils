#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huang Wei
"""
封装一些通用的方法，主要是系统，字符串，一些通用装饰器等。
"""
import sys
if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

import os
import datetime
import functools
import warnings


def count_time(func):
    """
    计算函数执行时间装饰器
    :param func:
    :return:
    """
    def int_time(*args, **kwargs):
        start_time = datetime.datetime.now()
        func(*args, **kwargs)
        over_time = datetime.datetime.now()
        total_time = over_time-start_time
        print('total time: %s' % total_time.total_seconds())
    return int_time

def judge_os_platform():
    """
    判断当前允许程序的操作系统类型
    :return:
    """
    platform = os.name
    if platform == 'nt':
        return 'windows'
    elif platform == 'posix':
        return 'linux'
    else:
        return None

def html_to_pdf(content, new_file_name):
    """
    将html转成pdf
    :return:
    """
    import pdfkit
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    return pdfkit.from_string(content, new_file_name, configuration=config)

def change_dic_to_json_str(obj):
    """
    将python字典转为json字符串
    :param obj:
    :return:
    """
    import json
    if not obj:
        if isinstance(obj, dict):
            return None
        elif isinstance(obj, list):
            return []
        elif isinstance(obj, str):
            return ''
        else:
            return None
    return json.dumps(obj, ensure_ascii=False)

def str_unicode_change():
    """
    str和unicode互转
    #---decode---
    #str------>unicode
    #\xe5\xb2\-->\u5e74\u9f84

    #str<------unicode
    #----encode-------
    :return:
    """
    pass

def open_image(image_file):
    """
    打开图片
    :param image_file:
    :return:
    """
    if os.name == "nt":
        os.system('start ' + image_file)  # for Windows
    else:
        if os.uname()[0] == "Linux":
            if "deepin" in os.uname()[2]:
                os.system("deepin-image-viewer " + image_file)  # for deepin
            else:
                os.system("eog " + image_file)  # for Linux
        else:
            os.system("open " + image_file)  # for Mac

def splite_list(l, num):
    """
    将列表l分割成num个子列表
    :param num: 分割成几部分，通常是线程数
    :return:
    """
    if not l:
        return None

    s = []
    size = int(len(l) / num)
    for i in range(0, len(l), size):
        c = l[i:i + size]
        s.append(c)
    return s

def is_str_contain_list_element(s, l):
    """
    判断字符串s是否包含列表中任意一个元素
    :param s:
    :param l:
    :return: Boolean
    """
    for element in l:
        if s.find(element) >= 0:
            return True

    return False

def deprecated(func):
    """This decorator is used to mark functions as deprecated.
    It will result in a warning being emitted when the function is used.
    """
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            stacklevel=2
        )
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func


if __name__ == '__main__':
    pass