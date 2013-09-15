# -*- coding: utf-8 -*-


"""
Created on 03.02.2011

@author: vda
"""


from PyQt4 import QtCore, QtGui


from ui.gui.radianceaddlayeredmaterialdialog import Ui_RAddLayeredMaterialDialog
from logic.models.tablemodels import LayeredMaterialEditableTableModel
from ui.misc.delegate import ComboBoxDelegate, DoubleSpinBoxCmDelegate
from logic.registry import MaterialRegistry, LayeredMaterialRegistry
from logic.db import LayeredMaterialDatabase


class RAddLayeredMaterialDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_RAddLayeredMaterialDialog()
        self.ui.setupUi(self)
        self.parent = parent
        
        self.__init()
        
    def __init(self):
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowMaximizeButtonHint)
        
        table = self.ui.layeredMaterialTableView
        table.horizontalHeader().setResizeMode(1)
        delegate_items = [self.trUtf8("None")] + MaterialRegistry.keys()
        delegate = DoubleSpinBoxCmDelegate(table)
        self.suffix = delegate.suffix
        table.setItemDelegate(ComboBoxDelegate(delegate_items))
        table.setItemDelegateForColumn(1, delegate)
        self.model = LayeredMaterialEditableTableModel()
        table.setModel(self.model)
        
        # signals
        self.model.dataChanged.connect(self._process_form)
        self.ui.layeredMaterialTitleLineEdit.textChanged.connect(self._process_form)
        self.ui.layeredMaterialTitleLineEdit.textEdited.connect(self._process_form)
        self.ui.checkBox.clicked.connect(self._process_form)
        
        self._process_form()
        
    def _process_form(self):
        title = ''
        layers = []
        total_thickness = 0.0
        for material, thickness in self.model.cells:
            if material != self.trUtf8("None"):
                total_thickness = total_thickness + thickness
                layers.append('%s %.2f%s' % (unicode(material), thickness, unicode(self.suffix)))
        
        if self.ui.checkBox.isChecked():
            if layers:
                title = '%s (%.2f%s)' % ('; '.join(layers), total_thickness, unicode(self.suffix))
            self.ui.layeredMaterialTitleLineEdit.setText(title)
        else:
            title = unicode(self.ui.layeredMaterialTitleLineEdit.text())
        
        if LayeredMaterialRegistry.has_key(title):
            self.ui.errorLabel.setVisible(True)
            self.ui.addButton.setEnabled(False)
            self.ui.correctnessErrorLabel.setVisible(True)
        else:
            self.ui.errorLabel.setVisible(False)
            
            if self.model.data_is_valid() and title:
                self.ui.addButton.setEnabled(True)
                self.ui.correctnessErrorLabel.setVisible(False)
                
            else:
                self.ui.addButton.setEnabled(False)
                self.ui.correctnessErrorLabel.setVisible(True)
    
    @QtCore.pyqtSlot()
    def on_addButton_clicked(self):
        layers = []
        for material, thickness in self.model.cells:
            if material != self.trUtf8("None"):
                m_id = MaterialRegistry.get(unicode(material)).id
                layers.append([m_id, thickness])
        
        data = {
                'layers': layers,
                }
        
        title = self.ui.layeredMaterialTitleLineEdit.text()
        
        db = LayeredMaterialDatabase()
        db.add(title, data)
        
        self.parent.reload_comboboxes()
        self.parent.parent.reload_comboboxes()
        
        self.close()
        
    