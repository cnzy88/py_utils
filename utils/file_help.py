#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huang Wei
import os

class FileHelp:

    """
    文件处理类
    """

    @staticmethod
    def write_file(filepath, content):
        """
        往文件中写内容(不附加)
        :param filepath:
        :param content:
        :return:
        """
        if not isinstance(content, str):
            content = str(content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def read_file(filepath):
        """
        从文件中读取内容
        :param filepath:
        :return:
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError as e:
            print('file %s not exist' % (filepath))
            return None

    @staticmethod
    def remove_dir_all_files(dir):
        """
        删除一个目录下的所有文件
        :param dir:
        :return:
        """
        ls = os.listdir(dir)
        for i in ls:
            c_path = os.path.join(dir, i)
            if os.path.isdir(c_path):
                os.rmdir(c_path)
            else:
                os.remove(c_path)

    @staticmethod
    def list_dir_all_files(dir):
        """
        获取某个目录下的所有文件的路径
        :param dir:
        :return:
        """
        paths = []
        ls = os.listdir(dir)
        for i in ls:
            c_path = os.path.join(dir, i)
            paths.append(c_path)
        return paths

    @staticmethod
    def get_dir_files(dir):
        """
        获取某个目录下的所有文件
        :param dir:
        :return:
        """
        for root, dirs, files in os.walk(dir):
            return files