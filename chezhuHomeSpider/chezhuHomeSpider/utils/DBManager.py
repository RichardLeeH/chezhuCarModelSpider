# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import MySQLdb

def connMySQL(aHost, aPort, aUser, aPasswd, aDBName):
    conn = MySQLdb.connect(host=aHost, port = aPort, user=aUser, passwd=aPasswd,db=aDBName)
    cur  = conn.cursor()
    conn.set_character_set('utf8')
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')
    return (conn, cur)