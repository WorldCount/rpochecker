#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 15.08.2013

@author: WorldCount
'''

import postfile, packfile
from engine import config
import csv


# Парсер почтовых файлов

class PostParser(object):
    
    def __init__(self, link):
        
        self.link = link
        self.cfg = config.Config()
        self.pack = self.isPack()
        self.firstString = ["OPERTYPE", "OPERDATE", "BARCODE", "INDEXTO", "MAILDIRECT", "TRANSTYPE", "MAILTYPE", "MAILCTG", "MAILRANK", "SENDCTG", "POSTMARK", "MASS", "PAYMENT", "VALUE", "PAYTYPE", "MASSRATE", "INSRRATE", "AIRRATE", "ADVALTAX", "SALETAX", "RATE", "OPERATTR", "INDEXOPER", "INDEXNEXT", "COMMENT"]
    
    
    
    def isPack(self):
        """Проверяет, является ли файл архивом"""
        
        with open(self.link) as f:
            line = f.readline()
        
        if line[0:2] == "OP":
            return False
        if line[0:2] == "PK":
            return True
        
    
    def load(self):
        """ Загружает файл рпо """
        
        if self.pack:
            myObject = packfile.PostPackFile(self.link)
            myObject.setPack(True)
        else:
            myObject = postfile.PostFile(self.link)
            myObject.setPack(False)
        
        # Оставляем данные объекта себе
        self.workObject = myObject
        return myObject
    
    
    def save(self):
        """ Сохраняет файл в почтовом формате """
        
        # Получаем полный путь для сохранения обработанного файла 
        fileLink = self.cfg.Base['fileOpsRoot'] + self.workObject.name
        
        # Пишим в файл
        with open(fileLink, "wb") as f:
            
            # Формат
            writer = csv.writer(f, delimiter = "|", quotechar='\n')
            # Записываем первую строку
            writer.writerow(self.firstString)
            # И обработанные данные отправлений
            writer.writerows(self.workObject.listMail)
        
    
        