# -*- coding: utf-8 -*-


"""
Created on 10.02.2011

@author: vda
"""


from PyQt4 import QtCore, QtGui

from ui.gui.radianceeditlayeredmaterialdialog import Ui_REditLayeredMaterialDialog
from logic.models.tablemodels import LayeredMaterialEditableTableModel
from ui.misc.delegate import DoubleSpinBoxCmDelegate, ComboBoxDelegate
from ui.widgets.deletelayeredmaterialmessagebox import RDeleteLayeredMaterialMessageBox
from logic.registry import LayeredMaterialRegistry, MaterialRegistry
from logic.db import LayeredMaterialDatabase


class REditLayeredMaterialDialog(QtGui.QDialog):
    def __init__(self, layered_material, layered_material_default_title, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_REditLayeredMaterialDialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.layered_material = layered_material
        self.layered_material_default_title = layered_material_default_title
        
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
        
        data = []
        for material_id, thickness in self.layered_material.layers:
            data.append([MaterialRegistry.get_by_id(material_id), thickness])
        
        self.model = LayeredMaterialEditableTableModel(data)
        table.setModel(self.model)
        
        # signals
        self.ui.layeredMaterialTitleLineEdit.textChanged.connect(self._process_form)
        self.ui.layeredMaterialTitleLineEdit.textEdited.connect(self._process_form)
        self.model.dataChanged.connect(self._process_form)
        self.ui.checkBox.clicked.connect(self._process_form)
        
        self.ui.layeredMaterialTitleLineEdit.setText(self.layered_material_default_title)
        
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
            if self.layered_material_default_title != title:
                self.ui.saveButton.setEnabled(False)
                self.ui.errorLabel.setVisible(True)
                self.ui.correctnessErrorLabel.setVisible(True)
            else:
                self.ui.saveButton.setEnabled(True)
                self.ui.errorLabel.setVisible(False)
                self.ui.correctnessErrorLabel.setVisible(False)
                
        else:
            self.ui.errorLabel.setVisible(False)
            
            if self.model.data_is_valid() and title:
                self.ui.saveButton.setEnabled(True)
                self.ui.correctnessErrorLabel.setVisible(False)
                
            else:
                self.ui.saveButton.setEnabled(False)
                self.ui.correctnessErrorLabel.setVisible(True)
                
    @QtCore.pyqtSlot()
    def on_saveButton_clicked(self):
        layers = []
        for material, thickness in self.model.cells:
            if material != self.trUtf8("None"):
                m_id = MaterialRegistry.get(unicode(material)).id
                layers.append([m_id, thickness])
        
        kwargs = {
                  'title': unicode(self.ui.layeredMaterialTitleLineEdit.text()),
                  'data': {
                           'layers': layers,
                           },
                  }
        
        db = LayeredMaterialDatabase()
        db.update(self.layered_material_default_title, **kwargs)
        
        self.parent.reload_comboboxes()
        self.parent.parent.reload_comboboxes()
        
        self.close()
    
    @QtCore.pyqtSlot()
    def on_deleteButton_clicked(self):
        # display confirmation dialog
        messagebox = RDeleteLayeredMaterialMessageBox(self)
        choice = messagebox.exec_()
        
        if choice == messagebox.Yes:
            # deletes nuclide from database, reloads nuclide registry, reloads
            # nuclide comboboxes, closes nuclide edit dialog
            db = LayeredMaterialDatabase()
            db.remove(self.layered_material_default_title)
            
            self.parent.reload_comboboxes()
            self.parent.parent.reload_comboboxes()
            
            self.close()
    