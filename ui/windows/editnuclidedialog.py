# -*- coding: utf-8 -*-


"""
Created on 01.11.2010

@author: vda
"""


from PyQt4 import QtCore, QtGui

from ui.gui.radianceeditnuclidedialog import Ui_REditNuclideDialog
from ui.widgets.nuclidedisplaywidget import NuclideDisplayWidget
from ui.widgets.deletenuclidemessagebox import RDeleteNuclideMessageBox
from logic.models.tablemodels import GammaSpectrumEditableTableModel
from ui.misc.delegate import DoubleSpinBoxDelegate
from logic import elements
from logic.registry import NuclideRegistry
from logic.db import NuclideDatabase
from logic.misc.functions import clean_list
from logic.misc.struct import Struct


class REditNuclideDialog(QtGui.QDialog):
    
    def __init__(self, nuclide, nuclide_original_name, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_REditNuclideDialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.nuclide = nuclide
        self.nuclide_original_name = nuclide_original_name

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
        self.model = GammaSpectrumEditableTableModel(self.nuclide.spectre)
        table.setModel(self.model)
        
        # signals
        self.ui.elementComboBox.currentIndexChanged.connect(self._process_form)
        self.ui.elementComboBox.editTextChanged.connect(self._process_form)
        self.ui.atomicMassSpinBox.valueChanged.connect(self._process_form)
        self.model.dataChanged.connect(self._process_form)
        
        element_name, a_mass = self.nuclide_original_name.split('-')
        a_mass = int(a_mass)
        
        # elements combobox
        self.ui.elementComboBox.insertItems(0, sorted(elements.get_elements_names_list()))
        self.ui.elementComboBox.setEditText(element_name)
        
        # atomic mass spinbox
        self.ui.atomicMassSpinBox.setValue(a_mass)
        
        # atomic number spinbox
        self.ui.atomicNumberSpinBox.setValue(self.nuclide.a_num)

    @QtCore.pyqtSlot()
    def on_deleteButton_clicked(self):
        # display confirmation dialog
        messagebox = RDeleteNuclideMessageBox(self)
        choice = messagebox.exec_()
        
        if choice == messagebox.Yes:
            # deletes nuclide from database, reloads nuclide registry, reloads
            # nuclide comboboxes, closes nuclide edit dialog
            db = NuclideDatabase()
            db.remove(self.nuclide_original_name)
            
            self.parent.reload_comboboxes()
            self.parent.parent.reload_comboboxes()
            
            self.close()
            
    @QtCore.pyqtSlot()
    def on_saveButton_clicked(self):
        """
        Updates nuclide database records.
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
        
        kwargs = {
                  'title': self.nuclide.eng,
                  'a_mass': self.nuclide.a_mass,
                  'data': {
                           'spectre': spectre,
                           },
                  }
        
        db.update(self.nuclide_original_name, **kwargs)
        
        NuclideRegistry.reload()
        
        # reloads reference dialog and main window nuclide comboboxes
        self.parent.reload_comboboxes()
        self.parent.parent.reload_comboboxes()
        
        self.close()

    def _process_form(self):
        element_name = unicode(self.ui.elementComboBox.currentText())
        a_mass = self.ui.atomicMassSpinBox.value()

        nuclide_name = '-'.join((element_name, str(a_mass)))

        if self.nuclide_original_name != nuclide_name:
            label_text = (' ' * 3).join((
                                         self.nuclide_original_name,
                                         u'\u2192', # unicode right arrow symbol
                                         nuclide_name,
                                         ))
            
        else:
            label_text = self.nuclide_original_name
        
        self.ui.nuclideNameLabel.setText(label_text)
        
        # capitalizes input string for more convenient completer usage
        self.ui.elementComboBox.setEditText(element_name.capitalize())
        
        try:
            element = elements.get_element(element_name)
        except elements.ElementNotFound:
            a_num, lat, eng, rus = 0, None, None, None
            self.ui.saveButton.setEnabled(False)
        else:
            a_num, lat, eng, rus = element
            
            # nuclide does not exists, table filled correctly
            if not NuclideRegistry.has_key(nuclide_name) \
            and self.model.data_is_valid():
                self.ui.saveButton.setEnabled(True)
                self.ui.errorLabel.setVisible(False)
                self.ui.correctnessErrorLabel.setVisible(False)
            
            # nuclide exists, current nuclide title is not original one
            elif NuclideRegistry.has_key(nuclide_name) \
            and nuclide_name != self.nuclide_original_name:
                self.ui.saveButton.setEnabled(False)
                self.ui.errorLabel.setVisible(True)
                self.ui.correctnessErrorLabel.setVisible(True)
                
            # nuclide exists, table filled correctly, current nuclide title
            # is original one
            elif NuclideRegistry.has_key(nuclide_name) \
            and nuclide_name == self.nuclide_original_name \
            and self.model.data_is_valid():
                self.ui.saveButton.setEnabled(True)
                self.ui.errorLabel.setVisible(False)
                self.ui.correctnessErrorLabel.setVisible(False)
        
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
        