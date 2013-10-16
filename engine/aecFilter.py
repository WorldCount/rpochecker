#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 15.08.2013

@author: WorldCount
'''

# Общий файл для всех фильтров

class AECFilter(object):
    
    def __init__(self, fileObject):
        
        # Обьект для работы
        self.fileObject = fileObject
        # Список отправлений
        self.myList = fileObject.listMail
        # Список ошибочных отправлений
        self.errorList = []
        # Список исправленных отправлений
        self.correctList = []
        # Список с финальным результатом
        self.resultList = []
        # Тип файла
        self.typefile = fileObject.version
        
    
    def run(self):
        """ Запускает работу фильтра """
        
        pass
    
    
    def searchError(self):
        """ Ищет ошибки """
        
        pass
    
    def stat(self):
        """ Выводит статистику """
        
        return u"Найдено ошибок: " + str(len(self.errorList)) + u" | Исправлено: " + str(len(self.correctList))
        
    
    
    
    