# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.internet import defer
from twisted.internet import reactor

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from chezhuHomeSpider.spiders import chezhuBrandSpider, chezhuModelSpider

configure_logging()
runner = CrawlerRunner(get_project_settings())

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(chezhuBrandSpider.KKCarBrandSpider)
    yield runner.crawl(chezhuModelSpider.KKCarModelSpider)
    reactor.stop()


crawl()
reactor.run() # the script will block here until the last crawl call is finished