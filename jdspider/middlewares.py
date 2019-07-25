# # -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from logging import  getLogger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from scrapy.http import HtmlResponse
import time
from jdspider.utils import get_config
from operator import itemgetter

class  SeleniumMiddleware():
    def __init__(self, timeout=None, service_args=[]):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.browser = webdriver.Chrome(service_args=service_args)
        self.browser.set_window_size(1400, 700)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)



    def __del__(self):
        self.browser.close()

    def action_scroll(self):
        for i in range(1, 10000, 50):
            js = "document.documentElement.scrollTop={value}".format(value=i)
            self.browser.execute_script(js)
        time.sleep(1)

    def action_click(self, element_xpath):
        ele = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, element_xpath))
        )
        ele.click()

    def action_sendKeys(self, element_xpath, text):
        ele = self.wait.until(
            EC.presence_of_element_located((By.XPATH, element_xpath))
        )
        ele.send_keys(text)

    def task_action(self, task):
        '''
        每次任务所执行的动作
        :param task: task字典 signal:1、滚动条 2、点击 3、输入
        :return:
        '''
        signal = task.get('action').get('signal')
        if signal == 1:
            self.action_scroll()
        if signal == 2:
            self.action_click(element_xpath=task.get('action').get('args'))
        if signal == 3:
            self.action_sendKeys(element_xpath=task.get('action').get('args'), text=task.get('action').get('text'))


    def task_collect(self, attrs):
        '''
        采集数据函数
        :param attrs: 一个字典类型的属性集合，键为字段名称，值为xpath路径
        :return item: 一个字典类型的字段集合，键为字段名称，值为文本类型的字符串
        '''
        item = {}
        for attr_key, attr_value in attrs.items():
            ele = self.wait.until(
                EC.presence_of_element_located((By.XPATH, attr_value))
            )
            item[attr_key] = ele.text
        return item


    def process_request(self, request, spider):
        #获取配置文件
        tasks = get_config(request.meta.get('name')).get('tasks')

        #存放任务先后顺序的列表
        ordered_tasks = sorted(tasks, key=itemgetter('order'))
        self.logger.debug('硒同学开始工作')
        try:
            #打开浏览器
            self.browser.get(request.url)
            #依次完成每个任务,结果存入列表
            ls = []
            for task in ordered_tasks:
                #读取相应的操作配置文件,然后执行相应动作
                self.task_action(task)
                #采集数据
                attrs = task.get('attrs') #元素字典
                if attrs:
                    ls.append(self.task_collect(attrs)) #将字典加入列表
            request.meta['ls'] = ls
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                            status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, request=request, status=500)




    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   service_args=crawler.settings.get('CHROMEDRIVER_SERVICE_ARGS'))







#
# class SMiddleware():
#     def __init__(self, timeout=None, service_args=[]):
#         self.logger = getLogger(__name__)
#         self.timeout = timeout
#         self.browser = webdriver.Chrome(service_args=service_args)
#         self.browser.set_window_size(1400, 700)
#         self.browser.set_page_load_timeout(self.timeout)
#         self.wait = WebDriverWait(self.browser, self.timeout)
#
#     def __del__(self):
#         self.browser.close()
#
#     def process_request(self, request, spider):
#         self.logger.debug('硒同学开始工作')
#
#         #time.sleep(1)
#         try:
#             self.browser.get(request.url)
#
#             #滚动页面
#             for i in range(1, 10000, 15):
#                 js = "document.documentElement.scrollTop={value}".format(value=i)
#                 self.browser.execute_script(js)
#
#             #寻找元素
#             next_page = self.wait.until(
#                 EC.presence_of_element_located((By.XPATH, '//a[@class="pn-next"]'))
#                 )
#
#             next_page.click()
#             return HtmlResponse(url=self.browser.current_url, body=self.browser.page_source, request=request, encoding='utf-8',
#                             status=200)
#
#         except TimeoutException:
#             return HtmlResponse(url=request.url, request=request, status=500)
#
#
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
#                    service_args=crawler.settings.get('CHROMEDRIVER_SERVICE_ARGS'))
#
#
#
#


