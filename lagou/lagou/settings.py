# Scrapy settings for lagou project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'lagou'

SPIDER_MODULES = ['lagou.spiders']
NEWSPIDER_MODULE = 'lagou.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'lagou (+http://www.yourdomain.com)'
RANDOMIZE_DOWNLOAD_DELAY = True

USER_AGENT = 'Mozilla AppleWebKit/537.36 Chrome/27.0.1453.93 Safari/537.36'

COOKIES_ENABLED = False