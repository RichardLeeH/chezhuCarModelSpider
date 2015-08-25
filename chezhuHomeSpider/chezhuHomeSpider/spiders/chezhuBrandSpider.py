# -*- coding: utf-8 -*-
# encoding: utf-8

from KKCarBrandParser import KKCarBrandParser

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

'''  
爬取汽车之家的汽车模型  
'''
import scrapy

class KKCarBrandSpider(scrapy.Spider):
    # define the fields for your item here like:    
    name = "chezhuBrandSpider"
    allowed_domains = ["auto.16888.com"]
    start_urls = [
     "http://auto.16888.com/"
     ]
    
    
    def parse(self, response):
        
        brandParser = KKCarBrandParser(response.body)
        brandList = brandParser.parse_brand()
        
        return brandList
        
        
if __name__ == "__main__":
    fp = open("/Volumes/NormalDisk/scrapyProject/chezhuHomeSpider/Sources/chezhuHome.html")
    content = fp.read();

    bdParser = KKCarBrandParser(content)
    
    
    
