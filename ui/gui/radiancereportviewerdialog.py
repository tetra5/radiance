# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\gui\radiancereportviewerdialog.ui'
#
# Created: Fri Jul 15 11:15:47 2011
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RReportViewerDialog(object):
    def setupUi(self, RReportViewerDialog):
        RReportViewerDialog.setObjectName("RReportViewerDialog")
        RReportViewerDialog.resize(800, 480)
        RReportViewerDialog.setMinimumSize(QtCore.QSize(800, 480))
        RReportViewerDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtGui.QVBoxLayout(RReportViewerDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtGui.QSplitter(RReportViewerDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(10)
        self.splitter.setChildrenCollapsible(True)
        self.splitter.setObjectName("splitter")
        self.tableView = QtGui.QTableView(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setMinimumSize(QtCore.QSize(0, 0))
        self.tableView.setMaximumSize(QtCore.QSize(170, 16777215))
        self.tableView.setProperty("cursor", QtCore.Qt.PointingHandCursor)
        self.tableView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView.setDragDropOverwriteMode(False)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView.setGridStyle(QtCore.Qt.NoPen)
        self.tableView.setSortingEnabled(True)
        self.tableView.setWordWrap(False)
        self.tableView.setCornerButtonEnabled(False)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setVisible(False)
        self.tableView.horizontalHeader().setDefaultSectionSize(135)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.verticalHeader().setStretchLastSection(False)
        self.webView = QtWebKit.QWebView(self.splitter)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setRenderHints(QtGui.QPainter.TextAntialiasing)
        self.webView.setObjectName("webView")
        self.verticalLayout.addWidget(self.splitter)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.saveButton = QtGui.QPushButton(RReportViewerDialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Radiance/icons/page_save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveButton.setIcon(icon)
        self.saveButton.setAutoDefault(False)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.closeButton = QtGui.QPushButton(RReportViewerDialog)
        self.closeButton.setDefault(True)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(RReportViewerDialog)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL("clicked()"), RReportViewerDialog.close)
        QtCore.QMetaObject.connectSlotsByName(RReportViewerDialog)

    def retranslateUi(self, RReportViewerDialog):
        RReportViewerDialog.setWindowTitle(QtGui.QApplication.translate("RReportViewerDialog", "Report viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("RReportViewerDialog", "Save...", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("RReportViewerDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
import radiance_rc
