# -*- coding: utf-8 -*-


"""Radiance startup script."""


import sys
import logging
import time
from StringIO import StringIO
import traceback

from PyQt4.QtCore import qWarning

from ui.RApplication import RApplication
from ui.windows.RMainWindow import RMainWindow
from ui.widgets.RSplashScreen import RTSplashScreen
from logic.threads import ImportingThread
from logic.exceptions import TranslationFileLoadingError, \
    TabWidgetIndexOutOfRange, UnsupportedTemplateType


__version__ = '1.1'


def exception_hook(exception_type, exception_value, traceback_obj):
    separator = '-' * 80
    notice = "An unhandled exception occurred."
    time_str = time.strftime("%d.%m.%Y %H:%M:%S")
    tb_info_file = StringIO()
    traceback.print_tb(traceback_obj, None, tb_info_file)
    tb_info_file.seek(0)
    tb_info = tb_info_file.read()
    errmsg = '%s: \n%s' % (str(exception_type), str(exception_value))
    msg = '\n'.join([separator, time_str, separator, errmsg, separator, tb_info])
    qWarning('\n'.join((str(notice), msg)))


def main():
    sys.excepthook = exception_hook
    
    log = logging.getLogger('Radiance')
    f_fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler = logging.FileHandler('radiance.log')
    f_handler.setLevel(logging.DEBUG)
    f_handler.setFormatter(f_fmt)
    log.addHandler(f_handler)
    
    try:
        application = RApplication(sys.argv)
        window = RMainWindow()
        splashscreen = RTSplashScreen(ImportingThread(), window)
        application.exec_()
        
    except TranslationFileLoadingError:
        log.critical('Could not load translation file.')
        return 1
    
    except TabWidgetIndexOutOfRange, index:
        log.critical('Tab widget index %d out of range.' % index)
        return 1
    
    except UnsupportedTemplateType:
        log.critical('Unsupported report template type.')
        return 1
    
    else:
        return 0
    
    
if __name__ == '__main__':
    sys.exit(main())
        
    
def pyinstaller_workaround():
#    import matplotlib
#    import numpy
#    import scipy
    import sqlalchemy
    import scipy.interpolate
    import sqlalchemy.dialects.sqlite
    from PyQt4 import QtNetwork
    import scipy.linalg

    