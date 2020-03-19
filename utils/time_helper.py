#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huang Wei
import datetime
import time

class TimeHelp(object):

    """
    时间处理类
    """

    def __init__(self, format='%Y-%m-%d %H:%M:%S'):
        """
        初始化
        :param format: 定义要返回的时间的格式，默认返回年-月-日 时:分:秒
        """
        self.format = format

    def get_current_time(self):
        """
        获取当前的时间
        :return:
        """
        return time.strftime(self.format, time.localtime(time.time()))

    def get_current_weekday(self):
        """
        获取当前是周几
        :return:  int
        """
        return datetime.datetime.now().weekday()

    def time_plus(self, t, type, num):
        """

        :param t:      待增加的时间
        :param type:   加时间的类型， second, minute, hour, day
        :param num:    加的数
        :param format:    时间格式，默认为%Y-%m-%d %H:%M:%S
        :return:
        """
        time_obj = datetime.datetime.strptime(t, self.format)
        if type == 'second':
            return str((time_obj + datetime.timedelta(seconds=num)).strftime(self.format))
        elif type == 'minute':
            return str((time_obj + datetime.timedelta(minutes=num)).strftime(self.format))
        elif type == 'hour':
            return str((time_obj + datetime.timedelta(hours=num)).strftime(self.format))
        else:
            print('type %s not supported yet' % type)
            return None

    def utc_secs_to_localtime(self, secs):
        """
        将utc时间转化成东八区当前时间
        :param secs:
        :return:
        """
        s = time.strftime(self.format, time.gmtime(secs))
        return self.time_plus(s, 'hour', 8)

    def time_diff(self, timeStra, timeStrb):
        """
        两个时间相减后的分钟差, 如果为负，则返回0
        :param timeStra:
        :param timeStrb:
        :return:
        """
        if timeStra <= timeStrb:
            return 0
        a = str(timeStra.split(".")[0])
        b = str(timeStrb.split(".")[0])
        ta = time.strptime(a, "%Y-%m-%d %H:%M:%S")
        tb = time.strptime(b, "%Y-%m-%d %H:%M:%S")
        y, m, d, H, M, S = ta[0:6]
        dataTimea = datetime.datetime(y, m, d, H, M, S)
        y, m, d, H, M, S = tb[0:6]
        dataTimeb = datetime.datetime(y, m, d, H, M, S)
        secondsDiff = (dataTimea - dataTimeb).seconds
        daysDiff = (dataTimea - dataTimeb).days
        minutesDiff = daysDiff * 1440 + round(secondsDiff / 60, 1)
        return int(minutesDiff)

if __name__ == '__main__':
    time_helper = TimeHelp('%Y-%m-%d %H:%M:%S')
    print(time_helper.time_diff('2020-03-19 18:25:15', '2020-03-19 18:22:12'))








