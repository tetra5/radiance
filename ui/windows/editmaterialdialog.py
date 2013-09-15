# -*- coding: utf-8 -*-


"""
Created on 18.01.2011

@author: vda
"""


from PyQt4 import QtCore, QtGui

from ui.gui.radianceeditmaterialdialog import Ui_REditMaterialDialog
from ui.widgets.deletematerialmessagebox import RDeleteMaterialMessageBox
from logic.models.tablemodels import MuDEditableTableModel, \
    EEditableTableModel, DoseBuildUpFactorEditableTableModel, \
    MassAttenuationCoefficientEditableTableModel
from ui.misc.delegate import DoubleSpinBoxDelegate, IntegerSpinBoxDelegate
from logic.registry import MaterialRegistry
from logic.db import MaterialDatabase
from logic.misc.functions import transpose


class REditMaterialDialog(QtGui.QDialog):
    
    def __init__(self, material, material_original_name, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_REditMaterialDialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.material = material
        self.material_original_name = material_original_name
        
        self.__init()
        
    def __init(self):
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowMaximizeButtonHint)
        
        # models
        self.mu_d_model = MuDEditableTableModel([self.material.mu_d])
        self.e_model = EEditableTableModel([[v] for v in self.material.e])
        
        mass_atten_coeff = transpose([list(self.material.mass_atten_coeff_x), list(self.material.mass_atten_coeff_y)])
        mass_atten_coeff = [list(v) for v in mass_atten_coeff]
        self.mass_atten_coeff_model = MassAttenuationCoefficientEditableTableModel(mass_atten_coeff)
        
        h_header = self.mu_d_model.cells[0][:-1]
        v_header = ['%.4f' % v[0] for v in self.e_model.cells[:-1]]
        self.dose_buildup_model = DoseBuildUpFactorEditableTableModel(self.material.b, v_header, h_header)
        
        # mu_d table view & model
        table = self.ui.materialMuDTableView
        table.horizontalHeader().setResizeMode(1)
        table.setItemDelegate(IntegerSpinBoxDelegate())
        table.setModel(self.mu_d_model)
        
        # e table view & model
        table = self.ui.materialETableView
        table.horizontalHeader().setResizeMode(1)
        table.setItemDelegate(DoubleSpinBoxDelegate())
        table.setModel(self.e_model)
        
        # dose buildup table view and model
        table = self.ui.materialDoseBuildupFactorTableView
        table.horizontalHeader().setResizeMode(1)
        table.setItemDelegate(DoubleSpinBoxDelegate())
        table.setModel(self.dose_buildup_model)
    
        # mass attenuation coefficient table view and model
        table = self.ui.materialMassAttenuationCoefficientTableView
        table.horizontalHeader().setResizeMode(1)
        table.setItemDelegate(DoubleSpinBoxDelegate())
        table.setModel(self.mass_atten_coeff_model)
        
        # signals
        self.mu_d_model.dataChanged.connect(self._rebuild_dose_buildup_table)
        self.e_model.dataChanged.connect(self._rebuild_dose_buildup_table)
        self.mass_atten_coeff_model.dataChanged.connect(self._process_form)
        self.ui.materialTitleLineEdit.textChanged.connect(self._process_form)
        self.ui.materialTitleLineEdit.textEdited.connect(self._process_form)
        self.ui.materialDensityDoubleSpinBox.valueChanged.connect(self._process_form)
        self.ui.materialDensityDoubleSpinBox.editingFinished.connect(self._process_form)
        
        self.ui.materialTitleLineEdit.setText(self.material_original_name)
        self.ui.materialDensityDoubleSpinBox.setValue(self.material.density)
        
    def _rebuild_dose_buildup_table(self):
        table = self.ui.materialDoseBuildupFactorTableView
        table.horizontalHeader().setVisible(True)
        table.verticalHeader().setVisible(True)
        
        h_header = self.mu_d_model.cells[0][:-1]
        v_header = ['%.4f' % v[0] for v in self.e_model.cells[:-1]]
        empty_cells = [[0 for _ in h_header] for _ in v_header]
        
        self.dose_buildup_model = DoseBuildUpFactorEditableTableModel(empty_cells, v_header, h_header)
        self.ui.materialDoseBuildupFactorTableView.setModel(self.dose_buildup_model)
        self.dose_buildup_model.dataChanged.connect(self._process_form)
        self.ui.saveButton.setEnabled(False)        

    def _process_form(self):
        density = self.ui.materialDensityDoubleSpinBox.value()
        material_name = unicode(self.ui.materialTitleLineEdit.text())
        
        if self.material_original_name != material_name:
            label_text = (' ' * 3).join((
                                         self.material_original_name,
                                         u'\u2192', # unicode right arrow symbol
                                         material_name,
                                         ))
            self.ui.materialNameLabel.setText(label_text)
        else:
            self.ui.materialNameLabel.setText(' ')
            
        if self.material.density != density:
            label_text = (' ' * 3).join((
                                         str('%.2f' % self.material.density),
                                         u'\u2192', # unicode right arrow symbol
                                         str('%.2f' % density),
                                         ))
            self.ui.materialDensityLabel.setText(label_text)
        else:
            self.ui.materialDensityLabel.setText(' ')
            
        #self.ui.materialTitleLineEdit.setText(material_name.capitalize())
        
        if not MaterialRegistry.has_key(material_name) \
        and material_name != '' \
        and self.mu_d_model.data_is_valid() \
        and self.e_model.data_is_valid() \
        and self.mass_atten_coeff_model.data_is_valid() \
        and self.dose_buildup_model.data_is_valid():
            self.ui.saveButton.setEnabled(True)
            self.ui.errorLabel.setVisible(False)
            self.ui.correctnessErrorLabel.setVisible(False)
            
        elif MaterialRegistry.has_key(material_name) \
        and material_name != self.material_original_name:
            self.ui.saveButton.setEnabled(False)
            self.ui.errorLabel.setVisible(True)
            self.ui.correctnessErrorLabel.setVisible(True)
        
        elif MaterialRegistry.has_key(material_name) \
        and self.mu_d_model.data_is_valid() \
        and self.e_model.data_is_valid() \
        and self.mass_atten_coeff_model.data_is_valid() \
        and self.dose_buildup_model.data_is_valid():
            self.ui.saveButton.setEnabled(True)
            self.ui.errorLabel.setVisible(False)
            self.ui.correctnessErrorLabel.setVisible(False)
        
        else:
            self.ui.saveButton.setEnabled(False)
            self.ui.errorLabel.setVisible(False)
            self.ui.correctnessErrorLabel.setVisible(True)
        
    @QtCore.pyqtSlot()
    def on_deleteButton_clicked(self):
        messagebox = RDeleteMaterialMessageBox(self)
        choice = messagebox.exec_()
        
        if choice == messagebox.Yes:
            db = MaterialDatabase()
            db.remove(self.material_original_name)
            
            self.parent.reload_comboboxes()
            self.parent.parent.reload_comboboxes()
            
            self.close()
        
    @QtCore.pyqtSlot()
    def on_saveButton_clicked(self):
        m = transpose(self.mass_atten_coeff_model.cells)
        mass_atten_coeff = [list(m[0][:-1]), list(m[1][:-1])]
        
        title = unicode(self.ui.materialTitleLineEdit.text())
        
        kwargs = {
                  'title': title,
                  'data': {
                           'mu_d': self.mu_d_model.cells[0][:-1],
                           'e': [v[0] for v in self.e_model.cells[:-1]],
                           'b': self.dose_buildup_model.cells,
                           'mass_attenuation_coefficient': mass_atten_coeff,
                           'density': self.ui.materialDensityDoubleSpinBox.value(),
                           },
                  }
        
        db = MaterialDatabase()
        db.update(self.material_original_name, **kwargs)
        
        self.parent.reload_comboboxes()
        self.parent.parent.reload_comboboxes()

        self.close()
