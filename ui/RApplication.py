# -*- coding: utf-8 -*-


"""
Created on 13.10.2010

@author: vda
"""


import logging

from PyQt4.QtCore import QString, QFile, QIODevice
from PyQt4.QtGui import QApplication, QIcon

from logic.exceptions import StylesheetFileLoadingError
from ui.RTranslator import RTranslator
from ui.gui import radiance_rc


log = logging.getLogger('Radiance')


class RApplication(QApplication):
    def __init__(self, argv):
        super(RApplication, self).__init__(argv)
        self.__init()
        
    def __init(self):
        self.installTranslator(RTranslator(self))
        
        self.setOrganizationName('tetra5')
        self.setOrganizationDomain('tetra5.org')
        self.setApplicationName('Radiance')
        self.setWindowIcon(QIcon(':/Radiance/shield.png'))
        
        try:
            qss = QFile(':/Radiance/styles/default.qss')
            if not qss.open(QIODevice.ReadOnly):
                raise StylesheetFileLoadingError
            qss = qss.readAll()
            stylesheet = QString.fromUtf8(qss)
            self.setStyleSheet(stylesheet)
        except StylesheetFileLoadingError:
            log.error('Could not load default stylesheet file.')
        