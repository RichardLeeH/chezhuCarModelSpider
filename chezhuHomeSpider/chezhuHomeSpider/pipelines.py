# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.utils.project import get_project_settings
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import sqlite3
import time

from chezhuHomeSpider.utils.DBManager import connMySQL


class ChezhuHomePipeline(object):
    def __init__(self):
        self.kkcardb = None
        self.cursor  = None
        self.brandCount  = 0
        self.seriesCount = 0
        self.modelCount  = 0
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)
    
    def initialize(self):
#         if path.exists(self.filename):
#             self.kkcardb = sqlite3.connect(self.filename)
#             self.cursor  = self.kkcardb.cursor()
#         else:
#             self.kkcardb = self.create_table(self.filename)
#             self.cursor  = self.kkcardb.cursor()
        #连接MySQL
        settings = get_project_settings()
        host   = settings.get('MYSQL_HOST')
        port   = settings.get('MYSQL_PORT')
        user   = settings.get('MYSQL_USER')
        passwd = settings.get('MYSQL_PASSWD')
        dbName = settings.get('MYSQL_DBNAME')
        print('mysql:'+host+','+port+','+user+','+passwd+','+dbName)
        dbTool = connMySQL(host, int(port), user, passwd, dbName)
        self.kkcardb = dbTool[0]
        self.cursor  = dbTool[1]
 
    def finalize(self):
        if self.kkcardb is not None:
            self.kkcardb.commit()
            self.kkcardb.close()
            self.kkcardb = None
            print('dbbrandCount='+str(self.brandCount))
            print('dbseriesCount='+str(self.seriesCount))
            print('dbmodelCount='+str(self.modelCount))    
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
        
        if cmp(spider.name, 'chezhuBrandSpider') == 0:
            #车品牌，车系爬取
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
                    #写入本地sqlite
    #                 self.cursor.execute("replace into t_bx_car_brand(brandId, brandName, baseId, baseName, firstLetter) values(?, ?, ?, ?, ?)", (int(brandId), brandName, int(baseBrandId), baseBrandName, firstLetter))
                    #写入mysql
                    curTime = (time.time())*1000
                    sql = "REPLACE into t_bx_car_brand(id,status,delFlag,createTime,modifyTime,brandName,charName, baseId, baseName) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"     
                    param = (str(brandId),0,0,curTime,curTime,brandName.encode('utf8'), firstLetter, str(baseBrandId), baseBrandName.encode('utf8'))
                     
                    self.cursor.execute(sql,param)
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
                        #写入sqlite数据库
    #                     self.cursor.execute("replace into t_bx_car_series(seriesId, seriesName, brandId) values(?, ?, ?)", (int(seriesId), seriesName, int(seriesBrandId)))
    
                        #写入mysql
                        curTime = (time.time()) * 1000
                        sql = "REPLACE into t_bx_car_series(id,status,delFlag,createTime,modifyTime,seriesName,brandId) values(%s,%s,%s,%s,%s,%s,%s)"     
                        param = (str(seriesId),0,0,curTime,curTime,seriesName.encode('utf8'), str(seriesBrandId))
                         
                        self.cursor.execute(sql,param)
                        self.seriesCount = (self.seriesCount+1)
                        
                    except:
                        print('car_db_series_error:')                    
            elif cmp(itemClassName, 'ChezhuhomeModelItem') == 0:    
                print('itemClassName=', itemClassName)
                
        elif cmp(spider.name, 'chezhuModelSpider') == 0:
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
    #                 self.cursor.execute("replace into t_kk_model(modelId, modelName, price4S, priceReal, priceManufacturer, year, seriesId) values(?, ?, ?, ?, ?, ?, ?)", (int(modelId), modelName, price4S, priceReal, priceManufacturer, year, int(seriesId)))
                    curTime = time.time() * 1000
                    sql = "REPLACE into t_bx_car_model(id,status,delFlag,createTime,modifyTime,modelName,modelYear,seriesId, price4S, priceReal, priceManufacturer) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"     
                    param = (str(modelId),0,0,curTime,curTime,modelName.encode('utf8'), year, str(seriesId), price4S.encode('utf8'), priceReal.encode('utf8'),priceManufacturer.encode('utf8'))
                    
                    self.cursor.execute(sql,param)
                    self.modelCount = (self.modelCount+1)
                #写入数据库:车品牌
                except:
                    print('car_db_model_error:')
        else:
            pass
        
        return item
    