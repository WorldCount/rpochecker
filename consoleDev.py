#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 07.04.2013

@author: WorldCount
'''


from wc.timer import Timer
from engine import consolehelp
from engine import consolecmd


class ConsoleInterface(object):
    
    """Работа из консоли"""
    
    def __init__(self):
        
        
        self.author = u"WorldCount"
        # Список доступных комманд
        self.commandList = ["help", "check", "exit", "getwp", "getpp", "getdw", "getbase"]
        
        # Помощь
        self.help = consolehelp.Help(self.commandList)
        # Обработчик комманд
        self.cmd = consolecmd.Command()
        
        # Консоль
        self.command()
    
    
    
    def command(self):
        """Прием комманд"""
        
        self.consoleHello()
        
        while 1:
            cmd = raw_input('cmd~: ')
            cmdParse = cmd.rsplit(' ')
            
            # Приводим полученную команду к нижнему регистру
            cmdStr = str(cmdParse[0]).lower()
            
            if cmdStr in self.commandList:
                
                # Помощь
                if cmdStr == 'help':
                    
                    if len(cmdParse) > 1: 
                        self.help.getHelp(cmdParse[1])
                    else: 
                        self.help.getHelp(cmdParse[0])
                
                # Выход из программы
                if cmdStr == 'exit': self.cmd.exit()
                
                # Проверка поступивших файлов
                if cmdStr == 'check':
                    with Timer() as t:
                        self.cmd.check()
                    print u"Затраченное время: %.7s сек.\n" % t.secs
                    
                # Данные за винпост
                if cmdStr == "getwp":
                    with Timer() as t:
                        if len(cmdParse) > 1:
                            self.cmd.getWP(cmdParse[1])
                        else:
                            print u"Ошибка, не указан номер ОПС"
                    print u"Затраченное время: %.7s сек.\n" % t.secs
                
                # Данные за партионку
                if cmdStr == "getpp":
                    with Timer() as t:
                        if len(cmdParse) > 1:
                            self.cmd.getPP(cmdParse[1])
                        else:
                            print u"Ошибка, не указан номер ОПС"
                    print u"Затраченное время: %.7s сек.\n" % t.secs
                    
                # Данные за доставку
                if cmdStr == "getdw":
                    with Timer() as t:
                        if len(cmdParse) > 1:
                            self.cmd.getDW(cmdParse[1])
                        else:
                            print u"Ошибка, не указан номер ОПС"
                    print u"Затраченное время: %.7s сек.\n" % t.secs
                    
                # Проверка поступивших файлов группы РПО
                if cmdStr == 'getbase':
                    with Timer() as t:
                        self.cmd.getBase()
                    print u"Затраченное время: %.7s сек.\n" % t.secs
                    
            else:
                print u"Неизвестная команда:", cmdParse[0], "\n"
        
    
    def consoleHello(self):
        
        """Приветствие"""
        
        num = 45
        
        print u"\n" + "-" * num + ">"
        print u"\nВас приветствует [ RpoChecker Console v.0.3 ]"
        print u"Автор:", self.author
        print u"\n" + "-" * num + ">\n"
        
        
if __name__ == "__main__":
    
    ConsoleInterface()
    