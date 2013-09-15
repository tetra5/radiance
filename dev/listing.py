# -*- coding: utf-8 -*-


"""
Created on 11.02.2011

@author: vda
"""


import os

from logic.misc.pyfs import recursive_glob


excluded_files = ['radiance_rc.py']
search_path = '../'


if __name__ == '__main__':
    lines_total = 0
    files_total = 0
    py_files = list(recursive_glob(search_path, '*.py'))
    py_files = [file for file in py_files if file not in excluded_files]
    
    for file in py_files:
        print os.path.basename(file)
            
        with open(file) as f:
            lines = []
            for i, l in enumerate(f):
                if l.strip():
                    lines.append(l)
        print '\n'.join(lines)
        print '(', len(lines), 'lines)', '\n\n\n'
        lines_total += len(lines)
            
    print '(%d lines total, %d files total)' % (lines_total + 1, files_total + 1)
