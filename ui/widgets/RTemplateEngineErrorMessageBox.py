# -*- coding: utf-8 -*-


"""
Created on 01.04.2011

@author: vda
"""


from PyQt4.QtGui import QMessageBox


class RTemplateEngineErrorMessageBox(QMessageBox):
    def __init__(self, parent=None, msg=None):
        super(RTemplateEngineErrorMessageBox, self).__init__(parent)
        
        self.setIcon(QMessageBox.Critical)
        self.setText(msg)
        self.setWindowTitle(self.tr('Template engine error'))