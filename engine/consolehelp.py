#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 12.06.2013

@author: WorldCount
'''

class Help(object):
    
    """Помощь по консольным командам"""
    
    
    def __init__(self, cmdList):
        
        # Список доступных комманд
        self.cmdList = cmdList
        # Количество символов
        self.num = 70
        # Формат строки
        self.strFormat = "| %-66s |"
        # Двойная полоска-разделитель
        self.dualBand = u"="*self.num
        # Одинарная полоска-разделитель
        self.singleBand = u"-"*self.num
        
        
    
    def getHelp(self, cmd=False):
        """Помощь по коммандам"""
        
        # Приводим комманду к нижнему регистру
        cmdString = str(cmd).lower()
        
        # КОМАНДЫ
        # help
        if cmd == False or cmdString == u"help":
            self.helpManual()
        # check
        if cmdString == u"check":
            self.helpCheck()
        # get
        if cmdString == u"getwp":
            self.helpGetWP()
        
        
    
    # Обработчики команды getHelp
    def helpManual(self):
        """help"""
        
        print "\n" + self.dualBand
        print self.strFormat % (u"Используйте: help [Команда] для получения справки.")
        print self.dualBand
        print u"\nСписок доступных комманд:\n" + str(self.cmdList)[1:-1] + u"\n"
        
    def helpCheck(self):
        """check"""
        
        print "\n" + self.dualBand
        print self.strFormat % (u"[check] - проверяет поступившие файлы.")
        print self.dualBand + u"\n"
        
    def helpGetWP(self):
        """getWP"""
        
        print "\n" + self.dualBand
        print self.strFormat % (u"[getwp НомерОПС] - выводит файлы WinPost по ОПС.")
        print self.dualBand
        print self.strFormat % (u"Пример использования: ")
        print self.singleBand
        print self.strFormat % (u"getwp 101000")
        print self.dualBand + u"\n"
        