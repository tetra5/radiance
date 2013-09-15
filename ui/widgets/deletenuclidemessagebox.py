# -*- coding: utf-8 -*-


"""
Created on 01.11.2010

@author: vda
"""


from PyQt4 import QtGui


class RDeleteNuclideMessageBox(QtGui.QMessageBox):
    
    def __init__(self, parent):
        QtGui.QMessageBox.__init__(self, parent)
        
        self.setText(self.tr('Are you sure you want to delete this nuclide?'))
        self.setStandardButtons(self.Yes | self.Cancel)
        self.setDefaultButton(QtGui.QMessageBox.Cancel)
        self.setIcon(QtGui.QMessageBox.Warning)
        self.setWindowTitle(self.tr('Delete nuclide'))
        self.setButtonText(self.Yes, self.tr('Yes'))
        self.setButtonText(self.Cancel, self.tr('Cancel'))
               
    