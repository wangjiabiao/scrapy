#coding=utf-8
'''
modified:
2014-11-27 需要增加翻页方式
'''
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector,Selector
from lagou.items import LagouItem
from scrapy.http import Request
from scrapy.http import HtmlResponse
from lxml import etree
import urllib
import math
import re
class test(CrawlSpider):
    name = "lagou"
    allowed_domains = ["http://www.lagou.com/jobs"]
    #start_urls = ["http://search.51job.com/list/000000%252C00,000000,0000,00,9,99,%25CA%25FD%25BE%25DD%25B7%25D6%25CE%25F6,1,1.html?"
                  #"lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=01&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&confirmdate=9&fromType=14"]
    start_urls=['http://www.lagou.com/jobs/list_所有职务']

    #rules = [Rule(SgmlLinkExtractor(allow=('http://search.51job.com/job/.*\.html', )),callback='myparse'),]

    def parse(self, response):
        x = HtmlXPathSelector(response)
        start_url=x.xpath("//div[@class='menu_sub dn']/dl/dd/a/@href").extract()
        if start_url:
         for i in start_url:
            print i
            urls=[i+'&pn='+str(i+1) for i in range(30)]
            for url in urls:
               jobs=url.xpath("//div[@class='hot_pos_l']//div[@class='mb10']/a/@href").extract()
               for job in jobs:
                 yield  Request(job,callback=self.parse1)

    def parse1(self, response):


        x = HtmlXPathSelector(response)
        item = LagouItem()
        item['title']=x.xpath("//dt[@class='clearfix']/h1/text()").extract()[2]
        item['companyname']=x.xpath("//div[@class='s_txt_jobs']//a[@style='font-size:14px;font-weight:bold;color:#000000;']/text()").extract()[0]
        item['tag']=x.xpath("//div[@class='s_txt_jobs']//div[@class='jobdetail_divRight_span']").extract()
        print  x.path("//div[@class='s_txt_jobs']//tbody/tr/td/text()").extract()
        #item['day']=x.xpath("//div[@class='s_txt_jobs']//table[@class='jobs_1']//td[@class='txt_2 '][1]/text()").extract()
        #item['place']=x.xpath("//div[@class='s_txt_jobs']//table[@class='jobs_1']//td[@class='txt_2 '][2]/text()").extract()
        #item['cnt']=x.xpath("//div[@class='s_txt_jobs']//table[@class='jobs_1']//td[@class='txt_2 '][3]/text()").extract()
        #item['jobyear']=x.xpath("//div[@class='s_txt_jobs']//table[@class='jobs_1']//td[@class='txt_2 '][4]/text()").extract()
        #item['xueli']=x.xpath("//div[@class='s_txt_jobs']//table[@class='jobs_1']//td[@class='txt_2 '][5]/text()").extract()

        title=x.xpath("//div[@class='s_txt_jobs']//table[@class='jobs_1']//td[@class='txt_1']/text()").extract()
        nei=x.xpath("//div[@class='s_txt_jobs']//table[@class='jobs_1']//td[@class='txt_2 ']/text()").extract()

        print title
        print nei
        for i,j in zip(title,nei):
            if i==u'发布日期：':
                item['day']=j
            elif i==u'工作地点：':
                item['place']=j
            elif i==u'招聘人数：':
                item['cnt']=j
            elif i==u'工作年限：':
                item['jobyear']=j
            elif i.replace(u'\xa0',u'')==u'学历：':
                item['xueli']=j
            elif i==u'薪水范围：':
                item['money']=j

        #item['money']=x.xpath("//div[@class='s_txt_jobs']//table[@class='jobs_1']//td[@class='txt_2 jobdetail_xsfw_color ']/text()").extract()
        detail=x.xpath("//td[@class='txt_4 wordBreakNormal job_detail ']/div").extract()[0]
        item['jobdetail']='\t'.join(detail)
        fu=x.xpath("//div[@class='s_txt_jobs']//div[@class='jobdetail_divRight_span']/span[@class='Welfare_label']/text()").extract()
        if len(fu) > 0:
            item['fuli']=fu

        item['url']=response.url
        next_url=x.xpath("//a[@style='border:0px; width:auto;margin-left:5px;']/@href").extract()[2]
        seq = Request(next_url,callback=self.parse)
        yield item