#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 14.08.2013

@author: WorldCount
'''

import os.path
import hashlib
from engine.config import Config

# Класс почтового файла

class PostFile(object):
    
    def __init__(self, link):
        
        # Конфиг
        self.cfg = Config()
        # Ссылка на файл
        self.link = link
        # Имя файла
        self.name = os.path.basename(self.link)
        
        # Если есть косяк в имени файла
        if self.name[0] == "c":
            # Исправляем его
            self.name = "1" + self.name[1:]
            
        # Список с отправлениями
        self.listMail = self.getAllMail()
        # Номер отделения
        self.ops = self.name[:6]
        # Количество отправлений в файле
        self.num = len(self.listMail)
        # Дубликат, значение по умолчанию
        self.pack = False
        # Хеш файла
        self.hash = self._hash()
        # Дата файла
        self.date = self._datetime()
        # Версия ПО
        self.version = self._version()
        # Тип файла
        self.fileType = self._fileType()
        # Количество строк
        self.string = len(self.listMail)
        # Количество ошибок в файле
        self.error = 0
    
    
    
    def getAllMail(self):
        """ Получает список отправлений """
        
        # Открываем файл
        with open(self.link, "r") as myFile:
            
            # Возвращаем список
            return self._helpMailFunc(myFile)
    
    
    def _helpMailFunc(self, link):
        """ Вспомогательный метод для _getAllMail()"""
        
        # Парсим
        rpoList = self._postOpen(link)
        # Заносим в опертип
        self.opertype = rpoList[0][0]
        # Удаляем первый элемент из списка
        del rpoList[0]
        
        # Возвращаем список
        return rpoList
        
    
    def setPack(self, value):
        """ Устанавливает значение архивирования файла """
        
        if type(value) is bool:
            self.pack = value
            return True
        else:
            return False
        
    
    def _hash(self):
        """ Возвращает MD5-хеш файла """
        
        fileHash = hashlib.md5()
        
        # Для хеша
        mdSum = ''
        
        # Читаем список отправлений
        for numRPO in self.listMail:
            
            # Складываем в строку номера отправлений
            mdSum += numRPO[2]
                
        # и добавляем информацию в хеш.
        fileHash.update(mdSum)
        # Возвращаем полученный хеш в 16-ом виде.
        return fileHash.hexdigest()
    
    
    def _datetime(self):
        """Возвращает штамп даты и времени файла"""
        
        stamp = os.path.getmtime(self.link)
        return stamp
    
    
    def _version(self):
        """ Определяет версию ПО файла """
        
        softVersion = self.listMail[0][24].split(";")[0]
        
        # ВинПост
        if self.opertype == "OPERTYPE" and softVersion[0] == "W" and self.ops != self.cfg.Base['ops']:
            return softVersion
        else:
            # Список версий ПО в файле
            listVersion = []
            
            # Перебираем строки
            for row in self.listMail:
                
                # Обрезаем строку по ";"
                softVersion = row[24].split(";")[0]
                
                # Если версия есть в списке, то пропускаем
                if softVersion in listVersion:
                    continue
                # Если нет, то добавляем
                else:
                    listVersion.append(softVersion)
            
            # Если версий в списке больше 1, то это базовый файл
            if self.ops == self.cfg.Base['ops'] or len(listVersion) > 1:
                return "Base"
            else:
                
                if len(softVersion) > 7:
                    # Возвращаем только обрезанные версии, т.к. бывают косяки с нарезанием строки по ";"
                    charVersion = listVersion[0][0]
                    
                    # Партионка
                    if charVersion == "P":
                        return softVersion[:5]
                    # Почтовые отправления
                    if charVersion  == "N":
                        return softVersion[:7]
                    # Доставка
                    if charVersion == "D":
                        return softVersion[:5]
                    if charVersion == "R":
                        return softVersion[:7]
                else:
                    return softVersion
            
            
    def _postOpen(self, link):
        """ Открывает и парсит почтовый файл """
        
        # Список с результатом
        myList = []
        
        # и читаем построчно
        for line in link:
            
            # Если строка пустая, то пропускаем её
            if line == "\n":
                continue
            
            # Символ для разбора
            line2 = line[0]
            
            # Если это число, или буква "о", тогда добавляем в список
            if line2.isdigit() or line2.lower() == "o":
                tmpLine = line.rstrip().split("|")
                myList.append(tmpLine)
            # Если нет, то находим предыдущий элемент и добавляем строку к нему
            else:
                myList[-1][-1] = myList[-1][-1] + line.rstrip()
                    
        # Возвращаем распарсенный список
        return myList
    
    
    def _fileType(self):
        """Возвращает тип файла"""
        
        if self.version == "Base":
            
            if int(self.ops) == int(Config().Base['ops']):
                fileType = "BaseOps"
            else:
                fileType = "Unkown"
                
        elif self.version[0] == "W":
            fileType = "WinPost"
        elif self.version[0] == "D":
            fileType = "DW"
        elif self.version[0] == "N" or "P":
            fileType = "PartPost"
        else:
            fileType = "Unkown"
        return fileType