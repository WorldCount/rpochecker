#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 18.03.2013

@author: WorldCount
'''

# Измеряем время работы. Менеджер контента

import time

class Timer(object):
    
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        
        self.end = time.time()
        
        self.secs = self.end - self.start
        
        self.msecs = self.secs * 1000  # millisecs
        
        if self.verbose:
            print u'Затраченное время: %f ms' % self.msecs