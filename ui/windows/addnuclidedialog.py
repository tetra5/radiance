# -*- coding: utf-8 -*-


"""
Created on 26.10.2010

@author: vda
"""


from PyQt4 import QtCore, QtGui

from ui.gui.radianceaddnuclidedialog import Ui_RAddNuclideDialog
from ui.widgets.nuclidedisplaywidget import NuclideDisplayWidget
from logic.models.tablemodels import GammaSpectrumEditableTableModel, \
    GammaSpectrumTableModel
from ui.misc.delegate import DoubleSpinBoxDelegate
from logic import elements
from logic.registry import NuclideRegistry
from logic.db import NuclideDatabase
from logic.misc.functions import clean_list
from logic.misc.struct import Struct


class RAddNuclideDialog(QtGui.QDialog):
    
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_RAddNuclideDialog()
        self.ui.setupUi(self)
        self.parent = parent
        
        self.__init()
        
    def __init(self):
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowMaximizeButtonHint)
        
        # nuclide display widget init
        self.nuclide_display_widget = NuclideDisplayWidget(self, bg="#000000", fg="#FFFFFF")
        self.ui.topLayout.insertWidget(0, self.nuclide_display_widget)
        
        # gamma spectrum table view/model
        table = self.ui.gammaSpectrumTableView
        table.horizontalHeader().setResizeMode(1)
        table.setItemDelegate(DoubleSpinBoxDelegate())
        # creates editable model with first empty row
        self.model = GammaSpectrumEditableTableModel()
        table.setModel(self.model)
        
        # signals
        self.ui.elementComboBox.currentIndexChanged.connect(self._process_form)
        self.ui.elementComboBox.editTextChanged.connect(self._process_form)
        self.ui.atomicMassSpinBox.valueChanged.connect(self._process_form)
        self.model.dataChanged.connect(self._process_form)
        
        # elements combobox
        self.ui.elementComboBox.insertItems(0, sorted(elements.get_elements_names_list()))
        self.ui.elementComboBox.setCurrentIndex(0)

    @QtCore.pyqtSlot()
    def on_addButton_clicked(self):
        """
        Cleans input data, adds nuclide to database, reloads nuclide registry, 
        and nuclide comboboxes at reference dialog and main window
        """
        
        spectre = clean_list(self.model.cells)
        
        # this should never happen due to user input validation, still 
        # worth checking
        if not spectre:
            raise Exception, "Gamma spectrum is invalid."
        
        # this should not happen, same as above
        if None in (self.nuclide.lat, self.nuclide.eng, self.nuclide.rus, 
                    self.nuclide.a_mass, self.nuclide.a_num):
            raise Exception, "Nuclide data is invalid."
            
        db = NuclideDatabase()

        data = {
                'spectre': spectre,
                }
        
        db.add(self.nuclide.eng, self.nuclide.a_mass, data)
        
        self.parent.reload_comboboxes()
        self.parent.parent.reload_comboboxes()
        
        self.close()
    
    def _process_form(self):
        element_name = unicode(self.ui.elementComboBox.currentText())
        a_mass = self.ui.atomicMassSpinBox.value()
        nuclide_name = '-'.join((element_name, str(a_mass)))
        
        # capitalizes input string for more convenient completer usage
        self.ui.elementComboBox.setEditText(element_name.capitalize())
        
        try:
            element = elements.get_element(element_name)
        
        except elements.ElementNotFound:
            a_num, lat, eng, rus = 0, None, None, None
            self.ui.addButton.setEnabled(False)
        
        else:
            a_num, lat, eng, rus = element
            
            if NuclideRegistry.has_key(nuclide_name):
                self.ui.addButton.setEnabled(False)
                self.ui.errorLabel.setVisible(True)
                model = GammaSpectrumTableModel(NuclideRegistry.get(nuclide_name).spectre)
                self.ui.gammaSpectrumTableView.setModel(model)
                self.ui.correctnessErrorLabel.setVisible(True)
            
            else:
                self.ui.errorLabel.setVisible(False)
                self.ui.gammaSpectrumTableView.setModel(self.model)
                
                if self.model.data_is_valid() and element_name:
                    self.ui.addButton.setEnabled(True)
                    self.ui.correctnessErrorLabel.setVisible(False)
                    
                else:
                    self.ui.addButton.setEnabled(False)
                    self.ui.correctnessErrorLabel.setVisible(True)
                    
        finally:
            kwargs = {
                      'a_num': a_num,
                      'a_mass': a_mass,
                      'lat': lat,
                      'eng': eng,
                      'rus': rus,
                      }
        
            self.nuclide = Struct(**kwargs)
            
            self.nuclide_display_widget.set_data(self.nuclide)
            self.ui.atomicNumberSpinBox.setValue(a_num)
