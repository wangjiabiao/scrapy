#coding=utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector,Selector
from lagou.items import LagouItem
from scrapy.http import Request

class test(CrawlSpider):
    name = "lagou"
    allowed_domains = ["lagou.com"]
    start_urls=['http://www.lagou.com/']
    #翻页函数
    def parse(self, response):
        x = HtmlXPathSelector(response)
        start_url=x.xpath("//div[@class='menu_sub dn']/dl/dd/a/@href").extract()
        print start_url
        if start_url:
         for i in start_url:
            print '---------'
            print i
            urls=[i+'&pn='+str(n) for n in range(1,30)]
            for url in urls:
                #print url
                #yield  Request(url)
                yield  Request(url,callback=self.parse1)

    #一级页面
    def parse1(self, response):

        x = HtmlXPathSelector(response)
        jobs=x.xpath("//div[@class='hot_pos_l']//div[@class='mb10']/a/@href").extract()
        print jobs
        for job in jobs:
                 yield  Request(job,callback=self.parse2)
    #二级页面
    def parse2(self, response):


        x = HtmlXPathSelector(response)
        item = LagouItem()
        item['title']=x.xpath("//dt[@class='clearfix']/h1/@title").extract()

        line=x.xpath("//dd[@class='job_request']/span/text()").extract()
        item['money']=line[0]
        item['place']=line[1]
        item['year']=line[2]
        item['xueli']=line[3]

        item['tag']=x.xpath("//dd[@class='job_request']/text()").extract()[5].split(":")[1].strip(' \n\t\r')

        item['company']=x.xpath("//dl[@class='job_company']/dt/a/img/@alt").extract()[0]
        item['lingyu']=x.xpath("//dl[@class='job_company']//ul[@class='c_feature reset']/li/text()").extract()[0]
        item['guimo']=x.xpath("//dl[@class='job_company']//ul[@class='c_feature reset']/li/text()").extract()[1]
        item['jieduan']=x.xpath("//dl[@class='job_company']//ul[@class='c_feature reset']/li/text()").extract()[5]

        detail=x.xpath("//dd[@class='job_bt']/p/text()").extract()

        item['jobdetail']=''.join(detail)

        item['url']=response.url

        yield item
