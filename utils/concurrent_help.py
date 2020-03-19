#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huang Wei
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
    ALL_COMPLETED,
    wait,
    ProcessPoolExecutor
)

class ConcurrentHelp(object):

    """
    并发基类
    """

    def __init__(self, pool):
        """
        初始化线程池，创建max_workers个线程
        :param max_workers:
        """
        self.pool = pool

    def submit(self, f, args):
        """
        提交任务f到线程池中
        :param f:  待执行的任务
        :param args:  任务函数的参数
        :return: Future
        """
        return self.pool.submit(f, *args)

    def add_callback(self, future, callback):
        """
        给任务注册完成时的回调函数。callback示例:
        def cb(future):
            result = future.result()
            ...
            ...
        :param future:
        :param callback:
        :return:
        """
        future.add_done_callback(callback)

    def is_done(self, future):
        """
        获取任务是否已完成的状态
        :param future:
        :return: boolean
        """
        return future.done()

    def cancel(self, future):
        """
        取消线程池中未运行的任务
        :param future:
        :return: boolean
        """
        return future.cancel()

    def is_running(self, future):
        """
        任务是否开始执行
        :param future:
        :return:  boolean
        """
        return future.runnig()

    def as_completed(self, futures):
        """
        遍历线程池中所有任务，一旦有任务完成，返回执行结果.
        注意:此方法会阻塞主线程
        :param futures: List
        :return:
        """
        for future in as_completed(futures):
            yield future.result()

    def wait(self, futures, return_when=ALL_COMPLETED):
        """
        主线程阻塞，直到满足设定的条件
        :param futures:
        :param return_when:
        :return:
        """
        wait(futures, return_when=return_when)

    def close_pool(self):
        """
        关闭线程池。如果有任务未完成，则会阻塞直到所有任务完成。
        :return:
        """
        self.pool.shutdown()

class ThreadPoolHelp(ConcurrentHelp):

    """
    多线程处理类
    用法:
    pool = thread_pool(max_workers=2)
    pool.submit(sleep, (2,))
    pool.submit(sleep, (3,))
    thread_pool.add_callback(future1, cb)  #可选，不一定需要

    两种等待方式
    第一种:
    thread_pool.wait([future1, future2], return_when=ALL_COMPLETED)
    for result in pool.as_completed([future1, future2]):
        print(result)

    第二种
    pool.close_pool()
    """

    def __init__(self, max_workers=None):
        pool = ThreadPoolExecutor(max_workers=max_workers)
        super(ThreadPoolHelp, self).__init__(pool)


class ProcessPoolHelp(ConcurrentHelp):
    """
    多进程处理类
    用法:
    pool = ProcessPoolHelp(max_workers=2)
    future1 = pool.submit(sleep, (2,))
    future2 = pool.submit(sleep, (3,))
    pool.close_pool()
    目前多进程只能在python3中运行，在python2中运行会出错，好像是个python2的bug.
    """

    def __init__(self, max_workers=None):
        pool = ProcessPoolExecutor(max_workers=max_workers)
        super(ProcessPoolHelp, self).__init__(pool)


if __name__ == '__main__':
    pass



