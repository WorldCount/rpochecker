#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 15.08.2013

@author: WorldCount
'''

from engine import aecFilter, datacheck
import re

# Фильтр для RA...RU бандеролей

class BND(aecFilter.AECFilter):
    
    def __init__(self, fileObject):
        
        aecFilter.AECFilter.__init__(self, fileObject)
        
        # бъект для работы с базой
        self.db = datacheck.DataCheck()
        
        
    def run(self):
        """ Запуск фильтра """
        
        self.searchError()   
    
    
    def searchError(self):
        """ Ищет ошибочные отправления RA...RU"""
        
        # Верные типы отправлений: Письмо, Бандероль, Мелкий пакет
        listMailType = ["2", "3", "5"]
        
        # Перебираем отправления
        for row in self.myList:
            
            # Если тип фала базовый, то его проверять не надо
            if self.typefile == "Base":
                continue
            
            # Если ШПИ отправления начинается с R
            if row[2][:1] == "R":
                
                # Неизвестная строка ошибочная\или нет
                unkownRow = row
                # Счетчик
                error = 0
                
                # Если тип отправления не входит в верные
                if row[6] not in listMailType:
                    # Исправляем его
                    row[6] = "3"
                    error += 1
                    
                # Если категория отправления не заказное 
                if row[7] != "1":
                    # исправляем
                    row[7] = "1"
                    error += 1
                
                # Текущий флаг страны
                currentFlag = row[2][-2:]
                
                # Текушие данные о стране [(строка с кодом)(код страны)]
                search = re.findall("(CountryFrom=([0-9]+)?)", row[24], re.IGNORECASE)
                
                
                # Если данных нету
                if not search:
                    continue
                
                
                # Если текущий флаг RU и код страны 643, то считаем его CN
                if currentFlag == "RU" and search[0][1] == "643":
                    currentFlag = "CN"
                    error += 1
                elif(currentFlag == "RU" and search[0][1] != "643"):
                    continue
                    
                # Коректный код для текущей страны
                correctCode = self.db.searchCode(currentFlag)
                
                # Если коректный код страны совпадает с текущим, то не правим
                if str(correctCode) == search[0][1]:
                    continue
                # если нет, то
                else:
                    # получаем правильную строку для замены
                    correctString = "CountryFrom=" + str(correctCode)
                    # и заменяем
                    row[24] = row[24].replace(search[0][0], correctString)
                    error += 1
                    
                # Для счетчика ошибок
                if error > 0:
                    # закинули неизвестную строку в ошибочные
                    self.errorList.append(unkownRow)
                    # закинули строку в исправленные
                    self.correctList.append(row)
                    
        # Возвращаем результат работы объекту
        self.resultList = self.myList
                    
                    
                

