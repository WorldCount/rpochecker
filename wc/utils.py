#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 17.11.2012

@author: WorldCount
'''

import datetime
import os.path
import sys

def getCurrentDate():
    '''Получает текущую дату'''
    
    currentdate = datetime.datetime.now()
    
    return currentdate.strftime("%d.%m.%y %H:%M")


def setSlash(string):
    '''Добавляет слеш в конец пути, если его нет'''
    
    num = len(string)
    
    if string[num-1:num] != "\\":
        string += "\\"
    return string


def getScriptDir():
    '''Получает каталог скрипта'''
    
    string = os.path.dirname(sys.argv[0])
    string = setSlash(string)
    
    return string


def getFileDate(fileRoot):
    '''Получает дату изменения файла'''
    
    if os.path.exists(fileRoot):
        stamp = os.path.getmtime(fileRoot)
        dFile = datetime.datetime.fromtimestamp(stamp)
        return dFile.strftime("%d.%m.%y %H:%M")
    else:
        return False
    

def goDateTime(stamp):
    '''Формат даты'''
    
    temp = datetime.datetime.fromtimestamp(stamp)
    return temp.strftime("%d.%m.%y"), temp.strftime("%H:%M:%S")    