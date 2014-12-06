# Scrapy settings for qianchen project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'qianchen'

SPIDER_MODULES = ['qianchen.spiders']
NEWSPIDER_MODULE = 'qianchen.spiders'
#ITEM_PIPELINES = ['qianchen.pipelines.QianchenPipeline']

RANDOMIZE_DOWNLOAD_DELAY = True

USER_AGENT = 'Mozilla AppleWebKit/537.36 Chrome/27.0.1453.93 Safari/537.36'

COOKIES_ENABLED = False
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'qianchen (+http://www.yourdomain.com)'
