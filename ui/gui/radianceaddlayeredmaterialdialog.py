# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\gui\radianceaddlayeredmaterialdialog.ui'
#
# Created: Fri Jul 15 11:15:47 2011
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RAddLayeredMaterialDialog(object):
    def setupUi(self, RAddLayeredMaterialDialog):
        RAddLayeredMaterialDialog.setObjectName("RAddLayeredMaterialDialog")
        RAddLayeredMaterialDialog.setWindowModality(QtCore.Qt.NonModal)
        RAddLayeredMaterialDialog.resize(640, 480)
        RAddLayeredMaterialDialog.setMinimumSize(QtCore.QSize(640, 480))
        RAddLayeredMaterialDialog.setSizeGripEnabled(True)
        self.verticalLayout_3 = QtGui.QVBoxLayout(RAddLayeredMaterialDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.titleLabel = QtGui.QLabel(RAddLayeredMaterialDialog)
        self.titleLabel.setObjectName("titleLabel")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.titleLabel)
        self.layeredMaterialTitleLineEdit = QtGui.QLineEdit(RAddLayeredMaterialDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layeredMaterialTitleLineEdit.sizePolicy().hasHeightForWidth())
        self.layeredMaterialTitleLineEdit.setSizePolicy(sizePolicy)
        self.layeredMaterialTitleLineEdit.setMaxLength(512)
        self.layeredMaterialTitleLineEdit.setObjectName("layeredMaterialTitleLineEdit")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.layeredMaterialTitleLineEdit)
        self.checkBox = QtGui.QCheckBox(RAddLayeredMaterialDialog)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.checkBox)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.errorLabel = QtGui.QLabel(RAddLayeredMaterialDialog)
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
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.layeredMaterialToolBox = QtGui.QToolBox(RAddLayeredMaterialDialog)
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
        self.correctnessErrorLabel = QtGui.QLabel(RAddLayeredMaterialDialog)
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
        self.addButton = QtGui.QPushButton(RAddLayeredMaterialDialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Radiance/icons/disk.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addButton.setIcon(icon)
        self.addButton.setAutoDefault(False)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout.addWidget(self.addButton)
        self.cancelButton = QtGui.QPushButton(RAddLayeredMaterialDialog)
        self.cancelButton.setAutoDefault(False)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(RAddLayeredMaterialDialog)
        self.layeredMaterialToolBox.setCurrentIndex(0)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), RAddLayeredMaterialDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RAddLayeredMaterialDialog)

    def retranslateUi(self, RAddLayeredMaterialDialog):
        RAddLayeredMaterialDialog.setWindowTitle(QtGui.QApplication.translate("RAddLayeredMaterialDialog", "Add layered material", None, QtGui.QApplication.UnicodeUTF8))
        self.titleLabel.setText(QtGui.QApplication.translate("RAddLayeredMaterialDialog", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("RAddLayeredMaterialDialog", "Generate title automatically", None, QtGui.QApplication.UnicodeUTF8))
        self.errorLabel.setText(QtGui.QApplication.translate("RAddLayeredMaterialDialog", "Already exists.", None, QtGui.QApplication.UnicodeUTF8))
        self.layeredMaterialToolBox.setItemText(self.layeredMaterialToolBox.indexOf(self.gammaSpectrumPageWidget), QtGui.QApplication.translate("RAddLayeredMaterialDialog", "Layers", None, QtGui.QApplication.UnicodeUTF8))
        self.correctnessErrorLabel.setText(QtGui.QApplication.translate("RAddLayeredMaterialDialog", "Check the correctness of data input.", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("RAddLayeredMaterialDialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("RAddLayeredMaterialDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

import radiance_rc
