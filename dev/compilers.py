# -*- coding: utf-8 -*-


"""
Created on 13.10.2010

@author: vda
"""


import os
from distutils.sysconfig import get_python_lib
import subprocess

from PyQt4.uic import compileUi


#===============================================================================
# ui files compiler
#===============================================================================
def compile_ui(files):
    """
    Compiles *.ui files into a *.py files. Generated files are stored in the
    same directory.
    
    @param files: list of files
    """
    
    for uipath in files:
        try:
            compile_ui_file(uipath)
        except:
            raise
        

def compile_ui_file(uipath):
    if not uipath.endswith('.ui'):
        raise Exception, 'Invalid UI file %s.' % uipath
    
    
    with open(''.join((uipath[:-2], 'py')), 'w') as pyfile: # *.ui --> *.py
        with open(uipath, 'r') as uifile:
            try:
                compileUi(uifile, pyfile)
            except:
                raise Exception, 'Could not compile UI file %s.' % uipath

    
#===============================================================================
# translations compiler
#===============================================================================
def scan_translations(files, ts_file):
    pylupdate4_path = os.path.abspath(os.path.join(get_python_lib(),
                                                   'PyQt4/bin/pylupdate4.exe'))
    ts_file = os.path.abspath(ts_file)
    cmd = ' '.join([
                    pylupdate4_path, 
                    ' '.join(files), 
                    '-noobsolete', 
                    '-ts',
                    ts_file,
                    ])
    
    try:
        retcode = subprocess.call(cmd)
    except WindowsError as (errno, errstr):
        if errno == 740:
            raise Exception, 'Root access required.'
        else:
            raise Exception, 'Error #%d: %s' % (errno, errstr)
    else:
        if retcode > 0:
            raise Exception, 'Error: process returned %d.' % retcode
        elif retcode < 0:
            raise Exception, 'Error: process terminated by signal %d.' % retcode


#===============================================================================
# translations compiler (qm)
#===============================================================================
def compile_translations(files):
    for ts_file in files:
        try:
            compile_translations_qm_file(ts_file)
        except:
            raise
    
    
def compile_translations_qm_file(ts_file):
    if not ts_file.endswith('.ts'):
        raise Exception, 'Invalid TS file %s.' % ts_file
    
    lrelease_path = os.path.abspath(os.path.join(get_python_lib(),
                                                 'PyQt4/bin/lrelease.exe'))
    
    ts_path = os.path.abspath(ts_file)
    qm_path = ''.join((ts_path[:-2], 'qm'))
    
    cmd = ' '.join([
                    lrelease_path,
                    '-silent',
                    '-compress',
                    ts_path,
                    '-qm',
                    qm_path,
                    ])
    
    try:
        retcode = subprocess.call(cmd)
    except WindowsError as (errno, errstr):
        if errno == 740:
            raise Exception, 'Root access required.'
        else:
            raise Exception, 'Error #%d: %s' % (errno, errstr)
    else:
        if retcode > 0:
            raise Exception, 'Error: process returned %d.' % retcode
        elif retcode < 0:
            raise Exception, 'Error: process terminated by signal %d.' % retcode
        

#===============================================================================
# resources compiler
#===============================================================================
def compile_resources(files, out_path):
    for rc_file in files:
        try:
            compile_resources_rc_file(rc_file, out_path)
        except:
            raise
        

def compile_resources_rc_file(qrc_file, out_path, compress_level=9):
    if not qrc_file.endswith('.qrc'):
        raise Exception, 'Invalid RC file %s.' % qrc_file
    
    pyrcc4_path = os.path.abspath(os.path.join(get_python_lib(),
                                               'PyQt4/bin/pyrcc4.exe'))
    
    qrc_path = os.path.abspath(qrc_file)
    
    rc_path = os.path.join(out_path, ''.join((os.path.basename(qrc_path)[:-4], 
                                              '_rc.py')))
    
    cmd = ' '.join([
                    pyrcc4_path,
                    '-o',
                    rc_path,
                    '-compress',
                    str(compress_level),
                    qrc_path,
                    ])
    
    try:
        retcode = subprocess.call(cmd)
    except WindowsError as (errno, errstr):
        if errno == 740:
            raise Exception, 'Root access required.'
        else:
            raise Exception, 'Error #%d: %s' % (errno, errstr)
    else:
        if retcode > 0:
            raise Exception, 'Error: process returned %d.' % retcode
        elif retcode < 0:
            raise Exception, 'Error: process terminated by signal %d.' % retcode
        
