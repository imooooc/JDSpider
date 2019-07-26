# -*- coding: utf-8 -*-
from scrapy import  Spider, Request
from urllib.parse import urlencode
from jdspider.items import *
from jdspider.loaders import *
from jdspider.utils import get_config
import requests
class JdSpider(Spider):
    name = 'jd '
    def __init__(self, name, *args, **kwargs):
        config = get_config(name)
        self.config = config
        start_urls = config.get('start_urls')
        if start_urls:
            if start_urls.get('type') == 'static':
                self.start_urls = start_urls.get('value')
            elif start_urls.get('type') == 'dynamic':
                #self.start_urls = list(eval('urls.' + start_urls.get('method'))(*start_urls.get('args', [])))
                self.start_urls = ['https://search.jd.com/Search?keyword=iphone&page=1']

        self.allowed_domains = config.get('allowed_domains')
        super(JdSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, meta={"name": self.name}, callback=self.parse)


    def parse(self, response):
        ls = response.request.meta.get('ls')
        #print(ls)
        item= childItem()
        for i in ls:
            for key, value in i.items():
                item[key] = value
        yield item









    #def parse(self, response):

        #yield Request(url=response.url, callback=self.parse, dont_filter=True, encoding='utf-8')
        #
        # item = self.config.get('item')
        # if item.get('isCardList'):
        #     products = response.xpath(item.get('cardsPath'))
        #     for product in products:
        #         cls = eval(item.get('class'))() #JdItem
        #         loader = eval(item.get('loader'))(cls, selector=product, response=response) #JdProductLoader()
        #         #动态获取配置属性
        #         for key, value in item.get('attrs').items():
        #             for extractor in value:
        #                 if extractor.get('method') == 'xpath':
        #                     loader.add_xpath(key, *extractor.get('args'), **{'re': extractor.get('re')})
        #                 if extractor.get('method') == 'css':
        #                     loader.add_css(key, *extractor.get('args'), **{'re': extractor.get('re')})
        #         yield loader.load_item()

    #
    # name = 'jd'
    # allowed_domains = ['www.jd.com']
    # start_urls = ['http://www.jd.com/']
    # base_url = 'https://search.jd.com/Search?'
    # def start_requests(self):
    #     #url_demo = 'https://search.jd.com/Search?keyword=iphone&page=5'
    #     for keyword in self.settings.get('KEY_WORDS'):
    #         for page in range(1, self.settings.get('MAX_PAGE') + 1, 2):
    #             params = {
    #                 'keyword': keyword,
    #                 'page': page
    #             }
    #             url = self.base_url + urlencode(params)
    #             yield Request(url=url, callback=self.parse)
    #

    # def parse(self, response):
    #      products = response.xpath('//div[@class="gl-i-wrap"]')
    #      for product in products:
    #          item = JdItem()
    #          item['price'] = ''.join(product.xpath('.//div[@class="p-price"]/strong//text()').extract())
    #          item['title'] = product.xpath('.//div[@class="p-name p-name-type-2"]/a/@title').extract_first().strip()
    #          item['comments'] = ''.join(product.xpath('.//div[@class="p-commit"]/strong//text()').extract())
    #          item['shop'] = product.xpath('.//div[@class="p-shop"]/span/a/@title').extract_first()
    #          yield item

    #def parse(self, response):
    #
    #     products = response.xpath('//div[@class="gl-i-wrap"]')
    #     for product in products:
    #         loader = JdProductLoader(item=JdItem(), selector=product)
    #         loader.add_xpath('price', './/div[@class="p-price"]/strong//text()')
    #         loader.add_xpath('title', './/div[@class="p-name p-name-type-2"]/a/@title')
    #         loader.add_xpath('comments', './/div[@class="p-commit"]/strong//text()')
    #         loader.add_xpath('shop','.//div[@class="p-shop"]/span/a/@title')
    #         yield loader.load_item()
