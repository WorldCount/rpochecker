#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 30.09.2013

@author: WorldCount
'''

import os.path
import shutil
from datetime import datetime
from wc import utils
from engine import config
from postparser.postparser import PostParser
from engine.datasave import DataSave

# Управление файлами

class FileControl(object):
    
    
    def __init__(self):
        
        # Читаем конфиг
        self.cfg = config.Config()
        # Количество перемещенных базовых файлов
        self.numBaseMove = 0
                
    
    
    def run(self, listFiles):
        """ Расскидывает файлы по папкам """
        
        db = DataSave()
        
        # Перебираем файлы по очереди
        for rpoFile in listFiles:
            
            # Получаем имя файла
            nameFile = os.path.basename(rpoFile)
            
            # Если имя файла совпадает с именем базового ОПС
            if nameFile[:6] == self.cfg.Base['ops']:
                
                parser = PostParser(rpoFile)
                baseFile = parser.load()
                db.addBase(baseFile)
                # То перемещаем на отправку
                self.moveBase(rpoFile)
                # Прибавляем 1 к перемещенным базовым файлам
                self.numBaseMove += 1
                continue
            
            # Делаем копию
            self.getReserve(rpoFile)
            # Перемещаем в рабочую директорию
            self.moveWork(rpoFile)
            
        db.save()
        
    
    
    def moveBase(self, fileLink):
        """ Перемещает базовый файл для отправки """
        
        # Получаем имя файла
        nameFile = os.path.basename(fileLink)
        # Полный путь для перемещения базового файла
        moveDir = self.cfg.Base['exit'] + nameFile
        
        # Если папки еще не существует, то создаем
        if not os.path.exists(self.cfg.Base['exit']):
            os.makedirs(self.cfg.Base['exit'])
            
        # Перемещаем файл
        shutil.move(fileLink, moveDir)
        
        
    def moveWork(self, fileLink):
        """ Перемещает файлы в рабочую директорию """
        
        # Получаем имя файла
        fileName = os.path.basename(fileLink)
        
        # Если путь не задан в конфиге
        if self.cfg.AEC['work'] == "":
            # задаем ручками
            self.cfg.AEC['work'] = "work\\"
        
        # Директория скрипта
        scriptDir = utils.getScriptDir()
        # Рабочая папка
        workDir = utils.setSlash(self.cfg.AEC['work'])
        # Полный путь для перемещения файла в рабочую директорию
        moveDir = scriptDir + workDir + fileName
        
        # Если папки еще не существует, то создаем
        if not os.path.exists(self.cfg.AEC['work']):
            os.makedirs(self.cfg.AEC['work'])
            
        # Перемещаем файл
        shutil.move(fileLink, moveDir)
    
    
    def getReserve(self, fileLink):
        """ Делает резервную копию файла """
        
        # Получаем имя файла
        fileName = os.path.basename(fileLink)
        
        # Если путь не задан в конфиге
        if self.cfg.AEC['reserve'] == "":
            # задаем ручками
            self.cfg.AEC['reserve'] = "reserve\\"
            
        # Добавляем слеши в конце, если их нету
        reserveDir = utils.setSlash(self.cfg.AEC['reserve'])
        # Получаем сегодняшнюю дату
        date = datetime.now()
        # Формируем полный путь до папки с резервом
        reserveDir = utils.getScriptDir() + reserveDir + "%02d\\%02d\\%02d\\" % (date.year, date.month, date.day)
        
        # Если папки еще не существует, то создаем
        if not os.path.exists(reserveDir):
            os.makedirs(reserveDir)
            
        # Создаем полный путь к файлу
        fileFullRoot = reserveDir + fileName
        # Копируем файл в папку с резервными файлами
        shutil.copy(fileLink, fileFullRoot)