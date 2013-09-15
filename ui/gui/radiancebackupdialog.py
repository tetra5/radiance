# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\gui\radiancebackupdialog.ui'
#
# Created: Fri Jul 15 11:15:47 2011
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RBackupDialog(object):
    def setupUi(self, RBackupDialog):
        RBackupDialog.setObjectName("RBackupDialog")
        RBackupDialog.resize(256, 192)
        RBackupDialog.setMinimumSize(QtCore.QSize(256, 192))
        RBackupDialog.setMaximumSize(QtCore.QSize(256, 192))
        self.verticalLayout_3 = QtGui.QVBoxLayout(RBackupDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtGui.QGroupBox(RBackupDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainDatabaseCheckBox = QtGui.QCheckBox(self.groupBox)
        self.mainDatabaseCheckBox.setChecked(True)
        self.mainDatabaseCheckBox.setObjectName("mainDatabaseCheckBox")
        self.verticalLayout.addWidget(self.mainDatabaseCheckBox)
        self.reportDatabaseCheckBox = QtGui.QCheckBox(self.groupBox)
        self.reportDatabaseCheckBox.setChecked(True)
        self.reportDatabaseCheckBox.setObjectName("reportDatabaseCheckBox")
        self.verticalLayout.addWidget(self.reportDatabaseCheckBox)
        self.templateFilesCheckBox = QtGui.QCheckBox(self.groupBox)
        self.templateFilesCheckBox.setChecked(True)
        self.templateFilesCheckBox.setObjectName("templateFilesCheckBox")
        self.verticalLayout.addWidget(self.templateFilesCheckBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.saveButton = QtGui.QPushButton(RBackupDialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Radiance/icons/compress.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveButton.setIcon(icon)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.cancelButton = QtGui.QPushButton(RBackupDialog)
        self.cancelButton.setDefault(True)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(RBackupDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), RBackupDialog.close)
        QtCore.QMetaObject.connectSlotsByName(RBackupDialog)

    def retranslateUi(self, RBackupDialog):
        RBackupDialog.setWindowTitle(QtGui.QApplication.translate("RBackupDialog", "Backup", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("RBackupDialog", "Data source", None, QtGui.QApplication.UnicodeUTF8))
        self.mainDatabaseCheckBox.setText(QtGui.QApplication.translate("RBackupDialog", "Main database", None, QtGui.QApplication.UnicodeUTF8))
        self.reportDatabaseCheckBox.setText(QtGui.QApplication.translate("RBackupDialog", "Reports database", None, QtGui.QApplication.UnicodeUTF8))
        self.templateFilesCheckBox.setText(QtGui.QApplication.translate("RBackupDialog", "Report templates", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("RBackupDialog", "Save...", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("RBackupDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

import radiance_rc
