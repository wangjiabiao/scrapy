# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class RItem(Item):
    # define the fields for your item here like:
    name = Field()
    title=Field()
    version=Field()
    depends=Field()
    suggests=Field()
    published=Field()
    maintainer=Field()
    license=Field()
    author=Field()
    des=Field()
    url=Field()
    pass
