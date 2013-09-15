# -*- coding: utf-8 -*-


"""
Created on 13.10.2010

@author: vda
"""


from PyQt4 import QtCore, QtGui


class DoubleSpinBoxDelegate(QtGui.QItemDelegate):
    """
    Overrides default implementation of editable double spin box inside of
    table view for more convenient usage.
    """
    
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
        
    def createEditor(self, parent, option, index):
        editor = QtGui.QDoubleSpinBox(parent)
        editor.setDecimals(4)
        editor.setSingleStep(0.01)
        editor.setMaximum(9999.9999)
        return editor


class DoubleSpinBoxMmDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.suffix = self.trUtf8(" mm")
        
    def createEditor(self, parent, option, index):
        editor = QtGui.QDoubleSpinBox(parent)
        editor.setMinimum(0.01)
        editor.setDecimals(2)
        editor.setSingleStep(1.00)
        editor.setMaximum(9999.99)
        editor.setSuffix(self.suffix)
        return editor
    
    
class DoubleSpinBoxCmDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.suffix = self.trUtf8(" cm")
        
    def createEditor(self, parent, option, index):
        editor = QtGui.QDoubleSpinBox(parent)
        editor.setMinimum(0.01)
        editor.setDecimals(2)
        editor.setSingleStep(1.00)
        editor.setMaximum(99999.99)
        editor.setSuffix(self.suffix)
        return editor


class IntegerSpinBoxDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
        
    def createEditor(self, parent, option, index):
        editor = QtGui.QSpinBox(parent)
        return editor
    
    
class ComboBoxDelegate(QtGui.QItemDelegate):
    def __init__(self, items, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.items = items
        
    def createEditor(self, parent, option, index):
        editor = QtGui.QComboBox(parent)
        editor.insertItems(0, self.items)
        return editor
    
    def setEditorData(self, combobox, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole).toString()
        idx = combobox.findText(unicode(value))
        combobox.setCurrentIndex(idx)

    def setModelData(self, editor, model, index):
        value = editor.currentIndex()
        model.setData(index, editor.itemData(value, QtCore.Qt.DisplayRole))

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
        
