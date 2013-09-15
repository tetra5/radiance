# -*- coding: utf-8 -*-


"""
Created on 28.02.2011

@author: vda
"""


import os

from PyQt4.QtCore import Qt, QUrl
from PyQt4.QtGui import QDialog
from PyQt4.QtWebKit import QWebPage

from ui.gui.radiancehelpviewerdialog import Ui_RHelpViewerDialog
from settings import settings
from ui.widgets.RUrlLoadingErrorMessageBox import RUrlLoadingErrorMessageBox


class RHelpViewerDialog(QDialog):
    def __init__(self, parent=None):
        super(RHelpViewerDialog, self).__init__(parent)
        self.ui = Ui_RHelpViewerDialog()
        self.ui.setupUi(self)
        self.parent = parent
        
        self.__init()
        
    def __init(self):
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        # Window flags
        self.setWindowFlags(Qt.Dialog | Qt.WindowMaximizeButtonHint)
        
        # Signals
        self.ui.webView.linkClicked.connect(self.load_url)
        
        # QWebView settings
        self.ui.webView.setContextMenuPolicy(Qt.NoContextMenu)
        self.ui.webView.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        
        self.load_url(QUrl('/'.join((settings.get('help_path'), 'index.html'))))
        
    def load_url(self, url):
        basename = os.path.basename(unicode(url.toString()))
        path = os.path.join(settings.get('help_path'), basename)

        if not os.path.exists(path):
            messagebox = RUrlLoadingErrorMessageBox(self)
            messagebox.exec_()
        else:
            if not url.scheme() in ['http', 'ftp']:
                url = QUrl(os.path.abspath(os.path.join(settings.get('help_path'), basename)).replace('\\', '/'))
                url.setScheme('file')
                self.ui.webView.load(url)
            else:
                messagebox = RUrlLoadingErrorMessageBox(self)
                messagebox.exec_()
                
