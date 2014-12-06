#coding=utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector,Selector
from  R.items import RItem
from scrapy.http import Request
class test(CrawlSpider):
    name = "R"
    allowed_domains = ["cran.r-project.org"]
    start_urls=['http://cran.r-project.org/web/packages/available_packages_by_name.html']
    #翻页函数
    def parse(self, response):
        x = HtmlXPathSelector(response)
        _url=x.xpath("//table[@summary='Available CRAN packages by name.']/tr/td/a/@href").extract()

        if _url:
         for i in _url:
            print '---------'
            print i
            url='http://cran.r-project.org'+i.split('..')[2]

            yield  Request(url,callback=self.parse2)

    #二级页面
    def parse2(self, response):


        x = HtmlXPathSelector(response)
        item = RItem()
        item['name']=x.xpath("//html/head/title/text()").extract()[0]
        item['url']=response.url
        item['title']=x.xpath("//html/body/h2/text()").extract()[0]
        item['des']=x.xpath("//html/body/p/text()").extract()[0]
        title=x.xpath("//html/body/table/tr/td[1]/text()").extract()
        nei=x.xpath("//html/body/table/tr/td[2]/text()").extract()
        for i,j in zip(title,nei):
            if i==u'Version:':
                item['version']=j
            elif i==u'Depends:':
                item['depends']=j
            elif i==u'Suggests:':
                item['suggests']=j
            elif i==u'Pubulished:':
                item['published']=j
            elif i==u'Author:':
                item['author']=j
            elif i==u'Maintainer':
                item['Maintainer']=j
            elif i==u'License':
                item['license']=j





        yield item

