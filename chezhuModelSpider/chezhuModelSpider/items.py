# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


#车系模型
class ChezhuhomeModelItem(scrapy.Item):
    mModelId     = scrapy.Field()       #车系ID
    mModelName   = scrapy.Field()       #车系名称
    mSeriesId    = scrapy.Field()       #品牌ID
    mYear        = scrapy.Field()       #年代
    mPrice4S     = scrapy.Field()       #4S指导价
    mPriceReal   = scrapy.Field()       #真实报价
    mPriceManufacturer = scrapy.Field() #厂商指导价