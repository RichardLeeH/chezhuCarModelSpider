# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import os
import sys
    
#获取当前项目路径
def project_path():
    return os.getcwdu()

#获取当前脚本执行路径
def cur_file_path():
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

#文件或者路径是否存在
def exists(aPath):
    return os.path.exists()

#删除文件或者路径
def remove(aPath):
    if (exists(aPath)):
        os.remove(aPath)
    
#是否文件
def isFile(aPath):
    return os.path.isdir(aPath)

#是否文件夹
def isDir(aPath):
    return os.path.isdir(aPath)

#创建多级目录
def mkdirs(aPath):
    if (exists(aPath)):
        os.makedirs(aPath)

#创建单级目录
def mkdir(aPath):
    if (exists(aPath)):
        os.mkdir(aPath)

#打开文件，如果不存在，则创建一个
def openFile(aName, aMode=0777):
    return os.open(aName, aMode)
 
#获取文件大小
def fileSize(aFileName):
    return os.path.getsize(aFileName)

#关闭文件
def fileClose(aFile):
    aFile.close()

#写入文件
def fileWrite(aFile, aContent):
    aFile.write(aContent)
    