#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 15.08.2013

@author: WorldCount
'''

from engine import aecFilter
import re
# Фильтр для EMS

class EMS(aecFilter.AECFilter):
    
    def __init__(self, fileObject):
        aecFilter.AECFilter.__init__(self, fileObject)

        
        
        
    def run(self):
        """ Запуск фильтра """
        
        self.searchError()
        
    
    def searchError(self):
        """ Ищет ошибочные отправления EMS"""
        
        # Перебираем отправления
        for row in self.myList:
            
            # Если тип фала базовый, то его проверять не надо
            if self.typefile == "Base":
                continue
            
            # Ищем EMS, прием
            if row[2][:2] == "EA" and row[0] == "1":
                
                
                # Получаем значение из поля COMMENT
                myStr = row[24]
                # Ищем данные об отправителе
                search = re.findall("(Sndr=[а-яА-Я]+)", myStr.decode("cp866").encode("utf8"))
                
                try:
                    # Если данные найдены, то править не надо
                    if search[0]:
                        continue
                # Если данных нету
                except IndexError:
                    
                    # Добавляем EMS к ошибочным
                    self.errorList.append(row)
                    
                    # Исправляем
                    row[24] = row[24].replace("Sndr=", "Sndr=Рогов".decode("utf8").encode("cp866"))
                    
                    # Добавляем EMS к исправленным
                    self.correctList.append(row)
        
        # Возвращаем результат работы объекту
        self.resultList = self.myList
             
    
    