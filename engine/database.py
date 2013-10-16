#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 02.03.2013

@author: WorldCount
'''

import sqlite3
from engine import config
import os.path
import csv
import sys

"""Общий класс БД"""

class DataBase(object):
    """Работа с базой"""
    
    
    def __init__(self):
        
        # Загружаем конфиг
        self.cfg = config.Config()
        
        # Файл с данными МЖД
        self.emsLink = "ems_data.wc"
        
        # Если нет базы данных, то создаем её
        if not os.path.exists(self.cfg.Base['base']):
            self.createDatabase()
    
    
    
    
    def connect(self):
        """Соединение с БД."""
        
        return sqlite3.connect(self.cfg.Base['base'])
    
    
    def createDatabase(self):
        """Создание новой базы данных"""
        
        with self.connect() as conn:
            
            curr = conn.cursor()
            
            # Таблица для ВинПоста
            curr.execute("""
                create table WinPost(
                id integer not null primary key autoincrement,
                num_file text not null,
                num_ops integer not null,
                file_date_stamp real not null,
                file_hash text not null,
                dup integer null,
                file_soft text not null,
                num_string integer,
                num_error integer
                );
                """
            )
            
            # Таблица для ПартПоста
            curr.execute("""
                create table PartPost(
                id integer not null primary key autoincrement,
                num_file text not null,
                num_ops integer not null,
                file_date_stamp real not null,
                file_hash text not null,
                dup integer null,
                file_soft text not null,
                num_string integer,
                num_error integer
                );
                """
            )
            
            # Таблица для Доставки
            curr.execute("""
                create table DW(
                id integer not null primary key autoincrement,
                num_file text not null,
                num_ops integer not null,
                file_date_stamp real not null,
                file_hash text not null,
                dup integer null,
                file_soft text not null,
                num_string integer,
                num_error integer
                );
                """
            )
            
            # Таблица для Базового ОПС
            curr.execute("""
                create table BaseOps(
                id integer not null primary key autoincrement,
                num_file text not null,
                num_ops integer not null,
                file_date_stamp real not null,
                file_hash text not null,
                dup integer null,
                file_soft text not null,
                num_string integer,
                num_error integer
                );
                """
            )
            
            # Таблица для Неизвестной Версии ПО
            curr.execute("""
                create table Unkown(
                id integer not null primary key autoincrement,
                num_file text not null,
                num_ops integer not null,
                file_date_stamp real not null,
                file_hash text not null,
                dup integer null,
                file_soft text not null,
                num_string integer,
                num_error integer
                );
                """
            )
            
            
            # Таблица для Международных
            curr.execute("""
                create table Trans(
                flag  text not null primary key,
                runame text not null,
                enname text not null,
                code integer null
                );
                """
            )
            
            # Получаем данные МЖД
            self.tmpList = self.parseEms() 
            # Формируем запрос на заполнение таблицы МЖД
            query = """insert into Trans (flag, runame, enname, code) values (?, ?, ?, ?)"""
            # Вставляем данные в БД
            curr.executemany(query, self.tmpList)
            
            
    def reCreateDatabase(self):
        """Пересоздает базу данных"""
        
        os.remove(self.cfg.fullBaseRoot)
        self.createDatabase()
            
            
    def parseEms(self):
        """Парсит данные по МЖД"""
        
        # Если файла нету, то закрываем программу
        if not os.path.exists(self.emsLink):
            u"Нету файла с данными по МЖД"
            sys.exit(0)
        
        # Открываем файл
        with open(self.emsLink, "rb") as emsList:
            
            # Парсим
            dataList = csv.reader(emsList, delimiter = "|", quotechar='\n')
            # Преобразуем в список
            result = list(dataList)
            
            for myStr in result:
                
                myStr[1] = myStr[1].decode("utf8")
            
            # Возвращаем результат
            return result
           
            

    

if __name__ == "__main__":
    print u"Error: Importing This Module."