# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#车品牌模型
class ChezhuhomeBrandItem(scrapy.Item):
    mBrandId       = scrapy.Field() #品牌ID
    mBrandName     = scrapy.Field() #品牌名称
    mBaseBrandId   = scrapy.Field() #基本品牌ID 如 一汽奥迪 基本品牌名称为奥迪
    mBaseBrandName = scrapy.Field() #基本品牌名称
    mFirstLetter   = scrapy.Field() #所属查询字母
    mSeriesList    = scrapy.Field() #车系列表

#车系模型
class ChezhuhomeSeriesItem(scrapy.Item):
    mSeriesId     = scrapy.Field()#车系ID
    mSeriesName   = scrapy.Field()#车系名称
    mBrandId      = scrapy.Field()#品牌ID

#车系模型
class ChezhuhomeModelItem(scrapy.Item):
    mModelId     = scrapy.Field()       #车系ID
    mModelName   = scrapy.Field()       #车系名称
    mSeriesId    = scrapy.Field()       #品牌ID
    mYear        = scrapy.Field()       #年代
    mPrice4S     = scrapy.Field()       #4S指导价
    mPriceReal   = scrapy.Field()       #真实报价
    mPriceManufacturer = scrapy.Field() #厂商指导价
    