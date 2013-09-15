# -*- coding: utf-8 -*-


"""
Created on 14.10.2010

@author: vda
"""


from PyQt4.QtCore import QLocale


settings = {
            'locale': QLocale().name(),
            'template_path': './templates',
            'i18n_path': './i18n',
            'help_path': './help',
            }


SL_SCREEN_OK, SL_SCREEN_ERR, ML_SCREEN_OK, ML_SCREEN_ERR = range(4)


TEMPLATE_TYPES = {
                  SL_SCREEN_OK: 'sl-success.html',
                  SL_SCREEN_ERR: 'sl-error.html',
                  ML_SCREEN_OK: 'ml-success.html',
                  ML_SCREEN_ERR: 'ml-error.html',
                  }

