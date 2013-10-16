#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 01.03.2013

@author: WorldCount
'''

# Классы ошибок


class NotFound(Exception):
    pass

class FileNotFound(NotFound):
    pass

class SectionNotFound(NotFound):
    pass