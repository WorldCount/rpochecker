#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 12.06.2013

@author: WorldCount
'''

import glob
import sys
import datetime
import os
from engine import config
from postparser.postparser import PostParser
from engine.datasave import DataSave
from engine.dataload import DataLoad
from engine.filecontrol import FileControl
from engine.filter import Filter


class Command(object):
    """Комманды для консоли"""
    
    def __init__(self):
        
        # Загружаем конфиг
        self.cfg = config.Config()
    
    
    def check(self):
        """Проверка файлов"""
        
        # Список поступивших файлов файлов
        maskFiles = glob.glob(self.cfg.Base['fileOpsRoot'] + self.cfg.fileMask)
        # Всего файлов найлено
        numAllFiles = len(maskFiles)
        
        # Расскидываем файлы по папкам
        fileCtrl = FileControl()
        fileCtrl.run(maskFiles)
        
        # Всего базовых файлов перемещено:
        numBaseFiles = fileCtrl.numBaseMove
        
        # Получаем список рабочих файлов
        workFiles = glob.glob(self.cfg.AEC['work'] + self.cfg.fileMask)
        # Всего файлов на обработку
        numWorkFiles = len(workFiles)
        
        # Объект для сохранения данных в БД
        dbSave = DataSave()
        
        # Счетчики для полосы загрузки
        i = 0
        
        # Всего ошибок найдено
        numAllError = 0
        
        # Перебираем файлы
        for rpoFile in workFiles:
            
            # Создаем парсер
            parser = PostParser(rpoFile)
            # Парсим файл
            opsFile = parser.load()
            
            # Работа фильтров
            myFilter = Filter(opsFile)
            # Найдено ошибок в файле
            numFileError = myFilter.error
            # Передаем количество ошибок в файл
            opsFile.error = numFileError
            numAllError += numFileError
            
            # Добавляем в базу
            dbSave.addBase(opsFile)
            # Сохраняем обработанный файл в папку с результатом
            parser.save()
            # Удаляем его из рабочей папки
            os.remove(rpoFile)
            
            # Ведем расчеты для полосы загрузки
            i += 1
            x = (i*100)/numWorkFiles
            # Выводим полосу
            sys.stdout.write(u'\rВыполнено: %s%%' % x)
            sys.stdout.flush()
            
        # Сохраняем в базу
        dbSave.save()
        
        # Получаем информацию
        countList = dbSave.getCountFiles()
        
        # Выводим информацию
        print u"\n\nВсего найдено файлов:", numAllFiles, u"шт.\n"
        
        print u"Из них:"
        print u"    перемещено на отправку -", numBaseFiles, u"шт."
        print u"    перемещено на обработку -", countList[0], u"шт.\n"
        
        print u"Обработка:"
        print u"    всего дубликатов -", countList[1], u"шт."
        print u"    добавленно новых -", countList[2], u"шт."
        print u"\nВсего ошибок найдено: ", numAllError, u"шт.\n"
        
        
        
    def exit(self):
        """Выход из программы"""
        
        print u"\nПока! <(o.O)^"
        exit()
        
    
    def getWP(self, opsNum = False):
        """Выводит данные ОПС по ВинПосту за день"""
        
        self.get(opsNum, "WP")
        
    
    def getPP(self, opsNum = False):
        """Выводит данные ОПС по Партионке за день"""
        
        self.get(opsNum, "PP")
        
    
    def getDW(self, opsNum = False):
        """Выводит данные ОПС по Доставке за день"""
        
        self.get(opsNum, "DW")
        
    
    def getBase(self):
        """Выводит данные по базовому ОПС """
        
        self.get()
    
    
    # ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ
    def isPack(self, link):
        """Проверяет, является ли файл архивом"""
        
        with open(link) as f:
            line = f.readline()
        
        if line[0:2] == "OP":
            return False
        if line[0:2] == "PK":
            return True
        
        
    def get(self, opsNum = False, typeFile = False):
        """Выводит данные ОПС определенного типа за день"""
        
        myConnect = DataLoad()

        if opsNum == False:
            myConnect.load(False, False, False, False, True)
        else:
            myConnect.load(opsNum, typeFile, False, False, True)
            
        self.printData(myConnect.getData())
        print u"\rВсего файлов: ", len(myConnect.getData()), u"шт.\n"
        
        
    def printData(self, myTuple):
        """Выводит полученную информацию в оформлении"""
        
        strFormat = "| %-13s| %-18s| %-7s| %-15s| %-7s| %-6s|"
        num = 79
        
        print "\n" + u"="*num
        print strFormat % (u"Файл:", u"Дата:", u"Дубль:", u"Софт:", u"Строк:", u"Ошибок")
        print u"="*num
        
        for dataFile in myTuple:
            
            genDate = datetime.datetime.fromtimestamp(dataFile[1])
            genDate = genDate.strftime("%d.%m.%y %H:%M:%S")
            if dataFile[2] == 1:
                Dup = u"Да"
            else:
                Dup = u"Нет"
            
            print strFormat % (dataFile[0], genDate, Dup, dataFile[3], dataFile[4], dataFile[5])
            
        print u"-"*num + "\n"