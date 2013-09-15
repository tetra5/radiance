# -*- coding: utf-8 -*-


"""
Created on 13.10.2010

@author: vda
"""

from copy import deepcopy

from PyQt4 import QtCore, QtGui

from ui.gui.radiancereferencedialog import Ui_RadianceReferenceDialog
from ui.widgets.nuclidedisplaywidget import NuclideDisplayWidget
from ui.windows.addnuclidedialog import RAddNuclideDialog
from ui.windows.editnuclidedialog import REditNuclideDialog
from ui.windows.addmaterialdialog import RAddMaterialDialog
from ui.windows.editmaterialdialog import REditMaterialDialog
from ui.windows.addlayeredmaterialdialog import RAddLayeredMaterialDialog
from ui.windows.editlayeredmaterialdialog import REditLayeredMaterialDialog
from logic.registry import NuclideRegistry, MaterialRegistry, \
    LayeredMaterialRegistry
from logic.misc.functions import recursive_map, transpose
from logic.models.tablemodels import GenericTableModel, \
    MassAttenuationCoefficientTableModel, GammaSpectrumTableModel, \
    EmptyMaterialTableModel, EmptyNuclideTableModel, \
    EmptyLayeredMaterialTableModel, LayeredMaterialTableModel
    

class RReferenceDialog(QtGui.QDialog):
    
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_RadianceReferenceDialog()
        self.ui.setupUi(self)
        self.parent = parent
        
        self.__init()
        
    def __init(self):
        """
        Custom window and widget settings, signals, etc.
        """
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        # Nuclide display widget init
        self.nuclide_display_widget = NuclideDisplayWidget(self)
        self.ui.nuclideTopLayout.insertWidget(0, self.nuclide_display_widget)
        
        # Signals
        self.ui.nuclideComboBox.currentIndexChanged.connect(self._process_form)
        self.ui.materialComboBox.currentIndexChanged.connect(self._process_form)
        self.ui.multiLayeredMaterialComboBox.currentIndexChanged.connect(self._process_form)
        
        # Window flags
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowMaximizeButtonHint)
        
        # Nuclide gamma spectrum table view settings
        table = self.ui.nuclideGammaSpectrumTableView
        table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        table.horizontalHeader().setResizeMode(1)
        
        # Material dose buildup factor table view settings
        table = self.ui.materialDoseBuildupFactorTableView
        table.horizontalHeader().setResizeMode(1)
        
        # Material mass attenuation coefficient table view settings
        table = self.ui.materialMassAttenuationCoefficientTableView
        table.horizontalHeader().setResizeMode(1)
        
        # Layered material layers table view settings
        table = self.ui.materialLayersTableView
        table.horizontalHeader().setResizeMode(1)
        
        # inserts initial nuclides and materials into corresponding comboboxes
        self.reload_comboboxes()
        
    @QtCore.pyqtSlot()
    def on_addNuclideButton_clicked(self):
        dialog = RAddNuclideDialog(self)
        dialog.exec_()

    @QtCore.pyqtSlot()
    def on_editNuclideButton_clicked(self):
        nuclide = deepcopy(self.nuclide)
        
        dialog = REditNuclideDialog(nuclide, unicode(self.ui.nuclideComboBox.currentText()), self)
        dialog.exec_()
        
    @QtCore.pyqtSlot()
    def on_addMaterialButton_clicked(self):
        dialog = RAddMaterialDialog(self)
        dialog.exec_()
        
    @QtCore.pyqtSlot()
    def on_editMaterialButton_clicked(self):
        material = deepcopy(self.material)
        
        dialog = REditMaterialDialog(material, unicode(self.ui.materialComboBox.currentText()), self)
        dialog.exec_()
        
    @QtCore.pyqtSlot()
    def on_addMultiLayeredMaterialButton_clicked(self):
        dialog = RAddLayeredMaterialDialog(self)
        dialog.exec_()
        
    @QtCore.pyqtSlot()
    def on_editMultiLayeredMaterialButton_clicked(self):
        layered_material = deepcopy(self.layered_material)
        layered_material_default_title = unicode(self.ui.multiLayeredMaterialComboBox.currentText()) 
        
        dialog = REditLayeredMaterialDialog(layered_material, layered_material_default_title, self)
        dialog.exec_()

    def _process_form(self):
        self.nuclide = NuclideRegistry.get(unicode(self.ui.nuclideComboBox.currentText()))
        self.material = MaterialRegistry.get(unicode(self.ui.materialComboBox.currentText()))
        self.layered_material = LayeredMaterialRegistry.get(unicode(self.ui.multiLayeredMaterialComboBox.currentText()))
        
        # nuclide form
        state = bool(self.nuclide)
        for widget in [
                       self.ui.editNuclideButton,
                       self.ui.nuclideComboBox,
                       ]:
            widget.setEnabled(state)
        for header in [
                       self.ui.nuclideGammaSpectrumTableView.verticalHeader(),
                       self.ui.nuclideGammaSpectrumTableView.horizontalHeader(),
                       ]:
            header.setVisible(state)
        if state:
            model = GammaSpectrumTableModel(self.nuclide.spectre)
            self.nuclide_display_widget.set_data(self.nuclide)
        else:
            model = EmptyNuclideTableModel()
            self.nuclide_display_widget.reset()
        self.ui.nuclideGammaSpectrumTableView.setModel(model)
        
        # material form
        state = bool(self.material)
        for widget in [
                       self.ui.editMaterialButton,
                       self.ui.materialComboBox,
                       ]:
            widget.setEnabled(state)
        for header in [
                       self.ui.materialDoseBuildupFactorTableView.verticalHeader(),
                       self.ui.materialDoseBuildupFactorTableView.horizontalHeader(),
                       self.ui.materialMassAttenuationCoefficientTableView.horizontalHeader(),
                       self.ui.rhoLabel,
                       self.ui.rhoValueLabel,
                       ]:
            header.setVisible(state)
        if state:
            data = recursive_map(lambda x: str(x).replace('.', ','), self.material.b)
            v_header = [str(k) for k in self.material.e]
            h_header = [str(k) for k in [round(float(x), 1) for x in self.material.mu_d]]
            dose_buildup_model = GenericTableModel(data, v_header, h_header)
            
            data = [self.material.mass_atten_coeff_x, self.material.mass_atten_coeff_y]
            data = recursive_map(lambda x: str(x).replace('.', ','), transpose(data))
            mass_atten_coeff_model = MassAttenuationCoefficientTableModel(data)
            
            label = '%s %s' % (str(self.material.density), unicode(self.trUtf8('g/cm³')))
            self.ui.rhoValueLabel.setText(label)
        else:
            dose_buildup_model = mass_atten_coeff_model = EmptyMaterialTableModel()
        self.ui.materialDoseBuildupFactorTableView.setModel(dose_buildup_model)
        self.ui.materialMassAttenuationCoefficientTableView.setModel(mass_atten_coeff_model)
        
        # layered material form
        state = bool(self.layered_material)
        for widget in [
                       self.ui.editMultiLayeredMaterialButton,
                       self.ui.multiLayeredMaterialComboBox,
                       ]:
            widget.setEnabled(state)
        for header in [
                       self.ui.materialLayersTableView.verticalHeader(),
                       self.ui.materialLayersTableView.horizontalHeader(),
                       ]:
            header.setVisible(state)
        if state:
            data = []
            for material_id, thickness in self.layered_material.layers:
                data.append([MaterialRegistry.get_by_id(material_id), thickness])
            model = LayeredMaterialTableModel(data)
        else:
            model = EmptyLayeredMaterialTableModel()
        self.ui.materialLayersTableView.setModel(model)
        
    def reload_comboboxes(self):
        comboboxes = [
                      self.ui.nuclideComboBox,
                      self.ui.materialComboBox,
                      self.ui.multiLayeredMaterialComboBox,
                      ]
        
        registries = [
                      NuclideRegistry,
                      MaterialRegistry,
                      LayeredMaterialRegistry,
                      ]
        
        for combobox, registry in zip(comboboxes, registries):
            registry.reload()
            
            if registry:
                prev_item = unicode(combobox.currentText())
                prev_index = combobox.findText(prev_item)
                
                combobox.clear()
                combobox.insertItems(0, sorted(registry.keys()))
                
                if prev_item and prev_index > 0:
                    combobox.setCurrentIndex(prev_index)
                else:
                    combobox.setCurrentIndex(0)
                    
            else:
                combobox.insertItems(0, [''])
                combobox.setCurrentIndex(0)
                combobox.clear()
        