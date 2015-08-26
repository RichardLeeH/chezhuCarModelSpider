# -*- coding: utf-8 -*-
# coding=utf-8

# Define here the models for your scraped items
## 车型解析
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from BeautifulSoup import BeautifulSoup

from chezhuHomeSpider.items import ChezhuhomeModelItem

import urlparse
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def getSeriesId(aUrl):
    result = urlparse.urlparse(aUrl)
    path = result[2]
    pathList = path.split('/')
    value  = pathList[1]
    return value

def getModelId(aUrl):
    result = urlparse.urlparse(aUrl)
    path = result[2]
    pathList = path.split('/')
    value  = pathList[2]
    return value

def getOnlyModelId(aUrl):
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
    
def getSeriesIdAndYear(aUrl):
    result = urlparse.urlparse(aUrl)
    path = result[2]
    pathList = path.split('/')
    return (pathList[1], pathList[2])

class KKCarModelParser(BeautifulSoup):
                            
    def parse_Model(self, aUrl):
        
#         #字典形式数据
#         #存储数据库
#         kkcardbName = '/Volumes/NormalDisk/scrapyProject/chezhuHomeSpider/chezhuHomeSpider/kkcar.db'
#         kkcardb = sqlite3.connect(kkcardbName)
#         ################################################################################################
#         #########创建表
#         try:
#             #创建 车型表，字段有：车型ID, 车型名称，最高报价，最低报价，年代，所属车系ID(外键)
#             kkcardb.execute("create table t_kk_model (modelId integer primary key, modelName varchar(50), maxPrice integer, minPrice integer, year integer, seriesId integer)")    
#             kkcardb.commit()           
#         except:
#             pass
        
