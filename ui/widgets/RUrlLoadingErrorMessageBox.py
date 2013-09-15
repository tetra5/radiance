# -*- coding: utf-8 -*-


"""
Created on 31.03.2011

@author: vda
"""


from PyQt4.QtGui import QMessageBox


class RUrlLoadingErrorMessageBox(QMessageBox):
    def __init__(self, parent=None):
        super(RUrlLoadingErrorMessageBox, self).__init__(parent)
        
        message = self.trUtf8(""":(""")
        
        self.setIcon(QMessageBox.Critical)
        self.setText(message)
        self.setWindowTitle(self.tr('Error'))