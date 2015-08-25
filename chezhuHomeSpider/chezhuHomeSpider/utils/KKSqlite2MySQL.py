# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import MySQLdb
import sqlite3
import time

class KKSqlite2MySQL():
        
    '''
    连接MySQL数据库
    '''
    def connMySQL(self, aHost, aUser, aPasswd, aDBName):
        conn = MySQLdb.connect(host=aHost, port = 3306, user=aUser, passwd=aPasswd,db=aDBName)
        cur  = conn.cursor()
        conn.set_character_set('utf8')
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        return (conn, cur)
    
    '''
    连接Sqlite数据库
    '''
    def connSqlite(self, aDBName):
        conn = sqlite3.connect(aDBName)
        cur  = conn.cursor()
        return (conn, cur)
        
if __name__ == "__main__":
    
    convertTool = KKSqlite2MySQL()
    
    #连接MySQL
    host = '182.92.0.17'
    user = 'root'
    passwd = '123456'
    dbName = 'kakabaoxiantestdb'
    mysqlInstance = convertTool.connMySQL(host, user, passwd, dbName)

    #连接sqlite数据库
    sqliteDBName = '/Volumes/NormalDisk/scrapyProject/carModelSpider/carModelSpider/kkcar.db'
    sqliteInstance = convertTool.connSqlite(sqliteDBName)
    
    #导入到t_brand 表中
    sqliteInstance[1].execute("select * from t_kk_brand")
    info = sqliteInstance[1].fetchall()
    for ii in info:
        #将数据插入到MySQL的表 t_brand中
        print(ii)
        curTime = (time.time())*1000
        sql = "REPLACE into t_brand(id,status,delFlag,createTime,modifyTime,brandName,charName) values(%s,%s,%s,%s,%s,%s,%s)"     
        param = (str(ii[0]),0,0,curTime,curTime,ii[1].encode('utf8'), ii[2].encode('utf8'))
         
        mysqlInstance[1].execute(sql,param)
     
#     #导入到t_series 表中
    sqliteInstance[1].execute("select * from t_kk_series")
    info = sqliteInstance[1].fetchall()
    for ii in info:
        #将数据插入到MySQL的表 t_brand中
        print(ii)
        curTime = (time.time()) * 1000
        sql = "REPLACE into t_series(id,status,delFlag,createTime,modifyTime,seriesName,brandId) values(%s,%s,%s,%s,%s,%s,%s)"     
        param = (str(ii[0]),0,0,curTime,curTime,ii[1].encode('utf8'), str(ii[2]))
         
        mysqlInstance[1].execute(sql,param)

    #导入到 t_model 表中
    sqliteInstance[1].execute("select * from t_kk_model")
    info = sqliteInstance[1].fetchall()
    for ii in info:
        #将数据插入到MySQL的表 t_brand中
        print(ii)
        curTime = time.time() * 1000
        sql = "REPLACE into t_model(id,status,delFlag,createTime,modifyTime,modelName,modelYear,seriesId, maxPrice, minPrice) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"     
        param = (str(ii[0]),0,0,curTime,curTime,ii[1].encode('utf8'), str(ii[4]), ii[5], ii[2], ii[3])
        
        mysqlInstance[1].execute(sql,param)

    mysqlInstance[0].commit()
    mysqlInstance[1].close()
    mysqlInstance[0].close()
    sqliteInstance[0].commit()
    sqliteInstance[1].close()
    sqliteInstance[0].close()
    
    