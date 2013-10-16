#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 15.09.2013

@author: WorldCount
'''

""" Проверка EMS в БД """


import database


class DataCheck(database.DataBase):
    """ Проверка EMS в БД """
    
    def __init__(self):
        
        database.DataBase.__init__(self)
        
        
        
    def searchCode(self, value):
        """ Ищет данные в БД """
        
        # Формируем запрос
        query = "select code from Trans where flag = ?"
        
        with self.connect() as conn:
            
            # Получаем курсор
            curr = conn.cursor()
            # Выполняем запрос
            curr.execute(query, (value, ))
            
            # Получаем результат
            response = list(curr.fetchall())
            
            if len(response) < 1:
                return False
            else:
                return response[0][0]
    