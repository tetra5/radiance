# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\gui\radianceaddnuclidedialog.ui'
#
# Created: Fri Jul 15 11:15:47 2011
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RAddNuclideDialog(object):
    def setupUi(self, RAddNuclideDialog):
        RAddNuclideDialog.setObjectName("RAddNuclideDialog")
        RAddNuclideDialog.setWindowModality(QtCore.Qt.NonModal)
        RAddNuclideDialog.resize(640, 480)
        RAddNuclideDialog.setMinimumSize(QtCore.QSize(640, 480))
        RAddNuclideDialog.setSizeGripEnabled(True)
        self.verticalLayout_3 = QtGui.QVBoxLayout(RAddNuclideDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.topLayout = QtGui.QHBoxLayout()
        self.topLayout.setObjectName("topLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.elementLabel = QtGui.QLabel(RAddNuclideDialog)
        self.elementLabel.setObjectName("elementLabel")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.elementLabel)
        self.elementComboBox = QtGui.QComboBox(RAddNuclideDialog)
        self.elementComboBox.setEditable(True)
        self.elementComboBox.setMaxVisibleItems(20)
        self.elementComboBox.setInsertPolicy(QtGui.QComboBox.InsertAtBottom)
        self.elementComboBox.setMinimumContentsLength(15)
        self.elementComboBox.setFrame(True)
        self.elementComboBox.setObjectName("elementComboBox")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.elementComboBox)
        self.atomicMassLabel = QtGui.QLabel(RAddNuclideDialog)
        self.atomicMassLabel.setObjectName("atomicMassLabel")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.atomicMassLabel)
        self.atomicMassSpinBox = QtGui.QSpinBox(RAddNuclideDialog)
        self.atomicMassSpinBox.setAccelerated(True)
        self.atomicMassSpinBox.setMinimum(1)
        self.atomicMassSpinBox.setMaximum(999)
        self.atomicMassSpinBox.setProperty("value", 1)
        self.atomicMassSpinBox.setObjectName("atomicMassSpinBox")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.atomicMassSpinBox)
        self.atomicNumberLabel = QtGui.QLabel(RAddNuclideDialog)
        self.atomicNumberLabel.setObjectName("atomicNumberLabel")
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.atomicNumberLabel)
        self.atomicNumberSpinBox = QtGui.QSpinBox(RAddNuclideDialog)
        self.atomicNumberSpinBox.setEnabled(False)
        self.atomicNumberSpinBox.setMaximum(999)
        self.atomicNumberSpinBox.setObjectName("atomicNumberSpinBox")
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.atomicNumberSpinBox)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.errorLabel = QtGui.QLabel(RAddNuclideDialog)
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
        self.topLayout.addLayout(self.verticalLayout)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.topLayout.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.topLayout)
        self.nuclideToolBox = QtGui.QToolBox(RAddNuclideDialog)
        self.nuclideToolBox.setFrameShape(QtGui.QFrame.StyledPanel)
        self.nuclideToolBox.setObjectName("nuclideToolBox")
        self.gammaSpectrumPageWidget = QtGui.QWidget()
        self.gammaSpectrumPageWidget.setGeometry(QtCore.QRect(0, 0, 620, 298))
        self.gammaSpectrumPageWidget.setObjectName("gammaSpectrumPageWidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.gammaSpectrumPageWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gammaSpectrumTableView = QtGui.QTableView(self.gammaSpectrumPageWidget)
        self.gammaSpectrumTableView.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
        self.gammaSpectrumTableView.setTabKeyNavigation(False)
        self.gammaSpectrumTableView.setAlternatingRowColors(True)
        self.gammaSpectrumTableView.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.gammaSpectrumTableView.setCornerButtonEnabled(False)
        self.gammaSpectrumTableView.setObjectName("gammaSpectrumTableView")
        self.verticalLayout_2.addWidget(self.gammaSpectrumTableView)
        self.nuclideToolBox.addItem(self.gammaSpectrumPageWidget, "")
        self.verticalLayout_3.addWidget(self.nuclideToolBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.correctnessErrorLabel = QtGui.QLabel(RAddNuclideDialog)
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
        self.addButton = QtGui.QPushButton(RAddNuclideDialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Radiance/icons/disk.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addButton.setIcon(icon)
        self.addButton.setAutoDefault(False)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout.addWidget(self.addButton)
        self.cancelButton = QtGui.QPushButton(RAddNuclideDialog)
        self.cancelButton.setAutoDefault(False)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(RAddNuclideDialog)
        self.nuclideToolBox.setCurrentIndex(0)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), RAddNuclideDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RAddNuclideDialog)

    def retranslateUi(self, RAddNuclideDialog):
        RAddNuclideDialog.setWindowTitle(QtGui.QApplication.translate("RAddNuclideDialog", "Add nuclide", None, QtGui.QApplication.UnicodeUTF8))
        self.elementLabel.setText(QtGui.QApplication.translate("RAddNuclideDialog", "Element", None, QtGui.QApplication.UnicodeUTF8))
        self.atomicMassLabel.setText(QtGui.QApplication.translate("RAddNuclideDialog", "Atomic mass", None, QtGui.QApplication.UnicodeUTF8))
        self.atomicNumberLabel.setText(QtGui.QApplication.translate("RAddNuclideDialog", "Atomic number", None, QtGui.QApplication.UnicodeUTF8))
        self.errorLabel.setText(QtGui.QApplication.translate("RAddNuclideDialog", "Already exists.", None, QtGui.QApplication.UnicodeUTF8))
        self.nuclideToolBox.setItemText(self.nuclideToolBox.indexOf(self.gammaSpectrumPageWidget), QtGui.QApplication.translate("RAddNuclideDialog", "Gamma spectrum", None, QtGui.QApplication.UnicodeUTF8))
        self.correctnessErrorLabel.setText(QtGui.QApplication.translate("RAddNuclideDialog", "Check the correctness of data input.", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("RAddNuclideDialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("RAddNuclideDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

import radiance_rc
