#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 02.04.2013

@author: WorldCount
'''


"""Загрузка файлов из БД"""

import database
import datetime
import time


class DataLoad(database.DataBase):
    """Загрузка данных из БД"""
    
    
    def __init__(self):
        
        database.DataBase.__init__(self)
        
        # Полученные данные
        self.dataList = []
        
        
        
        
    def getData(self):
        """Возвращает список с полученными данными"""
        
        return self.dataList


    def load(self, numOps=False, typeFile=False, dateFile=False, dateFileEnd=False, dup=True):
        """Загружает объект из базы"""
        
        # Временой отрезок
        timeFrame = self.timeMask(dateFile, dateFileEnd)
        
        # Начинаем формировать запрос
        query = u"select num_file, file_date_stamp, dup, file_soft, num_string, num_error from "
        
        
        if str(numOps) == self.cfg.Base['ops'] or numOps == False:
            typeFile = False
            numOps = self.cfg.Base['ops']
        
        # из какой таблицы
        if typeFile == False:
            query += u"BaseOps "
        elif typeFile == "PP":
            query += u"PartPost "
        elif typeFile == "WP":
            query += u"WinPost "
        elif typeFile == "DW":
            query += u"DW "
        else:
            query += u"Unkown "
            
        query += u"where num_ops = ? and (file_date_stamp >= ? and file_date_stamp <= ?) "
        
        # Если дубликаты не нужны
        if dup == False:
            query += u"and dup = 0 "
            
        # и отсортируем результат по дате
        query += u"order by file_date_stamp"

        with self.connect() as conn:
            
            # Получаем курсор
            curr = conn.cursor()
            # Выполняем запрос
            curr.execute(query, (numOps, timeFrame[0], timeFrame[1]))
            self.dataList = curr.fetchall()
            
            
    def loadOpsFull(self, numOps=False, dateFile=False, dateFileEnd=False, dup=True):
        """Загружает все файлы опс за день или отрезок"""
        
        # Если файл базовый, то вызываем обычную загрузку
        if (numOps == False) or (str(numOps) == self.cfg.baseOps):
            self.load(numOps, False, dateFile, dateFileEnd, dup)
        else:
            
            # Временой отрезок
            timeFrame = self.timeMask(dateFile, dateFileEnd)
            
            # Начинаем формировать запрос
            query = u"select num_file, file_date_stamp, dup, file_soft, num_string from("
            query += u" select * from DW union all select * from WinPost union all select * from PartPost union all select * from Unkown) "
            query += u"where num_ops = ? and (file_date_stamp >= ? and file_date_stamp <= ?) "
            
            # Если дубликаты не нужны
            if dup == False:
                query += u"and dup = 0 "
                
            # и отсортируем результат по дате
            query += u"order by file_date_stamp"
            
            with self.connect() as conn:
            
                # Получаем курсор
                curr = conn.cursor()
            # Выполняем запрос
                curr.execute(query, (numOps, timeFrame[0], timeFrame[1]))
                self.dataList = curr.fetchall()
            
        
    def loadAllFull(self, dateFile=False, dateFileEnd=False, dup=True):
        """Загружает все файлы за день или отрезок"""
          
        # Временой отрезок
        timeFrame = self.timeMask(dateFile, dateFileEnd)
        
        # Начинаем формировать запрос
        query = u"select num_file, file_date_stamp, dup, file_soft, num_string from("
        query += u" select * from DW union all select * from WinPost union all select * from PartPost union all select * from Unkown) "
        query += u"where (file_date_stamp >= ? and file_date_stamp <= ?) "
        
        # Если дубликаты не нужны
        if dup == False:
            query += u"and dup = 0 "
            
        # и отсортируем результат по дате
        query += u"order by file_date_stamp"
        
        with self.connect() as conn:
        
            # Получаем курсор
            curr = conn.cursor()
        # Выполняем запрос
            curr.execute(query, (timeFrame[0], timeFrame[1]))
            self.dataList = curr.fetchall()
            

    def timeMask(self, dateFile=False, dateFileEnd=False):
        """Возвращает список из 2-х штампов времени"""
        
        # Маска для разбора даты
        mask = "%d.%m.%Y"
        
        if dateFile == False:
            # Начальная дата будет сегодняшняя - 1 день
            dateTemp = datetime.datetime.today().strftime(mask)
            dateStart = datetime.datetime.strptime(dateTemp, mask) - datetime.timedelta(1)
        else:
            # или пользовательская
            dateStart = datetime.datetime.strptime(dateFile, mask)
            

        if dateFileEnd == False:
            if dateFile == False:
                # Если конечной даты нету, то будет начальная дата + 47:59:59
                dateEnd = dateStart + datetime.timedelta(1, 86399)
            else:
                dateEnd = dateStart + datetime.timedelta(0, 86399)
        else:
            # или пользовательская + 23:59:59
            dateEnd = datetime.datetime.strptime(dateFileEnd, mask) + datetime.timedelta(0, 86399)
        
        # Возвращаем даты в секундах
        return [int(time.mktime(dateStart.timetuple())), int(time.mktime(dateEnd.timetuple()))]
        
        
        
        
        