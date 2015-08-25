# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# 车品牌，车系解析
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from BeautifulSoup import BeautifulSoup

from ..items import ChezhuhomeBrandItem, ChezhuhomeSeriesItem

import re
import urlparse
import sqlite3

def getSeriesId(aUrl):
    result = urlparse.urlparse(aUrl)
    path = result[2]
    pathList = path.split('/')
    value  = pathList[1]
    return value

def getSubId(aUrl):
    result = urlparse.urlparse(aUrl)
    path = result[2]
    pathList = path.split('/')
    pos = pathList[2].index('.html')
    value  = pathList[2][1:pos]
    return value
    
    return value[0]
def urlParser(aUrl, aKey):
    result = urlparse.urlparse(aUrl)
    params = urlparse.parse_qs(result.query,True) 
    value  = params[aKey]
    return value[0]

def parseName(aLongName):
    pos = aLongName.index('4S')
    return aLongName[0:pos]
    
class KKCarBrandParser(BeautifulSoup):
                            
    def parse_brand(self):
        
        #字典形式数据
        fileBrand = '/Volumes/NormalDisk/scrapyProject/chezhuHomeSpider/chezhuHomeSpider/kakaCar.txt'
        fout = open(fileBrand, 'w') 

        #存储数据库
        kkcardbName = '/Volumes/NormalDisk/scrapyProject/chezhuHomeSpider/chezhuHomeSpider/kkcar.db'
        kkcardb = sqlite3.connect(kkcardbName)
        ################################################################################################
        #########创建表
        try:
            #创建 车品牌表，字段有：品牌ID, 品牌名称，首字母
            kkcardb.execute("create table t_kk_brand (brandId integer primary key, brandName varchar(20), baseId integer, baseName varchar(20), firstLetter varchar(1))")                
            kkcardb.commit()
        except:
            pass
        
        try:
            #创建 车系表，字段有：车系ID, 车系名称，所属品牌ID(外键)
            kkcardb.execute("create table t_kk_series (seriesId integer primary key, seriesName varchar(50), brandId integer)")
            kkcardb.commit()
        except:
            pass
        try:
            #创建 车型表，字段有：车型ID, 车型名称，最高报价，最低报价，年代，所属车系ID(外键)
            kkcardb.execute("create table t_kk_model (modelId integer primary key, modelName varchar(50), maxPrice integer, minPrice integer, year integer, seriesId integer)")    
            kkcardb.commit()           
        except:
            pass
        
        cursor = kkcardb.cursor()
    
        brandItems = [] #存储解析到得品        
        body = self.find('body')
        
        brandList = body.findAll('div', attrs={'class':re.compile('wrap brand_title|brand_box')})

        brandCount = 0
        seriesCount = 0

        firstLetter = 'A'
        for brandItem in brandList:            
            try:
                #判断是否索引字母
                item = brandItem.find('div', attrs={'class':'brand_mane f_l'})
                
                if item:#找到品牌
                    #处理品牌
                    #大品牌ID
                    
                    brandId    = ''
                    brandName  = ''
                    
                    aList = item.findAll('a')
                    
                    #主信息
                    href = aList[1]['href']   
                    brandId = urlParser(href, 'brandId')
                    
                    text = aList[1].text
                    brandName = parseName(text)
                    
                    #子列表
                    item = brandItem.find('div', attrs={'class':'brand_list f_r'})
                    brandSubId   = ''
                    brandSubName = ''
                    
                    if item:
                        #重新解析brand
                        brand_list        = item.findAll('h1')
                        brand_series_list = item.findAll('ul')
                        
                        if brand_list and brand_series_list and (len(brand_list)==len(brand_series_list)):
                            size = len(brand_list)
                            for i in range(0,size):
                                brand_item = brand_list[i]
                                if brand_item:#找到了品牌信息
                                    chezhuBrandItem = ChezhuhomeBrandItem()
                                    
                                    shref   = brand_item.find('a')['href']
                                    brandSubId   = getSubId(shref)
                                    brandSubName = brand_item.find('a').text
                                    
                                    print('car_brand:'+brandId+','+brandName+','+brandSubId+','+brandSubName+','+firstLetter)
                                    chezhuBrandItem['mBrandId']       = brandSubId;
                                    chezhuBrandItem['mBrandName']     = brandSubName;
                                    chezhuBrandItem['mBaseBrandId']   = brandId;
                                    chezhuBrandItem['mBaseBrandName'] = brandName;
                                    chezhuBrandItem['mFirstLetter']   = firstLetter;
                                                
                                    #写入数据库:车品牌
                                    cursor.execute("replace into t_kk_brand(brandId, brandName, baseId, baseName, firstLetter) values(?, ?, ?, ?, ?)", (int(brandSubId), brandSubName, int(brandId), brandName, firstLetter))
                                    kkcardb.commit()
                                    fout.write(('car_brand:'+brandSubId+','+brandSubName+','+brandId+','+brandName+','+firstLetter).encode('utf-8') + '\n')       #将分词好的结果写入到输出文件 
                                    brandCount = (brandCount + 1)

                                    #查找车系
                                    series_item = brand_series_list[i]
                                    if series_item:
                                        chezhuhomeSeriesList = []
                                        seriesList = series_item.findAll('li')
                                        if seriesList:
                                            for series in seriesList:
                                                chezhuhomeSeriesItem = ChezhuhomeSeriesItem()
                                                span = series.find('span', attrs={'class':'name'})
                                                sshref   = span.find('a')['href']
                                                seriesId   = getSeriesId(sshref)
                                                seriesName = span.find('a').text
                                                print('car_series:'+seriesId+','+seriesName+','+brandSubId)
                                                chezhuhomeSeriesItem['mSeriesId']   = seriesId;
                                                chezhuhomeSeriesItem['mSeriesName'] = seriesName;
                                                chezhuhomeSeriesItem['mBrandId']    = brandSubId;
            
                                                #写入数据库:车系
                                                try:
                                                    cursor.execute("replace into t_kk_series(seriesId, seriesName, brandId) values(?, ?, ?)", (int(seriesId), seriesName, int(brandSubId)))
                                                    kkcardb.commit()
                                                    chezhuhomeSeriesList.append(chezhuhomeSeriesItem)
                                                
                                                    seriesCount = (seriesCount + 1)
        
                                                except:
                                                    print('series write=error') 
                                                 
                                        chezhuBrandItem['mSeriesList'] = chezhuhomeSeriesList
                                        #加入到最后的列表中
                                        brandItems.append(chezhuBrandItem)
                                                    
                else:#找到索引字母
                    indexLetter = brandItem.find('span').text
                    firstLetter = indexLetter
                    print('indexLetter='+firstLetter)    
            except:
                pass
            
        kkcardb.commit()
        cursor.close()
        kkcardb.close()
        fout.close()
        print('解析完成')
        
        return brandItems

if __name__ == "__main__" and __package__ is None:

    fp = open("/Volumes/NormalDisk/scrapyProject/chezhuHomeSpider/Sources/chezhuHome.html")
    
    brandParse = KKCarBrandParser(fp.read())
    brandParse.parse_brand()
    
    
    
        
        