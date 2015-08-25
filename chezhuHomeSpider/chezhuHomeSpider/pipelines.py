# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from os import path
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import sqlite3
from items import ChezhuhomeBrandItem, ChezhuhomeSeriesItem

class ChezhuHomePipeline(object):
    filename  = '/Volumes/NormalDisk/scrapyProject/chezhuHomeSpider/kakaCar.db'
    fileBrand = '/Volumes/NormalDisk/scrapyProject/chezhuHomeSpider/kakaCar.txt'
    def __init__(self):
        self.kkcardb = None
        self.cursor  = None
        self.fout = open(self.fileBrand, 'w') 
        self.brandCount  = 0
        self.seriesCount = 0
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)
    
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
            print('dbbrandCount='+str(self.brandCount))
            print('dbseriesCount='+str(self.seriesCount))
            self.fout.close() 
    
    '''
    创建数据库及相关的表
    '''
    def create_table(self, filename):
        conn = sqlite3.connect(filename)
        #创建 车品牌表，字段有：品牌ID, 品牌名称，首字母
        conn.execute("create table t_kk_brand (brandId integer primary key, brandName varchar(20), baseId integer, baseName varchar(20), firstLetter varchar(1))")                
        
        #创建 车系表，字段有：车系ID, 车系名称，所属品牌ID(外键)
        conn.execute("create table t_kk_series (seriesId integer primary key, seriesName varchar(50), brandId integer)")

        #创建 车型表，字段有：车型ID, 车型名称，最高报价，最低报价，年代，所属车系ID(外键)
        conn.execute("create table t_kk_model (modelId integer primary key, modelName varchar(100), price4S varchar(20), priceReal varchar(20), priceManufacturer varchar(20), year varchar(4), seriesId integer)")    

        conn.commit()

        return conn
    
    ##################################################################################################       
    def process_item(self, item, spider):
        
        itemClassName = item.__class__.__name__
        
        if cmp(itemClassName, 'ChezhuhomeBrandItem') == 0:
            print('itemClassName=', itemClassName)

            brandId       = item['mBrandId']
            brandName     = item['mBrandName']
            baseBrandId   = item['mBaseBrandId']
            baseBrandName = item['mBaseBrandName']
            firstLetter   = item['mFirstLetter']
            seriesList    = item['mSeriesList']
#             print('car_db_brand:'+brandId+','+brandName+','+baseBrandId+','+baseBrandName+','+firstLetter)
#             self.fout.write(('car_db_brand:'+brandId+','+brandName+','+baseBrandId+','+baseBrandName+','+firstLetter).encode('utf-8') + '\n')       #将分词好的结果写入到输出文件 
            try:
                self.cursor.execute("replace into t_kk_brand(brandId, brandName, baseId, baseName, firstLetter) values(?, ?, ?, ?, ?)", (int(brandId), brandName, int(baseBrandId), baseBrandName, firstLetter))
                self.brandCount = (self.brandCount+1)
            #写入数据库:车品牌
            except:
                print('car_db_brand_error:')
                
            #车系写入数据库
            for series in seriesList:
                seriesId      = series['mSeriesId']
                seriesName    = series['mSeriesName']
                seriesBrandId = series['mBrandId']
#                 print('car_db_series:'+seriesId+','+seriesName+','+seriesBrandId)
                #写入数据库:车系
                try:
                    self.cursor.execute("replace into t_kk_series(seriesId, seriesName, brandId) values(?, ?, ?)", (int(seriesId), seriesName, int(seriesBrandId)))
                    self.seriesCount = (self.seriesCount+1)
                except:
                    print('car_db_series_error:')                    
        elif cmp(itemClassName, 'ChezhuhomeModelItem') == 0:    
            print('itemClassName=', itemClassName)
        return item
    