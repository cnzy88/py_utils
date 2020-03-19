#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huang Wei
from PyPDF2 import PdfFileReader, PdfFileWriter

class PdfHandle(object):

    """
    PDF处理类
    """

    def __init__(self, filepath, output):
        """
        初始化
        :param filepath:  待处理的pdf文件路径
        :param output:    新生成的pdf的路径
        """
        self.pdf_reader = PdfFileReader(open(filepath, 'rb'))
        self.pdf_writer = PdfFileWriter()
        self.output = output

    def get_page_num(self):
        """
        获取pdf的页数
        :return:
        """
        return self.pdf_reader.getNumPages()

    def get_page(self, index):
        """
        获取pdf页，第一页从0开始
        :param index:
        :return:
        """
        return self.pdf_reader.getPage(index)

    def remove(self, indexs):
        """
        删除某些页，并生成新的pdf文件
        :param indexs: List<int>  要删除的页码的列表
        :return:
        """
        for index in range(0, self.get_page_num()):
            if index not in indexs:
                pageObj = self.pdf_reader.getPage(index)
                self.pdf_writer.addPage(pageObj)

        self.pdf_writer.write(open(self.output, 'wb'))
