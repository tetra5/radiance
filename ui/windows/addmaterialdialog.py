# -*- coding: utf-8 -*-


"""
Created on 13.11.2010

@author: razor
"""

from PyQt4 import QtCore, QtGui

from ui.gui.radianceaddmaterialdialog import Ui_RAddMaterialDialog
from logic.models.tablemodels import MuDEditableTableModel, \
    EEditableTableModel, DoseBuildUpFactorEditableTableModel, \
    MassAttenuationCoefficientEditableTableModel
from ui.misc.delegate import DoubleSpinBoxDelegate, IntegerSpinBoxDelegate
from logic.registry import MaterialRegistry
from logic.db import MaterialDatabase
from logic.misc.functions import transpose


class RAddMaterialDialog(QtGui.QDialog):
    
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_RAddMaterialDialog()
        self.ui.setupUi(self)
        self.parent = parent
        
        self.__init()
        
    def __init(self):
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowMaximizeButtonHint)
        
        # models
        self.mu_d_model = MuDEditableTableModel([[1, 2, 4, 7, 10, 15, 20]])
        self.e_model = EEditableTableModel()
        self.mass_atten_coeff_model = MassAttenuationCoefficientEditableTableModel()
        self.dose_buildup_model = DoseBuildUpFactorEditableTableModel()
        #self.dose_buildup_model = EmptyDoseBuildUpFactorTableModel()
        
        # signals
        self.mu_d_model.dataChanged.connect(self._rebuild_dose_buildup_table)
        self.e_model.dataChanged.connect(self._rebuild_dose_buildup_table)
        #self.dose_buildup_model.dataChanged.connect(self._process_form)
        self.mass_atten_coeff_model.dataChanged.connect(self._process_form)
        self.ui.materialTitleLineEdit.textChanged.connect(self._process_form)
        self.ui.materialTitleLineEdit.textEdited.connect(self._process_form)
        
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
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)
        table.setModel(self.dose_buildup_model)
    
        # mass attenuation coefficient table view and model
        table = self.ui.materialMassAttenuationCoefficientTableView
        table.horizontalHeader().setResizeMode(1)
        table.setItemDelegate(DoubleSpinBoxDelegate())
        table.setModel(self.mass_atten_coeff_model)
        
        self.ui.errorLabel.setVisible(False)
        self.ui.addButton.setEnabled(False)

    @QtCore.pyqtSlot()
    def on_addButton_clicked(self):
        m = transpose(self.mass_atten_coeff_model.cells)
        mass_atten_coeff = [list(m[0][:-1]), list(m[1][:-1])]
        
        data = {
                'mu_d': self.mu_d_model.cells[0][:-1],
                'e': [v[0] for v in self.e_model.cells[:-1]],
                'b': self.dose_buildup_model.cells,
                'mass_attenuation_coefficient': mass_atten_coeff,
                'density': self.ui.materialDensityDoubleSpinBox.value(),
                }
        
        title = unicode(self.ui.materialTitleLineEdit.text())
        
        db = MaterialDatabase()
        db.add(title, data)
        
        self.parent.reload_comboboxes()
        self.parent.parent.reload_comboboxes()

        self.close()
        
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
        self.ui.addButton.setEnabled(False)
        
    def _process_form(self):
        title = unicode(self.ui.materialTitleLineEdit.text())

        if MaterialRegistry.has_key(title):
            self.ui.errorLabel.setVisible(True)
            self.ui.addButton.setEnabled(False)
            self.ui.correctnessErrorLabel.setVisible(True)
        else:
            self.ui.errorLabel.setVisible(False)
            
            if self.mass_atten_coeff_model.data_is_valid() \
            and self.dose_buildup_model.data_is_valid() \
            and title:
                self.ui.addButton.setEnabled(True)
                self.ui.correctnessErrorLabel.setVisible(False)
                
            else:
                self.ui.addButton.setEnabled(False)
                self.ui.correctnessErrorLabel.setVisible(True)
                
