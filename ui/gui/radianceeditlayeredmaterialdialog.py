# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\gui\radianceeditlayeredmaterialdialog.ui'
#
# Created: Fri Jul 15 11:15:47 2011
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_REditLayeredMaterialDialog(object):
    def setupUi(self, REditLayeredMaterialDialog):
        REditLayeredMaterialDialog.setObjectName("REditLayeredMaterialDialog")
        REditLayeredMaterialDialog.setWindowModality(QtCore.Qt.NonModal)
        REditLayeredMaterialDialog.resize(640, 480)
        REditLayeredMaterialDialog.setMinimumSize(QtCore.QSize(640, 480))
        REditLayeredMaterialDialog.setSizeGripEnabled(True)
        self.verticalLayout_3 = QtGui.QVBoxLayout(REditLayeredMaterialDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self._titleLabel = QtGui.QLabel(REditLayeredMaterialDialog)
        self._titleLabel.setObjectName("_titleLabel")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self._titleLabel)
        self.layeredMaterialTitleLineEdit = QtGui.QLineEdit(REditLayeredMaterialDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layeredMaterialTitleLineEdit.sizePolicy().hasHeightForWidth())
        self.layeredMaterialTitleLineEdit.setSizePolicy(sizePolicy)
        self.layeredMaterialTitleLineEdit.setMaxLength(512)
        self.layeredMaterialTitleLineEdit.setObjectName("layeredMaterialTitleLineEdit")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.layeredMaterialTitleLineEdit)
        self.checkBox = QtGui.QCheckBox(REditLayeredMaterialDialog)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.checkBox)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.errorLabel = QtGui.QLabel(REditLayeredMaterialDialog)
        self.errorLabel.setEnabled(True)
        self.errorLabel.setStyleSheet("QLabel {\n"
"    background: url(:/Radiance/icons/error.png);\n"
"    background-position: center left;\n"
"    background-repeat: no-repeat;\n"
"    padding-left: 20px;\n"
"}")
        self.errorLabel.setFrameShape(QtGui.QFrame.NoFrame)
        self.errorLabel.setObjectName("errorLabel")
        self.verticalLayout.addWidget(self.errorLabel)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.deleteButton = QtGui.QPushButton(REditLayeredMaterialDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deleteButton.sizePolicy().hasHeightForWidth())
        self.deleteButton.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Radiance/icons/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(icon)
        self.deleteButton.setAutoDefault(False)
        self.deleteButton.setObjectName("deleteButton")
        self.horizontalLayout_2.addWidget(self.deleteButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.layeredMaterialToolBox = QtGui.QToolBox(REditLayeredMaterialDialog)
        self.layeredMaterialToolBox.setFrameShape(QtGui.QFrame.StyledPanel)
        self.layeredMaterialToolBox.setObjectName("layeredMaterialToolBox")
        self.gammaSpectrumPageWidget = QtGui.QWidget()
        self.gammaSpectrumPageWidget.setGeometry(QtCore.QRect(0, 0, 620, 327))
        self.gammaSpectrumPageWidget.setObjectName("gammaSpectrumPageWidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.gammaSpectrumPageWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.layeredMaterialTableView = QtGui.QTableView(self.gammaSpectrumPageWidget)
        self.layeredMaterialTableView.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
        self.layeredMaterialTableView.setTabKeyNavigation(False)
        self.layeredMaterialTableView.setAlternatingRowColors(True)
        self.layeredMaterialTableView.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.layeredMaterialTableView.setCornerButtonEnabled(False)
        self.layeredMaterialTableView.setObjectName("layeredMaterialTableView")
        self.verticalLayout_2.addWidget(self.layeredMaterialTableView)
        self.layeredMaterialToolBox.addItem(self.gammaSpectrumPageWidget, "")
        self.verticalLayout_3.addWidget(self.layeredMaterialToolBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.correctnessErrorLabel = QtGui.QLabel(REditLayeredMaterialDialog)
        self.correctnessErrorLabel.setEnabled(True)
        self.correctnessErrorLabel.setStyleSheet("QLabel {\n"
"    background: url(:/Radiance/icons/error.png);\n"
"    background-position: center left;\n"
"    background-repeat: no-repeat;\n"
"    padding-left: 20px;\n"
"}")
        self.correctnessErrorLabel.setFrameShape(QtGui.QFrame.NoFrame)
        self.correctnessErrorLabel.setObjectName("correctnessErrorLabel")
        self.horizontalLayout.addWidget(self.correctnessErrorLabel)
        self.saveButton = QtGui.QPushButton(REditLayeredMaterialDialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Radiance/icons/disk.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveButton.setIcon(icon1)
        self.saveButton.setAutoDefault(False)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.cancelButton = QtGui.QPushButton(REditLayeredMaterialDialog)
        self.cancelButton.setAutoDefault(False)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(REditLayeredMaterialDialog)
        self.layeredMaterialToolBox.setCurrentIndex(0)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), REditLayeredMaterialDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(REditLayeredMaterialDialog)

    def retranslateUi(self, REditLayeredMaterialDialog):
        REditLayeredMaterialDialog.setWindowTitle(QtGui.QApplication.translate("REditLayeredMaterialDialog", "Edit layered material", None, QtGui.QApplication.UnicodeUTF8))
        self._titleLabel.setText(QtGui.QApplication.translate("REditLayeredMaterialDialog", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("REditLayeredMaterialDialog", "Generate title automatically", None, QtGui.QApplication.UnicodeUTF8))
        self.errorLabel.setText(QtGui.QApplication.translate("REditLayeredMaterialDialog", "Already exists.", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("REditLayeredMaterialDialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.layeredMaterialToolBox.setItemText(self.layeredMaterialToolBox.indexOf(self.gammaSpectrumPageWidget), QtGui.QApplication.translate("REditLayeredMaterialDialog", "Layers", None, QtGui.QApplication.UnicodeUTF8))
        self.correctnessErrorLabel.setText(QtGui.QApplication.translate("REditLayeredMaterialDialog", "Check the correctness of data input.", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("REditLayeredMaterialDialog", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("REditLayeredMaterialDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

import radiance_rc
