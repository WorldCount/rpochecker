#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 02.04.2013

@author: WorldCount
'''

"""Сохранение файлов в БД"""

import database

class DataSave(database.DataBase):
    
    
    def __init__(self):
        
        database.DataBase.__init__(self)
        
        # Список с данными файлов
        self.dataBaseList = []
        self.dataPartList = []
        self.dataWinList = []
        self.dataDWList = []
        self.dataUnkownList = []
        
        # Счетчики файлов
        self.countAllFile = 0
        self.countDupFile = 0
        self.countNewFile = 0
        
        
    def addBase(self, fileObject):
        """Собирает список с данными файлов"""
        
        # Считаем файл
        self.countAllFile += 1
        
        # Версия ПО
        fileVersion = fileObject.version
        
        if fileObject.fileType == "BaseOps":
            fileVersion = "Base"
            
        with self.connect() as conn:
            
            fileDup = 0
            
            # Проверяем на дубликат по хешу и номеру файла
            curr = conn.cursor()
            # Формируем и отправляем запрос
            query = "select file_date_stamp from " + fileObject.fileType + " where file_hash = ? and num_file = ? limit 1"
            curr.execute(query, (fileObject.hash, fileObject.name,))
            # Если найденных записей больше нуля, то это дубль
            if len(curr.fetchall()) > 0:
                fileDup = 1
                # Считаем дубль
                self.countDupFile += 1
            else:
                fileDup = 0
                # Считаем новый файл
                self.countNewFile += 1
                
        if fileObject.fileType == "BaseOps":
            self.dataBaseList.append((fileObject.name, fileObject.ops, fileObject.date, fileObject.hash, fileDup, fileVersion, fileObject.string, fileObject.error))
        elif fileObject.fileType == "WinPost":
            self.dataWinList.append((fileObject.name, fileObject.ops, fileObject.date, fileObject.hash, fileDup, fileVersion, fileObject.string, fileObject.error))
        elif fileObject.fileType == "PartPost":
            self.dataPartList.append((fileObject.name, fileObject.ops, fileObject.date, fileObject.hash, fileDup, fileVersion, fileObject.string, fileObject.error))
        elif fileObject.fileType == "DW":
            self.dataDWList.append((fileObject.name, fileObject.ops, fileObject.date, fileObject.hash, fileDup, fileVersion, fileObject.string, fileObject.error))
        else:
            self.dataUnkownList.append((fileObject.name, fileObject.ops, fileObject.date, fileObject.hash, fileDup, fileVersion, fileObject.string, fileObject.error))
        
        
    def save(self):
        """Сохраняет объект в базу"""
        
        query1 = """insert into PartPost (num_file, num_ops, file_date_stamp, file_hash, dup, file_soft, num_string, num_error) values (?, ?, ?, ?, ?, ?, ?, ?)"""
        query2 = """insert into BaseOps (num_file, num_ops, file_date_stamp, file_hash, dup, file_soft, num_string, num_error) values (?, ?, ?, ?, ?, ?, ?, ?)"""
        query3 = """insert into DW (num_file, num_ops, file_date_stamp, file_hash, dup, file_soft, num_string, num_error) values (?, ?, ?, ?, ?, ?, ?, ?)"""
        query4 = """insert into WinPost (num_file, num_ops, file_date_stamp, file_hash, dup, file_soft, num_string, num_error) values (?, ?, ?, ?, ?, ?, ?, ?)"""
        query5 = """insert into Unkown (num_file, num_ops, file_date_stamp, file_hash, dup, file_soft, num_string, num_error) values (?, ?, ?, ?, ?, ?, ?, ?)"""
        
        with self.connect() as conn:
            
            # Выполняем по одному запросу на список
            curr = conn.cursor()
            curr.executemany(query1, self.dataPartList)
            curr.executemany(query2, self.dataBaseList)
            curr.executemany(query3, self.dataDWList)
            curr.executemany(query4, self.dataWinList)
            curr.executemany(query5, self.dataUnkownList)
            
        # Очистили списки
        self.dataBaseList = []
        self.dataPartList = []
        self.dataWinList = []
        self.dataDWList = []
        self.dataUnkownList = []
        
            
    def getCountFiles(self):
        """Возвращает список со счетчиками файлов"""
        return [self.countAllFile, self.countDupFile, self.countNewFile]
        
            
            
            
if __name__ == "__main__":
    print u"Error: Importing This Module."