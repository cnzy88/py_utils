#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huang Wei
import xlrd
import xlwt

class ExcelReadHandle(object):

    """
    excel读处理类
    """

    def __init__(self, filename, table_index=0):
        # if isinstance(filename, str):
        #     filename = filename.decode('utf-8')
        self.wb = xlrd.open_workbook(filename=filename, encoding_override = 'utf-8')
        self.sheet = self.wb.sheet_by_index(table_index)

    def read_col_num(self):
        return self.sheet.ncols

    def read_row_num(self):
        return self.sheet.nrows

    def read_col(self, col_index):
        return self.sheet.col_values(col_index)

    def read_row(self, row_index):
        return self.sheet.row_values(row_index)

    def read_cell(self, row_index, col_index):
        return self.sheet.cell(row_index, col_index).value


class ExcelWriteHandle(object):

    """
    excel写处理类
    """

    def __init__(self, excel_headers=None):
        """
        对象初始化
        :param excel_headers:  List<String> excel表格头部  如['姓名', '年龄', '手机号码']
        """
        self.file = xlwt.Workbook(encoding='utf-8')
        self.table = self.file.add_sheet('Sheet1', cell_overwrite_ok=True)
        self.excel_headers = excel_headers
        self.style = self.set_default_style()

    def set_default_style(self):
        """
        设置生成的excel表格的默认样式
        header加粗， 高度240
        单元格宽度  200 * 30
        字体高度    220
        :return:
        """
        header_style = xlwt.XFStyle()
        header_style.font.bold = True
        header_style.font.height = 240
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        header_style.alignment = alignment

        for i in range(0, len(self.excel_headers)):
            self.table.write(0, i, self.excel_headers[i], header_style)
            self.table.col(i).width = 200 * 30

        style = xlwt.XFStyle()
        style.font.height = 220
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        style.alignment = alignment

        return style


    def write(self, filepath, datas):
        """
        将数据写到文件中，生成excel文件
        :param filepath:  生成的excel文件的路径
        :param datas:  List<Tuple> 如[('张三', '3岁', '10086'),('李四'，'四岁', '10011'))...]
        :return:
        """
        try:
            i = 0
            for data in datas:
                i += 1
                for j, header in enumerate(self.excel_headers):
                    self.table.write(i, j, data[j], self.style)
            self.file.save(filepath)
            return True
        except Exception as exc:
            print('write failed: %s' % exc)
            return False


if __name__ == '__main__':
    excel_writer = ExcelWriteHandle(['姓名', '年龄', '手机号'])
    datas = [('张三', '3岁', '10086'),('李四', '四岁', '10011')]
    excel_writer.write('test.xls', datas)