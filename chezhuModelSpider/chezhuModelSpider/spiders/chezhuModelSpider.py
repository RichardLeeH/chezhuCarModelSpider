# -*- coding: utf-8 -*-
# encoding: utf-8

from KKCarModelParser import KKCarModelParser

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

'''  
爬取汽车之家的汽车模型  
'''
import scrapy
import sqlite3
from scrapy.http import Request

class KKCarModelSpider(scrapy.Spider):
    
    dbName  = '/Volumes/NormalDisk/scrapyProject/chezhuHomeSpider/kakaCar.db' 
    name = "chezhuModelSpider"
    allowed_domains = ["www.16888.com"]
    start_urls = ['http://www.16888.com/57219/'
     ]
    
    def __init__(self, name=None, **kwargs):
        self.initStartUrls()
        
    def initStartUrls(self):
        self.kkcardb = sqlite3.connect(self.dbName)
        self.cursor  = self.kkcardb.cursor()
        
        seriesIdList = self.cursor.execute('select seriesId from t_kk_series')
        
#         for seriesId in seriesIdList:
#             start_url = 'http://www.16888.com/'+str(seriesId[0])
#             self.start_urls.append(start_url)
#             print('start_urls='+start_url)

        self.cursor.close()
        self.kkcardb.close()
        
    def parse(self, response):
        
        modelParser = KKCarModelParser(response.body)
        
        yearList = modelParser.parse_year()
        
        if len(yearList)>0:
            print('year_list='+str(yearList))
            for yearUrl in yearList:
                yield Request(yearUrl, callback=self.parse_model)
                yield yearUrl
                
        else:#没有年列表
            seriesList = modelParser.parse_Model(response.url)
            if seriesList and len(seriesList) > 0:#存在车型
                yield seriesList
            else:#车型也不存在，只有一种情况，即车系就是其对应的车型
                model = modelParser.parse_onlyModel(response.url)
                yield model
                    
    def parse_model(self, response):
        modelParser = KKCarModelParser(response.body)
        seriesList = modelParser.parse_Model(response.url)
        return seriesList
    
if __name__ == "__main__":
    pass

    
    
    
