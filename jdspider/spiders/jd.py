# -*- coding: utf-8 -*-
from scrapy import  Spider, Request
from jdspider.items import *
from jdspider.utils import get_config
class JdSpider(Spider):
    name = 'jd'

    def __init__(self, jname, *args, **kwargs):
        config = get_config(jname)
        self.jname = jname
        self.config = config
        start_urls = config.get('start_urls')
        if start_urls:
            if start_urls.get('type') == 'static':
                self.start_urls = start_urls.get('value')
            elif start_urls.get('type') == 'dynamic':
                # self.start_urls = list(eval('urls.' + start_urls.get('method'))(*start_urls.get('args', [])))
                self.start_urls = []
        self.allowed_domains = config.get('allowed_domains')
        super(JdSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, meta={'name': self.jname}, callback=self.parse)

    def parse(self, response):
        ls = response.request.meta.get('ls')
        item = childItem()
        for i in ls:
            for key, value in i.items():
                item[key] = value
            yield item