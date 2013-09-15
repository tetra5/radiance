# -*- coding: utf-8 -*-


"""
Created on 29.03.2011

@author: vda
"""


from platform import python_version, system

from PyQt4.QtCore import QT_VERSION_STR, PYQT_VERSION_STR, QString
from PyQt4.QtGui import QMessageBox

class RAboutMessageBox(QMessageBox):
    
    def __init__(self, parent=None):
        super(RAboutMessageBox, self).__init__(parent)
        
        from radiance import __version__
        message = self.trUtf8("""
<b>Radiance %s</b>
<p>&copy; 2010-2011 tetra5.org.
<p><b>Modules used:</b><br>
<a href="http://www.riverbankcomputing.com">PyQt4</a><br>
<a href="http://www.sqlalchemy.org">SQLAlchemy</a><br>
<a href="http://jinja.pocoo.org">Jinja2</a><br>
<a href="http://numpy.scipy.org/">NumPy</a><br>
<a href="http://www.scipy.org/">SciPy</a>
<p><b>Icons by:</b><br>
<a href="http://www.famfamfam.com/">famfamfam</a>
<p>Python %s - Qt %s - PyQt %s on %s
""") 
        message = unicode(message) % (__version__, python_version(), QT_VERSION_STR,
                                      PYQT_VERSION_STR, system())
        
        self.setIcon(QMessageBox.Information)
        self.setText(message)
        self.setWindowTitle(self.tr('About'))
        
        