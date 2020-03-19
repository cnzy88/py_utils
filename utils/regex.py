#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huang Wei
import re

class RegexHelp(object):

    """
    正则处理类
    """

    @staticmethod
    def match_number(source):
        """
        匹配字符串中的数字
        :param source: 原始数字
        :return: list  匹配到的数字的列表
        """
        return re.findall('\d+',source)

    @staticmethod
    def match_letters(source):
        """
              匹配字符串中的英文字母
              :param source: 原始数字
              :return: list  匹配到的英文字母的列表
              """
        return re.findall('[a-zA-Z]', source)

    @staticmethod
    def match(source, regex):
        """
        自定义规则匹配
        :param source:  原始字符串
        :param regex:   匹配规则
        :return:  list  匹配到的数据的列表
        """
        return re.findall(regex, source)

    @staticmethod
    def match_one(source, regex):
        """
        自定义规则匹配，只返回匹配到的第一个字符串
        :param source:
        :param regex:
        :return:  String
        """
        data = re.findall(regex, source)
        if not data:
            return None
        return data[0]

    @staticmethod
    def match_ip(source):
        """
        匹配字符串中的所有ip
        :param source:
        :return:
        """
        regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        return re.findall(regex, source)

    @staticmethod
    def filter_special_char(source):
        if not source:
            return None
        return re.sub(r'\W+', '', source)

if __name__ == '__main__':
    source = """“白熊管家”"""
    print(RegexHelp.filter_special_char(source))