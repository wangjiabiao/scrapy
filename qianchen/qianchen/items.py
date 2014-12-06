# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class QianchenItem(Item):
    # define the fields for your item here like:
    # name = Field()
    jobname=Field()
    companyname=Field()
    hangye=Field()
    guimo=Field()
    xingzhi=Field()
    cnt=Field()
    fuli=Field()
    money=Field()
    place=Field()
    day=Field()
    jobdetail=Field()
    url=Field()
    jobyear=Field()
    xueli=Field()
    tag=Field()
    pass
