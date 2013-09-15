# -*- coding: utf-8 -*-


"""
Created on 02.03.2011

@author: vda
"""

import os

from PyQt4.QtCore import QTranslator, QFile

from logic.exceptions import TranslationFileLoadingError
from settings import settings


class RTranslator(QTranslator):
    def __init__(self, parent=None):
        super(RTranslator, self).__init__(parent)
        
        fname = 'radiance_%s.qm' % settings.get('locale')
        fpath = os.path.join(settings.get('i18n_path'), fname)
        f = QFile(fpath)
        if f.exists() and not self.load(f.fileName()):
            raise TranslationFileLoadingError
