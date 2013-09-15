# -*- coding: utf-8 -*-


"""
Created on 28.01.2011

@author: vda
"""


from PyQt4 import QtCore, QtGui 


class VerticalLabel(QtGui.QWidget):
    def __init__(self, text, parent=None):
        QtGui.QLabel.__init__(self, parent)
        self.text = text
        
        fm = QtGui.QApplication.fontMetrics()
        self.width = fm.width(self.text)
        self.height = fm.height()
        
#        self.setMinimumSize(QtCore.QSize(100, 100))
#        self.setMaximumSize(QtCore.QSize(100, 100))
#        self.setGeometry(0, 0, 100, 100)
        
        self.setMinimumSize(QtCore.QSize(self.width, self.height))
        self.setMaximumSize(QtCore.QSize(self.width, self.height))
        self.setGeometry(0, 0, self.width, self.height)
#        self.update()
        
    def paintEvent(self, event):
        fm = QtGui.QApplication.fontMetrics()
        painter = QtGui.QPainter()
        painter.begin(self)
        
        painter.setBrush(QtGui.QBrush(QtGui.QColor('#CCCCCC')))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(0, 0, fm.height(), fm.width(self.text))
        #painter.drawRect(0, 0, 100, 100)
        
        
        painter.setPen(QtCore.Qt.black)
#        painter.translate(20, 100)
        painter.rotate(-90)
        painter.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)
        painter.end()
        

        