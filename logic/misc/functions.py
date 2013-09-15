# -*- coding: utf-8 -*-


"""
Created on 18.10.2010

@author: vda
"""


def clean_list(data):
    #[                    [
    # [1.0, 2.0],          [1.0, 2.0],
    # [0.0, 0.0],   -->    ] 
    # ['', 0.0],          
    # ]
    
    for row_num, row in enumerate(data):
        if not all(row):
            # deletes row if any of its elements are False, i.e.
            # http://docs.python.org/library/functions.html#all
            data.pop(row_num) 
            
    return data


def transpose(matrix):
    # [                  [
    #  [0, 1, 2],         [0, 3, 6],
    #  [3, 4, 5],   -->   [1, 4, 7],
    #  [6, 7, 8],         [2, 5, 8],
    #  ]                  ]
    # http://rosettacode.org/wiki/Matrix_transposition#Python
    
    return zip(*matrix) # HOLY SHIT!


def recursive_map(f, data):
    """
    Recursively maps function to a nested iterable of infinite depth.
    
    @param f: function
    @param data: any nested iterable of any depth
    """
    
    return [not hasattr(x, "__iter__") and f(x) or recursive_map(f, x) 
            for x in data]
    
    
def capitalize_first_letter(string):
    l = len(string)
    if l == 0:
        return string
    if l == 1:
        return string[0].capitalize()
    if l > 1:
        return ''.join((string[0].capitalize(), string[1:]))
    
    raise Exception, "Invalid input string."
        