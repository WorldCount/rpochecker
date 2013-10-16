#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 02.03.2013

@author: WorldCount
'''
from wc import utils
from wc import error
import ConfigParser
import sys

class Config(object):
    """Работа с настройками"""
    
    def __init__(self):
        
        
        # Маска для файлов
        self.fileMask = "*.*F"
        # Имя конфиг-файла
        self.nameCfg = "config.ini"
        # Директория конфига
        self.dirCfg = utils.getScriptDir()
        # Полный путь к конфигу
        self.fullCfgRoot = self.dirCfg + self.nameCfg
        # Секция Базового конфига
        self.sectionBaseCfg = "BASE"
        
        # ГЛАВНЫЙ КОНФИГ
        self.Base = {}
        # База данных
        self.Base['base'] = "base.db"
        # Полный путь к БД
        self.Base['fullBaseRoot'] = self.dirCfg + self.Base['base']
        # Индекс базового ОПС
        self.Base['ops'] = "127950"
        # Путь к файлам РПО
        self.Base['fileOpsRoot'] = "C:\\IN\\"
        # Включенные модули
        self.Base['module'] = []
        
        # AEC КОНФИГ
        self.AEC = {}
        
        # Грузим конфиг
        try:
            self.load()
        except error.SectionNotFound:
            print u"Секции: '" + self.sectionBaseCfg + u"' не существует.\nПроверьте конфигурационный файл: '" + self.fullCfgRoot + u"'."
            sys.exit(0)
            
        
        # Если модуль AEC включен
        if "AEC" in self.Base['module']:
            
            # Включаем AEC
            self.AEC['on'] = True
            # Читаем конфиг
            try:
                self.loadAEC()
            except error.SectionNotFound:
                print u"Секции: 'AEC' не существует.\nПроверьте конфигурационный файл: '" + self.fullCfgRoot + u"'."
                sys.exit(0)
        else:
            # Выключаем AEC
            self.AEC['on'] = False
            
        
        
        
    def load(self):
        """ Читает Базовый конфиг """
        
        # Парсер
        configRead = ConfigParser.ConfigParser()
        
        # Читаем конфиг    
        configRead.read(self.fullCfgRoot)
        # Секции в конфиге
        self.listSection = configRead.sections()
        
        # Если есть базовая секция в конфиг файле, то читаем
        if self.sectionBaseCfg in self.listSection:
            
            # Индекс базового ОПС
            self.Base['ops'] = configRead.get(self.sectionBaseCfg,'BaseOps')
            # Имя базы данных
            self.Base['base'] = configRead.get(self.sectionBaseCfg,'Base')
            # Путь к файлам РПО
            self.Base['fileOpsRoot'] = configRead.get(self.sectionBaseCfg, 'FileOpsRoot')
            # Директория с файлами на отправку
            self.Base['exit'] = configRead.get(self.sectionBaseCfg, 'ExitDir')
            # Включенные модули
            self.Base['module'] = configRead.get(self.sectionBaseCfg, 'Module').split(",")
        
        # Если нет, то возбуждаем исключение
        else:
            raise error.SectionNotFound()
            
            
    def loadAEC(self):
        """ Читает конфиг AEC """
        
        # Парсер
        configRead = ConfigParser.ConfigParser()
        
        # Читаем конфиг    
        configRead.read(self.fullCfgRoot)
        
        # Если есть секция модуля AEC в конфиге
        if "AEC" in self.listSection:
            
            # Директория для резервных файлов
            self.AEC['reserve'] = configRead.get("AEC", 'ReserveDir')
            # Рабочая директория AEC
            self.AEC['work'] = configRead.get("AEC", 'WorkDir')
            # Включенные модули AEC
            self.AEC['module'] = configRead.get("AEC", 'Module').split(",")
        
        # Если нет, то возбуждаем исключение
        else:
            raise error.SectionNotFound()
        
        
            
            
        
    

    