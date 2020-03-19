#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huang Wei
import sys
from jinja2 import Environment, FileSystemLoader

reload(sys)
sys.setdefaultencoding('utf-8')

class Jinjia2(object):

    """
    模板渲染处理类
    """

    def __init__(self, searchpath):
        self.searchpath = searchpath

    def render_html(self, template, objs, write_file=None):
        env = Environment(loader=FileSystemLoader(self.searchpath))
        template = env.get_template(template)
        html_content = template.render(objs = objs)
        if write_file:
            with open(write_file, 'w') as f:
                f.write(html_content)
        return html_content



if __name__ == '__main__':
    jinjia2_operator = Jinjia2('../static')
    objs = []
    obj = {}
    obj['msgtime'] = '2019-12-24 14:32:38'
    obj['msgbody'] = 'test2'
    obj['pos_class'] = 'dialog_item_right'
    obj['head_img_url'] = "http://wx.qlogo.cn/mmhead/ver_1/6hBjsI9aLs1icL94sSwY4dPvpEpb4qHibdt2lWYdU05B3YwKbYvgBp3ZsOjIJXTKQqztOqgjpcSMusKNS0n66QNoRvUXxz5mX8g8AYX0ZeSibY/96"
    objs.append(obj)
    objs.append(obj)
    objs.append(obj)
    jinjia2_operator.render_html('chat_template.html', objs, write_file='../static/test3.html')