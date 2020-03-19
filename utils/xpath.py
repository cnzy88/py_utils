#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huang Wei
from lxml import etree

class XPathHtml(object):

    """
    xpath处理类
    """

    def __init__(self, source_str=None, filepath=None, url=None):
        """
        html对象初始化
        :param source: 原始html字符串
        :param filepath: 要解析的文件路径
        """
        if source_str:
            self.html_element = etree.HTML(source_str)
        elif filepath:
            parser = etree.HTMLParser(encoding="utf-8")
            self.html_element = etree.parse(filepath, parser=parser)
        elif url:
            import requests
            from utils.spider_help import get_common_headers
            content = requests.get(url=url, headers=get_common_headers()).text
            self.html_element = etree.HTML(content)
        else:
            print('init xpath obj failed, not found source str or file.')
            raise RuntimeError

    def get_custom_class_content(self, class_name):
        """
        获取文档中所有的class=class_name的元素
        :param class_name:
        :return:
        """
        return self.html_element.xpath("""//*[@class="%s"]""" % class_name)

    def get_customization_content(self, regular):
        """
        获取自定义规则的内容
        自定义规则，如/html/body/div/ul/li/a,注意如果要获取a标签，那a标签就不需要加斜杠了，否则报错。
        /html/body/div/ul/li/a     返回的是List<Element>
        /html/body/div/ul/li/a/text()， 返回的是List<String>
        /html/body/div/ul/li/a/@href    返回的是List<String> 打印的是指定路径下a标签的属性href
        //li/a/text()    相对路径查找，查找所有li标签下的a标签内容
        //li[last()]/a/@href   查找最后一个li标签里的a标签的href属性数
        //li[last()-1]/a/@href  查找倒数第二个li标签里的a标签的href属性
        //*[@id="kw"]    使用相对路径查找所有的标签，属性id等于kw的标签
        //*              查找所有的元素

        轴，轴可定义相对于当前节点的节点集。
        sibling： 同级标签
        following： 当前标签后面的所有标签
        ...
        步语法：轴名称::节点[谓语]
        //img/following-sibling::span[1]   查找所有img标签的与之同级的下一个span标签
        //img/preceding-sibling::span[1]    查找所有img标签的与之同级的上一个span标签
        ../following-sibling::span[1]       查找当前标签的父标签的与之同级的(叔标签)span标签
        //*[@class="odd"]/td[position()=2]/text()  查找所有class='odd'的元素的第2个td子元素的内容

        几个函数: starts-with, ends-with, contains, or， text函数一般都是作为谓语，放在[]里面
        //input[starts-with(@id,'fuck')]
        //input[ends-with(@id,'fuck')]
        //input[contains(@id,'fuck')]
        //input[contains(@id,”fuck”) or contains(@id,”title”)]
        :return:  List
        """
        return self.html_element.xpath(regular)

    def to_string(self):
        """
        将html对象转为字符串
        :return: String
        """
        return etree.tostring(self.html_element).decode("utf-8")


if __name__ == '__main__':
    source = """
            <div>
                <ul>
                     <li class="item-0"><a href="link1.html">first item</a></li>
                     <span id='test'>I am span</span>
                     <li class="item-1"><a href="link2.html">second item</a></li>
                     <p id='test'>I am p</p>
                     <li id="item-inactive"><a href="link3.html">third item</a></li>
                     <li class="item-1"><a href="link4.html">fourth item</a></li>
                     <li class="test"><a href="link5.html">fifth item</a>
                 </ul>
             </div>
            """
    url = 'https://www.91duobaoyu.com/autoArticle/html/pc_12/12.html?advVersion=10012&qd=baidu1&keyword=%e8%b4%ad%e4%b9%b0%e9%87%8d%e7%96%be%e4%bf%9d%e9%99%a9%e6%9c%89%e5%bf%85%e8%a6%81%e5%90%97'
    xpath = XPathHtml(source_str=source)
    print(xpath.get_customization_content('//*[li]'))