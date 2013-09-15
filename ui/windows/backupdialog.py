# -*- coding: utf-8 -*-


"""
Created on 25.02.2011

@author: vda
"""

import os
import datetime
import zipfile

from PyQt4 import QtCore, QtGui

from ui.gui.radiancebackupdialog import Ui_RBackupDialog
from settings import settings
from logic.misc.pyfs import recursive_glob


class RBackupDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_RBackupDialog()
        self.ui.setupUi(self)
        
        self.__init()
        
    def __init(self):
        # Signals
        self.ui.mainDatabaseCheckBox.stateChanged.connect(self._process_form)
        self.ui.reportDatabaseCheckBox.stateChanged.connect(self._process_form)
        self.ui.templateFilesCheckBox.stateChanged.connect(self._process_form)
        
    def _process_form(self):
        enabled_state = self.ui.mainDatabaseCheckBox.isChecked() \
                        or self.ui.reportDatabaseCheckBox.isChecked() \
                        or self.ui.templateFilesCheckBox.isChecked() \
                        or self.ui.templateFilesCheckBox.isChecked()
        self.ui.saveButton.setEnabled(enabled_state)
        self.ui.archiveTypeComboBox.setEnabled(enabled_state)
    
    @QtCore.pyqtSlot()
    def on_saveButton_clicked(self):
        if settings.get('locale') == 'ru_RU':
            header = u'Сохранение резервной копии'
            extensions = u'Файлы резервного копирования (*.zip)'
        else:
            header = u'Save backup'
            extensions = u'Backup files (*.zip)'
            
        date = datetime.datetime.now().strftime('%d_%m_%Y___%H_%M_%S')
        filepath = os.path.join(os.path.expanduser('~'), 'Radiance_%s' % date)
        
        filename = QtGui.QFileDialog.getSaveFileName(self, header, filepath, extensions)
        if not filename.isEmpty():
            try:
                files = []
                if self.ui.mainDatabaseCheckBox.isChecked():
                    files.append('./radiance.db')
                if self.ui.reportDatabaseCheckBox.isChecked():
                    files.append('./reports.db')
                if self.ui.templateFilesCheckBox.isChecked():
                    files.extend(list(recursive_glob(settings.get('template_path'), '*')))
                
                files = [os.path.normpath(path) for path in files]
                
                filename = unicode(os.path.normpath('%s.zip' % filename))
                
                archive = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
                for file in files:
                    archive.write(file, file)
                archive.close()
                
            except IOError:
                raise
            
            else:
                self.close()