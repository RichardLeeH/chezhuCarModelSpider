# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from os import path
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import sqlite3

class ChezhumodelspiderPipeline(object):
    filename  = '/Volumes/NormalDisk/scrapyProject/chezhuHomeSpider/kakaCar.db'

    def __init__(self):
        self.kkcardb = None
        self.cursor  = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)
        self.seriesCount = 0
        
    def initialize(self):
        if path.exists(self.filename):
            self.kkcardb = sqlite3.connect(self.filename)
            self.cursor  = self.kkcardb.cursor()
        else:
            self.kkcardb = self.create_table(self.filename)
            self.cursor  = self.kkcardb.cursor()
 
    def finalize(self):
        if self.kkcardb is not None:
            self.kkcardb.commit()
            self.kkcardb.close()
            self.kkcardb = None
            print('seriesCount='+str(self.seriesCount))

    def process_item(self, item, spider):
        itemClassName = item.__class__.__name__
        
        if cmp(itemClassName, 'ChezhuhomeModelItem') == 0:
            print('itemClassName=', itemClassName)
            
            modelId     = item['mModelId']       #车系ID
            modelName   = item['mModelName']     #车系名称
            seriesId    = item['mSeriesId']      #品牌ID
            year        = item['mYear']          #年代
            price4S     = item['mPrice4S']       #4S指导价
            priceReal   = item['mPriceReal']     #真实报价
            priceManufacturer = item['mPriceManufacturer'] #厂商指导价
            
            print('car_db_model='+str(item))
            try:
                self.cursor.execute("replace into t_kk_model(modelId, modelName, price4S, priceReal, priceManufacturer, year, seriesId) values(?, ?, ?, ?, ?, ?, ?)", (int(modelId), modelName, price4S, priceReal, priceManufacturer, year, int(seriesId)))
                self.seriesCount = (self.seriesCount+1)
            #写入数据库:车品牌
            except:
                print('car_db_model_error:')

        return item
    