#         cursor = kkcardb.cursor()
        seiresList = []
        
        body = self.find('body')
        main_left_f_l = body.find('div', attrs={'class':'main_left f_l'})
        if main_left_f_l:
            car_list_tag = main_left_f_l.find('div', attrs={'class':'cars_list'})
            if car_list_tag:
                table_list = car_list_tag.find('table', attrs={'id':'cars_list_1'})
                if table_list:
                    tbody_tag = table_list.find('tbody')
                    
                    tr_list = None
                    if (tbody_tag == None):
                        tr_list = table_list.findAll('tr')
                    else:
                        tbody_tag = table_list.findAll('tr')
                        
                    if tr_list:
                        for tr_item in tr_list:
                            priceManufacturer = ''#厂商指导价
                            price4S           = ''#4S指导价
                            priceReal         = ''#真实报价
                            modelBaseName     = ''#车类型Base名称
                            modelName         = ''#车类型名称
                            modelId           = ''
                            
                            th = tr_item.find('th', attrs={'class':'r_a'})
                            td_list = tr_item.findAll('td')
                            if th:#车类型Base名称
                                pass
                            elif td_list:#车类型名称
                                size = len(td_list)
                                if (size == 5):
                                    for i in range(0,4):
                                        a_tag = td_list[i].find('a')
                                        if a_tag:
                                            if 0 == i:#模型名称及ID
                                                modelName = a_tag.text
                                                model_href = a_tag['href']
                                                modelId  = getModelId(model_href)
                                            elif 1 == i:#厂商指导价
                                                priceManufacturer = a_tag.text
                                            elif 2 == i:#厂商指导价
                                                price4S = a_tag.text
                                            elif 3 == i:#厂商指导价
                                                priceReal = a_tag.text
                                    seriesAndYear = getSeriesIdAndYear(aUrl)
                                    modelItem = ChezhuhomeModelItem()
                                    modelItem['mModelId']   = modelId
                                    modelItem['mModelName'] = modelName
                                    modelItem['mYear']      = seriesAndYear[1]
                                    modelItem['mSeriesId']  = seriesAndYear[0]
                                    modelItem['mPrice4S']   = price4S
                                    modelItem['mPriceReal'] = priceReal
                                    modelItem['mPriceManufacturer'] = priceManufacturer

                                    seiresList.append(modelItem)
                                         
                                    print('model='+modelId+','+modelName+','+seriesAndYear[1]+','+priceManufacturer+','+price4S+','+priceReal+','+seriesAndYear[0])
                    
        print('解析完成')
        return seiresList
     
    def parse_year(self):
        
        yearList = []
        
        headMenu = self.find('div', attrs={'class':'head_menu'})
        
        if headMenu:
            topNav = headMenu.find('div', attrs={'id':'topnav'})
            if topNav:
                head_list_tag = topNav.find('div', attrs={'class':'head_list'})
                if head_list_tag:
                    span_list_tag = head_list_tag.find('span', attrs={'class':'list'})
                    if span_list_tag:
                        year_list = span_list_tag.findAll('a')
                        if year_list:
                            for year_item in year_list:
                                year_href = year_item['href']
                                year_name = year_item.text
                                lenght = len(year_name)
                                year = year_name[0:4]
                                if (4 != lenght):
                                    yearList.append(year_href)
                                    print('addYear='+year_href)
        return yearList        
    
    def getPiceManufacturer(self, content):
        h1_tag = content.find('h1')
        if h1_tag:
            price = h1_tag.find('b')
            if price:
                return price.text
            
        return ''
    
    def getPrice(self, content):
        price = ('','')
        dl_tag = content.find('dl')
        if dl_tag:
            dd_tag_list = dl_tag.findAll('dd')
            if dd_tag_list and len(dd_tag_list) > 0:
                priceItem = dd_tag_list[1]
                print('aaa='+priceItem.text)
                print('bbb='+priceItem.find('span').text)
                tmp1 = priceItem.text
                tmp2 = priceItem.find('span').text
                pos = tmp1.index(tmp2)
                tmp3 = tmp1[0:pos]

                print('aaa='+tmp1)
                print('bbb='+tmp2)                
                print('ccc='+tmp3)                
                
                price4S = (tmp3.split(('：')))[1]
                
                priceReal = (tmp2.split(('：')))[1]
                return (price4S, priceReal)
                
        return price
                
    def parse_onlyModel(self, aUrl):
        modelName = ''
        modelId   = ''
        seriesId  = getSeriesId(aUrl)
        year      = '0000'
        price4S   = '暂无'
        priceReal = '暂无'
        priceManufacturer = '暂无'
        #获取车型名称和ID
        headMenu = self.find('div', attrs={'class':'head_menu'})        
        if headMenu:
            topNav = headMenu.find('div', attrs={'id':'topnav'})
            if topNav:
                head_list_tag = topNav.find('div', attrs={'class':'head_list'})
                if head_list_tag:
                    span_list_tag = head_list_tag.find('span', attrs={'class':'name'})
                    if span_list_tag:
                        model_tag = span_list_tag.find('a')
                        if model_tag:
                            modelName = model_tag.text
                            href      = model_tag['href']
                            modelId   = getOnlyModelId(href)
        #获取车型其他信息
        carInfo = self.find('div', attrs={'class':'wrap'}) 
        if carInfo:
            div_main_left_f_l = carInfo.find('div', attrs={'class':'main_left f_l'})
            if div_main_left_f_l:
                div_cars_info = div_main_left_f_l.find('div', attrs={'class':'cars_info'})
                if div_cars_info:
                    div_cars_show_f_l = div_cars_info.find('div', attrs={'class':'cars_show f_l'})
                    if div_cars_show_f_l:
                        div_show_box = div_cars_show_f_l.find('div', attrs={'class':'show_box'})
                        if div_show_box:
                            priceManufacturer = self.getPiceManufacturer(div_show_box)
                            otherPrice = self.getPrice(div_show_box)
                            price4S    = otherPrice[0]
                            priceReal  = otherPrice[1]
        
        modelItem = ChezhuhomeModelItem()
        modelItem['mModelId']   = seriesId
        modelItem['mModelName'] = modelName
        modelItem['mYear']      = year
        modelItem['mSeriesId']  = seriesId
        modelItem['mPrice4S']   = price4S
        modelItem['mPriceReal'] = priceReal
        modelItem['mPriceManufacturer'] = priceManufacturer
        print('modelItem='+str(modelItem))     
        return modelItem
                           
if __name__ == "__main__":

    fp = open("/Volumes/NormalDisk/scrapyProject/chezhuHomeSpider/chezhuHomeSpider/Sources/125955.html")
    
    brandParse = KKCarModelParser(fp.read())
 
    yearList = brandParse.parse_year()
    
    brandParse.parse_onlyModel('http://www.16888.com/125955')
    
    
    
        
        