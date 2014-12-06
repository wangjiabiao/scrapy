# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class LagouItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title=Field()
    url=Field()
    money=Field()
    place=Field()
    year=Field()
    xueli=Field()
    tag=Field()
    company=Field()
    lingyu=Field()
    jieduan=Field()
    guimo=Field()
    jobdetail=Field()
    pass
