#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huang Wei
import time
from selenium import webdriver

class SeleniumHelp:
    """
    封装selenium的一些方法，方便使用selenium
    """
    CHROME_DRIVER_PATH = 'C:\chromedriver.exe'

    def __init__(self, url):
        self.url = url
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')  #配置不打开chrome
        self.driver = webdriver.Chrome(executable_path=self.CHROME_DRIVER_PATH, chrome_options=self.options)
        self.driver.get(self.url)

    @property
    def content(self):
        """
        获取页面内容
        使用@property装饰器将一个直接访问的属性转变为函数触发式属性
        :return:
        """
        return self.driver.page_source

    def find_element_by_xpath(self, xpath):
        """
        通过xpath找元素(注意此方法只返回一个，即使找到多个元素)
        :param xpath:
        :return:
        """
        return self.driver.find_element_by_xpath(xpath)

    def click(self, element):
        """
        模拟鼠标点击事件
        :param element:
        :return:
        """
        element.click()

    def quit(self):
        """
        关闭浏览器并使driver失效
        :return:
        """
        self.driver.quit()


if __name__ == '__main__':
    url = 'https://www.91duobaoyu.com/autoArticle/html/pc_12/12.html?advVersion=10012&qd=baidu1&keyword=%e8%b4%ad%e4%b9%b0%e9%87%8d%e7%96%be%e4%bf%9d%e9%99%a9%e6%9c%89%e5%bf%85%e8%a6%81%e5%90%97'
    s = SeleniumHelp(url)
    print(len(s.content))
    # element = s.find_element_by_xpath('//*[@id="img-content"]/div[3]/div')
    # s.click(element)
    time.sleep(10)
    print(len(s.content))
    s.quit()