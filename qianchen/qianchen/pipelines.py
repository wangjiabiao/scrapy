# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
class QianchenPipeline(object):
    con = pymongo.Connection("localhost", 27017)
    db = con.spidernew

    def process_item(self, item, spider):


        dbdata = {"jobname":"", "companyname":"", "monoy":"", "place":"", "day":"", "jobdetail":"", "jobyear":"", "xueli":"", "cnt":"","fuli":""}
        dbdata["jobname"] = item['jobname']
        dbdata["companyname"] = item['companyname']
        dbdata["monoy"] = item['monoy']
        dbdata["place"] = item['place']
        dbdata["day"] = item['day']
        dbdata["jobdetail"] = item['jobdetail']
        dbdata["jobyear"] = item['jobyear']
        dbdata["xueli"] = item['xueli']
        dbdata["cnt"] = item['cnt']
        dbdata["fuli"] = item['fuli']
        try:
            self.db.job51.insert(dbdata)
        except:
            print "====================================insert error"

        return item
