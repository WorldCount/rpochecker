#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 15.09.2013

@author: WorldCount
'''

from engine import config
from filters import ems, bnd

# Запуск фильтров для AEC

class Filter(object):
    
    def __init__(self, fileObject):
        
        # Объект для работы
        self.fileObject = fileObject
        # Конфиг
        self.cfg = config.Config()
        # Ошибки в файле
        self.error = 0
        
        # Запускаем фильтр
        self.run()
        
        
    def run(self):
        """ Запускает работу фильтров """
        
        # Если включен EMS-фильтр
        if "EMS" in self.cfg.AEC['module']:
            myFilter = ems.EMS(self.fileObject)
            myFilter.run()
            self.error += len(myFilter.errorList)
        
        # Если включен BND-фильтр    
        if "BND" in self.cfg.AEC['module']:
            myFilter = bnd.BND(self.fileObject)
            myFilter.run()
            self.error += len(myFilter.errorList)
        