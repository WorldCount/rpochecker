#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 01.03.2013

@author: WorldCount
'''

"""Работа с дубликатами!"""

import os
import hashlib
import error


def getHash(root):
    """"Возвращает хеш файла. Если файл не найден, возбуждает исключение типа FileNotFound"""

    # Объект хеша
    fileHash = hashlib.md5()
    
    # Если файл существует,
    if os.path.exists(root):
        # открываем, 
        with open(root, u'rb') as myFile:
            
            # считываем его по-байтово,
            while True:
                content = myFile.read(1024)
                if content == '':
                    break
                # и добавляем информацию в хеш.
                fileHash.update(content)
        # Возвращаем полученный хеш в 16-ом виде.
        return fileHash.hexdigest()
    # Если файла не существует
    else:
        raise error.FileNotFound()
                
    

def isDup(oneRoot, twoRoot):
    """Возвращает является ли файл дубликатом"""
    
    # Получаем хеш файлов
    try:
        oneHash = getHash(oneRoot)
    except error.FileNotFound:
        return u"Ошибка, файл '" + oneRoot + u"' не найден!"
    try:
        twoHash = getHash(twoRoot)
    except error.FileNotFound:
        return u"Ошибка, файл '" + twoRoot + u"' не найден!"

    # Проверяем на дубликат
    if oneHash == twoHash:
        return True
    else:
        return False