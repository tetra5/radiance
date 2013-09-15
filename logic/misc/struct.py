# -*- coding: utf-8 -*-


"""
Created on 13.11.2010

@author: razor
"""


class Struct(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        
                    