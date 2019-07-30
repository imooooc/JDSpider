# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from jdspider.utils import get_config
from scrapy import Item, Field

config = get_config('jd')
class_name = config.get('item_class_name')
fields = {'collection': 'product'}
for task in config.get('tasks'):
    attrs = task.get('attrs')
    if attrs:
        for key in attrs.keys():
            fields.update({key: Field()}) #field = Field()
childItem = type(class_name, (Item,), fields)  #{'bar':True}

