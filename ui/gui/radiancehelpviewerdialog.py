# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\gui\radiancehelpviewerdialog.ui'
#
# Created: Fri Jul 15 11:15:47 2011
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RHelpViewerDialog(object):
    def setupUi(self, RHelpViewerDialog):
        RHelpViewerDialog.setObjectName("RHelpViewerDialog")
        RHelpViewerDialog.setWindowModality(QtCore.Qt.NonModal)
        RHelpViewerDialog.resize(800, 600)
        RHelpViewerDialog.setMinimumSize(QtCore.QSize(640, 480))
        RHelpViewerDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtGui.QVBoxLayout(RHelpViewerDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.webView = QtWebKit.QWebView(RHelpViewerDialog)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setRenderHints(QtGui.QPainter.TextAntialiasing)
        self.webView.setObjectName("webView")
        self.verticalLayout.addWidget(self.webView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.closeButton = QtGui.QPushButton(RHelpViewerDialog)
        self.closeButton.setDefault(True)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(RHelpViewerDialog)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL("clicked()"), RHelpViewerDialog.close)
        QtCore.QMetaObject.connectSlotsByName(RHelpViewerDialog)

    def retranslateUi(self, RHelpViewerDialog):
        RHelpViewerDialog.setWindowTitle(QtGui.QApplication.translate("RHelpViewerDialog", "Help viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("RHelpViewerDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
import radiance_rc
