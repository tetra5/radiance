# -*- coding: utf-8 -*-


import os

from dev.compilers import compile_ui, scan_translations, \
    compile_translations, compile_resources
from logic.misc.pyfs import recursive_glob
from settings import settings


#===============================================================================
#
# ! RUN AS ROOT TO GENERATE TRANSLATION STRINGS AND COMPILE TRANSLATION FILES !
#
# ! THIS SCRIPT ONLY COMPILES UI AND RESOURCES WITHOUT ROOT ACCESS !
#
#===============================================================================


if __name__ == '__main__':
    search_dir = './'
    
    
    #===========================================================================
    # CHANGE THOSE SETTINGS IF NEEDED
    #===========================================================================
    
    # translation file path
    ts_file = os.path.abspath('./i18n/radiance_%s.ts' % settings.get('locale'))
    rc_out_path = os.path.abspath('./ui/gui') # compiled resources output path
    
    
    
    # ! DO NOT TOUCH !
    # VVVVVVVVVVVVVVVV
    
    
    # compiles *.ui --> *.py to the same dir
    ui_files = list(recursive_glob(search_dir, '*.ui'))
    print 'Compiling %d UI file(s) ...' % len(ui_files)
    try:
        compile_ui(ui_files)
    except Exception, e:
        print '...error: %s.' % e
    else:
        print '...done.'
        
    print
    
    
    # compiles resources *.qrc -> *_rc.py to the specified directory
    qrc_files = list(recursive_glob(search_dir, '*.qrc'))
    print 'Compiling %d resource file(s) to %s ...' % (len(qrc_files), rc_out_path)
    try:
        compile_resources(qrc_files, rc_out_path)
    except Exception, e:
        print '...error: %s.' % e
    else:
        print '...done.'
    
    print
    
    
    # search *.py for pyqt translation strings, compiling them into a single
    # translation file specified
    py_files = list(recursive_glob(search_dir, '*.py'))
    print 'Scanning %d source file(s) for string translations to %s ...' \
        % (len(py_files), ts_file)
    try:
        scan_translations(py_files, ts_file)
    except Exception, e:
        print '...error: %s' % e
    else:
        print '...done.'
        print
        
        # compiles *.qm files to the same dir with *.ts files
        ts_files = list(recursive_glob(search_dir, '*.ts'))
        print ''.join([
                       'You can now use Qt Linguist to translate: ',
                       ', '.join(ts_files),
                       '.',
                       ])
        
        print
        print 'You can also skip this step.'
        print 
        
        raw_input('Press Enter when done.')
        
        print
        print 'Compiling %d translation file(s) ...' % len(ts_files)
        try:
            compile_translations(ts_files)
        except Exception, e:
            print '...error: %s.' % e
        else:
            print '...done.'
