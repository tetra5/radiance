# -*- coding: utf-8 -*-


"""
Created on 13.10.2010

@author: vda
"""


from PyQt4 import QtCore, QtGui


class NuclideDisplayWidget(QtGui.QWidget):
    def __init__(self, parent=None, bg="#EFEFEF", fg="#000000"):
        QtGui.QWidget.__init__(self, parent)
        self.setMinimumSize(QtCore.QSize(100, 100))
        self.setMaximumSize(QtCore.QSize(100, 100))
        self.setGeometry(0, 0, 100, 100)
        
        self.bg_color = bg
        self.fg_color = fg
        
        self.set_data()
        
    def set_data(self, nuclide=None):
        """
        Redraws widget using specified values.
        
        @param nuclide: object with predefined properties, i.e:
            class MyNuclide(object):
                def __init__(self):
                    self.lat = 'Pb' #shortened latin name, stands for Plumbum
                    self.a_mass = '999' #atomic mass
                    self.a_num = '82' #atomic number
            
            widget = NuclideDisplayWidget()
            widget.set_data(MyNuclide)
            
            OR simplier version:
            
            class MyNuclide: pass
            nuclide = MyNuclide()
            nuclide.lat, nuclide.a_mass, nuclide.a_num = 'Pb', '999', '82'
            widget = NuclideDisplayWidget()
            widget.set_data(nuclide)
        """
        if nuclide:
            self.lat = nuclide.lat
            self.a_mass = nuclide.a_mass
            self.a_num = nuclide.a_num
        else:
            self.lat = None
            self.a_mass = None
            self.a_num = None
        self.update()
        
    def reset(self):
        self.lat = None
        self.a_mass = None
        self.a_num = None
        self.update()
        
    def paintEvent(self, event):
        lat = '?' if not self.lat else self.lat
        a_mass = '?' if not self.a_mass else self.a_mass
        a_num = '?' if not self.a_num else self.a_num
        
        painter = QtGui.QPainter()
        painter.begin(self)
        
        painter.setBrush(QtGui.QBrush(QtGui.QColor(self.bg_color)))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(0, 0, 100, 100)
        
        #painter.setPen(QtCore.Qt.black)
        painter.setPen(QtGui.QPen(QtGui.QColor(self.fg_color)))
        
        big_font = QtGui.QFont('Helvetica', 25, QtGui.QFont.DemiBold)
        big_font.setStyleHint(QtGui.QFont.Helvetica)
        big_font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        painter.setFont(big_font) 
        painter.drawText(event.rect(), QtCore.Qt.AlignCenter, lat)
        
        small_font = QtGui.QFont('Helvetica', 12, QtGui.QFont.Light)
        small_font.setStyleHint(QtGui.QFont.Helvetica)
        small_font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        painter.setFont(small_font)
        
        fm = QtGui.QFontMetricsF(small_font)
        
        point = QtCore.QPointF(6, fm.ascent() + 3)
        painter.drawText(point, str(a_mass))
        
        point = QtCore.QPointF(6, self.height() - fm.ascent() / 2)
        painter.drawText(point, str(a_num))
        
        painter.end()
        
