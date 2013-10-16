#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 14.08.2013

@author: WorldCount
'''

from postparser import postfile
from zipfile import ZipFile

# Класс упакованного почтового файла

class PostPackFile(postfile.PostFile):
    
    def __init__(self, link):
        
        postfile.PostFile.__init__(self, link)
        
        
    def getAllMail(self):
        """ Получает список отправлений """
        
        with ZipFile(self.link) as myZip:
            
            # Открываем архив и ищем файл
            f = myZip.namelist()[0]
            
            # открываем файл и передаем дескриптор дальше
            return self._helpMailFunc(myZip.open(f))
