# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy.utils.project import get_project_settings
from jdspider.utils import get_config
from scrapy import Item, Field
import jdspider.settings

config = get_config('jd')
class_name = config.get('item_class_name')
fields = {'collection': 'aaa'}
for task in config.get('tasks'):
    attrs = task.get('attrs')
    if attrs:
        for key in attrs.keys():
            fields.update({key: Field()}) #field = Field()
childItem = type(class_name, (Item,), fields)  #{'bar':True}

