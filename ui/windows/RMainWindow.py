# -*- coding: utf-8 -*-


"""
Created on 13.10.2010

@author: vda
"""

import datetime
import logging

from PyQt4.QtCore import Qt, QSettings, pyqtSlot
from PyQt4.QtGui import QMainWindow, QApplication, QCursor, QMessageBox

from ui.gui.radiancemainwindow import Ui_RadianceMainWindow
from logic.registry import NuclideRegistry, MaterialRegistry, \
    LayeredMaterialRegistry
from logic.computation import simulate_screen, simulate_layered_screen
from logic.models.tablemodels import GammaSpectrumTableModel, \
    EmptyNuclideTableModel, LayeredMaterialTableModel, \
    EmptyLayeredMaterialTableModel
from ui.windows.referencedialog import RReferenceDialog
from ui.windows.backupdialog import RBackupDialog
from ui.windows.RHelpViewerDialog import RHelpViewerDialog
from ui.widgets.RAboutMessageBox import RAboutMessageBox
from logic.exceptions import ScreenSimulationFailed, \
    LayeredScreenSimulationFailed, TabWidgetIndexOutOfRange, \
    UnsupportedTemplateType
from ui.windows.RReportViewerDialog import RReportViewerDialog
from logic.db import ReportDatabase
from settings import TEMPLATE_TYPES, SL_SCREEN_OK, SL_SCREEN_ERR, \
    ML_SCREEN_OK, ML_SCREEN_ERR


log = logging.getLogger('Radiance')


class RMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(RMainWindow, self).__init__(parent)
        self.ui = Ui_RadianceMainWindow()
        self.ui.setupUi(self)
        self.__init()
    
    def __init(self):
        """
        Custom window and widget settings, signals, etc.
        """
        
        self.__form_data = {} 
        self.__read_settings() # loads main window settings from registry
        self.setContextMenuPolicy(Qt.NoContextMenu)
        
        # Signals.
        for signal in [
                       self.ui.nuclideComboBoxPage1.currentIndexChanged, # page 1
#                       self.ui.radioactiveDecayDoubleSpinBoxPage1.valueChanged, #page 1
                       self.ui.materialComboBox.currentIndexChanged, # page 1
#                       self.ui.materialThicknessDoubleSpinBox.valueChanged, # page 1
#                       self.ui.materialDensityDoubleSpinBox.valueChanged, # page 1
#                       self.ui.distanceDoubleSpinBoxPage1.valueChanged, # page 1
                       self.ui.nuclideComboBoxPage2.currentIndexChanged, # page 2
#                       self.ui.radioactiveDecayDoubleSpinBoxPage2.valueChanged, # page 2
                       self.ui.layeredMaterialComboBox.currentIndexChanged, # page 2
#                       self.ui.distanceDoubleSpinBoxPage2.valueChanged, # page 2
                       self.ui.tabWidget.currentChanged, # page switching
                       ]:
            signal.connect(self.__process_form)
            
        # Table views resize modes.
        for header in [
                       self.ui.gammaSpectrumTableViewPage1.horizontalHeader(),
                       self.ui.gammaSpectrumTableViewPage2.horizontalHeader(),
                       self.ui.layeredMaterialLayersTableView.horizontalHeader(),
                       ]:
            header.setResizeMode(1)
        
        self.reload_comboboxes()
        
    def _process_form_index0(self):
        nuclide = NuclideRegistry.get(unicode(self.ui.nuclideComboBoxPage1.currentText()))
        material = MaterialRegistry.get(unicode(self.ui.materialComboBox.currentText()))
        
        # nuclide widgets
        state = bool(nuclide)
        for widget in [
                       self.ui.nuclideComboBoxPage1,
                       self.ui.radioactiveDecayDoubleSpinBoxPage1,
                       ]:
            widget.setEnabled(state)
        for header in [
                       self.ui.gammaSpectrumTableViewPage1.horizontalHeader(),
                       self.ui.gammaSpectrumTableViewPage1.verticalHeader(),
                       ]:
            header.setVisible(state)
        if state:
            model = GammaSpectrumTableModel(nuclide.spectre)
        else:
            model = EmptyNuclideTableModel()
        self.ui.gammaSpectrumTableViewPage1.setModel(model)

        # material widgets
        state = bool(material)
        for widget in [
                       self.ui.materialComboBox,
                       self.ui.materialDensityDoubleSpinBox,
                       self.ui.materialThicknessDoubleSpinBox,
                       ]:
            widget.setEnabled(state)
        if state:
            self.ui.materialDensityDoubleSpinBox.setValue(float(material.density))
            
        # nuclide and material widgets
        state = bool(nuclide) and bool(material)
        self.ui.simulateButton.setEnabled(state)
        self.ui.correctnessErrorLabel.setVisible(not state)
        
        self.nuclide = nuclide
        self.material = material
        
    def _process_form_index1(self):
        nuclide = NuclideRegistry.get(unicode(self.ui.nuclideComboBoxPage2.currentText()))
        layered_material = LayeredMaterialRegistry.get(unicode(self.ui.layeredMaterialComboBox.currentText()))
        
        # nuclide widgets
        state = bool(nuclide)
        for widget in [
                       self.ui.nuclideComboBoxPage2,
                       self.ui.radioactiveDecayDoubleSpinBoxPage2,
                       ]:
            widget.setEnabled(state)
        for header in [
                       self.ui.gammaSpectrumTableViewPage2.horizontalHeader(),
                       self.ui.gammaSpectrumTableViewPage2.verticalHeader(),
                       ]:
            header.setVisible(state)
        if state:
            model = GammaSpectrumTableModel(nuclide.spectre)
        else:
            model = EmptyNuclideTableModel()
        self.ui.gammaSpectrumTableViewPage2.setModel(model)
        
        # layered material widgets
        state = bool(layered_material)
        for widget in [
                       self.ui.layeredMaterialComboBox,
                       ]:
            widget.setEnabled(state)
        for header in [
                       self.ui.layeredMaterialLayersTableView.horizontalHeader(),
                       self.ui.layeredMaterialLayersTableView.verticalHeader(),
                       ]:
            header.setVisible(state)
        if state:
            data = []
            valid = True
            total_thickness = 0.0
            for material_id, thickness in layered_material.layers:
                total_thickness += thickness
                layer = [MaterialRegistry.get_by_id(material_id), thickness]
                data.append(layer)
                if None in layer:
                    valid = False
            self.ui.layeredMaterialThicknessDoubleSpinBox.setValue(total_thickness)
            model = LayeredMaterialTableModel(data)
        else:
            self.ui.layeredMaterialThicknessDoubleSpinBox.setValue(0.01)
            model = EmptyLayeredMaterialTableModel()
        self.ui.layeredMaterialLayersTableView.setModel(model)
        
        # nuclide and layered material widgets and data is valid
        state = bool(nuclide) and bool(layered_material) and valid
        self.ui.simulateButton.setEnabled(state)
        self.ui.correctnessErrorLabel.setVisible(not state)
        
        self.nuclide = nuclide
        self.layered_material = layered_material
        
    def __write_settings(self):
        settings = QSettings()
        settings.beginGroup('UI/{0}'.format(self.__class__.__name__))
        settings.setValue('Geometry', self.saveGeometry())
        settings.setValue('State', self.saveState())
        settings.endGroup()
    
    def __read_settings(self):
        settings = QSettings()
        settings.beginGroup('UI/{0}'.format(self.__class__.__name__))
        self.restoreGeometry(settings.value('Geometry').toByteArray())
        self.restoreState(settings.value('State').toByteArray())
        settings.endGroup()
    
    def closeEvent(self, event):
        self.__write_settings()
    
    def __process_form(self):
        method = '%s%d' % ('_process_form_index', self.ui.tabWidget.currentIndex())
        try:
            getattr(self, method)()
        except AttributeError:
            raise TabWidgetIndexOutOfRange, self.__current_tab_index()

    def __simulate_screen(self, **kwargs):
        """Single-layered screen simulation.
        http://mathurl.com/
        P=\frac{Q}{R^2}\sum_{j=1}^{m}K'_{\gamma_{j}}*n_{E_{j}}*e^{-\mu_{E_{j}d}}*B^{\mu_{E_{j}d}}
        """
        
        try:
            (p, p_list) = simulate_screen(**kwargs)

        except:
            raise ScreenSimulationFailed
        
        return (p, p_list)
        
    def __simulate_layered_screen(self, **kwargs):
        """Multi-layered screen simulation."""
        
        raise LayeredScreenSimulationFailed
        
        return (None, None)
    
    @pyqtSlot()
    def on_simulateButton_clicked(self):
        self.ui.simulateButton.setEnabled(False)
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        
        result_data = {}
        
        try:
            if self.ui.tabWidget.currentIndex() == 0:
                """ Screen simulation template variables:
                
                nuclide = {
                    a_mass,
                    a_num,
                    lat,
                    eng,
                    rus,
                    spectre = [ ... ],
                    },
                material = {
                    b = [ ... ],
                    e = [ ... ],
                    mass_atten_coeff_x = [ ... ],
                    mass_atten_coeff_y = [ ... ],
                    mu_d = [ ... ],
                    title,
                    density, # default
                    },
                d,
                density, # user defined
                q,
                r,
                date,
                # --- after simulation ---
                    p,
                    p_list = [ ... ]
                """
                self.__form_data = {
                        'nuclide': self.nuclide,
                        'material': self.material,
                        'd': self.ui.materialThicknessDoubleSpinBox.value(),
                        'density': self.ui.materialDensityDoubleSpinBox.value(),
                        'q': self.ui.radioactiveDecayDoubleSpinBoxPage1.value(),
                        'r': self.ui.distanceDoubleSpinBoxPage1.value(),
                        }
                
                try:
                    result = self.__simulate_screen(**self.__form_data)
                except ScreenSimulationFailed:
                    template_type = SL_SCREEN_ERR
                    log.error('Screen simulation failed.')
                    raise
                else:
                    # screen simulation report
                    template_type = SL_SCREEN_OK
                    p, p_list = result
                    result_data = dict(
                                       p=float(p),
                                       p_list=[float(p) for p in p_list],
                                       )
            # layered screen simulation    
            elif self.ui.tabWidget.currentIndex() == 1:
                self.__form_data = {
                    'nuclide': self.nuclide,
                    'layered_material': self.layered_material,
                    'r': self.ui.distanceDoubleSpinBoxPage2.value(),
                    }
                
                try:
                    result = self.__simulate_layered_screen(**self.__form_data)
                except LayeredScreenSimulationFailed:
                    template_type = ML_SCREEN_ERR
                    log.error('Layered screen simulation failed.')
                    raise
                else:
                    # layered screen simulation report
                    template_type = ML_SCREEN_OK
            else:
                raise TabWidgetIndexOutOfRange
                    
        except ScreenSimulationFailed:
            QApplication.restoreOverrideCursor()
            message = self.trUtf8('Screen simulation failed.')
            QMessageBox.critical(self, self.trUtf8('Error'), message)
            
        except LayeredScreenSimulationFailed:
            QApplication.restoreOverrideCursor()
            message = self.trUtf8('Layered screen simulation failed.')
            QMessageBox.critical(self, self.trUtf8('Error'), message)
        
        except TabWidgetIndexOutOfRange:
            raise
            
        else:
            if template_type in TEMPLATE_TYPES:
                date = datetime.datetime.now()
                result = {}
                result.update(self.__form_data)
                result.update(result_data)
                result.update(dict(date=date))
                db = ReportDatabase()
                db.add(date, result, template_type)
            else:
                raise UnsupportedTemplateType
            
            QApplication.restoreOverrideCursor()
            
            # shows report browser
            report = RReportViewerDialog(self)
            report.exec_()
        
        self.ui.simulateButton.setEnabled(True)
    
    @pyqtSlot()
    def on_actionBackup_triggered(self):
        dialog = RBackupDialog(self)
        dialog.exec_()
    
    @pyqtSlot()
    def on_actionReports_triggered(self):
        self.ui.simulateButton.setEnabled(False)
        dialog = RReportViewerDialog(self)
        dialog.exec_()
        self.ui.simulateButton.setEnabled(True)
    
    @pyqtSlot()
    def on_actionReference_triggered(self):
        dialog = RReferenceDialog(self)
        dialog.show()
     
    @pyqtSlot()    
    def on_actionContents_triggered(self):
        dialog = RHelpViewerDialog(self)
        dialog.show()
        
    @pyqtSlot()
    def on_actionAbout_triggered(self):
        dialog = RAboutMessageBox(self)
        dialog.exec_()
    
    def reload_comboboxes(self):
        comboboxes = [
                      self.ui.layeredMaterialComboBox,
                      self.ui.materialComboBox,
                      self.ui.nuclideComboBoxPage1,
                      self.ui.nuclideComboBoxPage2,
                      ]
        
        registries = [
                      LayeredMaterialRegistry,
                      MaterialRegistry,
                      NuclideRegistry,
                      NuclideRegistry,
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
    
