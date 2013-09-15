# -*- coding: utf-8 -*-


"""
Created on 13.10.2010

@author: vda
"""


from PyQt4.QtCore import Qt, QString, SIGNAL
from PyQt4.QtGui import QSplashScreen, QPixmap, QPainter, QFont, QColor, \
    QApplication, QProgressBar, QPen, QCursor
    

class RSplashScreen(QSplashScreen):
    def __init__(self, parent=None):
        from radiance import __version__
        self.__version = __version__
        self.parent = parent
        
        pixmap = QPixmap(QString(':/Radiance/splashscreen.png'))
        flags = Qt.WindowStaysOnTopHint
        QSplashScreen.__init__(self, pixmap, flags)
        self.setMask(pixmap.mask())
        
        # Custom progress bar stylesheet
        progressbar_stylesheet = """
        QProgressBar:horizontal {
            border: 1px solid black;
            background: white;
            padding: 1px;
        }
        QProgressBar::chunk:horizontal {
            background-color: qlineargradient(spread: pad, x1: 1, y1: 0.5, x2: 0, y2: 0.5, stop: 0 black, stop: 1 white);
        }
        """
        
        # Place progress bar to bottom of splash screen.
        progressbar = QProgressBar(self)
        progressbar.setRange(0, 0)
        progressbar.setGeometry(10, self.height() - 20, self.width() - 20, 10)
        progressbar.setTextVisible(False)
        progressbar.setStyleSheet(progressbar_stylesheet)
        self.progressbar = progressbar

        self.show()
        
#    def paintEvent(self, event):
#        title = 'Radiance %s' % self.__version
#        
#        painter = QPainter()
#        painter.begin(self)
#        
#        #painter.setPen(QtCore.Qt.black)
#        painter.setPen(QPen(QColor(Qt.white)))
#        
#        big_font = QFont('Helvetica', 35, QFont.DemiBold)
#        big_font.setStyleHint(QFont.Helvetica)
#        big_font.setStyleStrategy(QFont.PreferAntialias)
#        painter.setFont(big_font) 
#        painter.drawText(event.rect(), Qt.AlignCenter, title)
#        
#        painter.end()
        

class RTSplashScreen(RSplashScreen):
    """
    Loads data in a separate thread, so that loading progress bar indicator
    won't be freezing.
    """
    
    def __init__(self, thread, parent=None):
        RSplashScreen.__init__(self, parent)
        
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        
        self.thread = thread
        
        self.connect(self.thread, SIGNAL("terminated"),
                     self.terminate)
        self.connect(self.thread, SIGNAL("finished()"),
                     self.close_splash_show_parent)
        self.connect(self.thread, SIGNAL("set_message"),
                     self.set_message)
        self.thread.start()
    
    def terminate(self, message):
        QApplication.restoreOverrideCursor()
        raise SystemExit, message
        
    def close_splash_show_parent(self):
        QApplication.restoreOverrideCursor()
        self.finish(self.parent)
        self.parent.show()
        
    def set_message(self, message):
        self.showMessage("Loading '%s' ..." % message, color=QColor('#FFFFFF'))
        