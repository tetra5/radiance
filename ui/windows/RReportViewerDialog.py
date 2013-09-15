# -*- coding: utf-8 -*-


"""
Created on 15.02.2011

@author: vda
"""

import os

from jinja2 import Template, filters, exceptions
from PyQt4 import QtCore, QtGui

from ui.gui.radiancereportviewerdialog import Ui_RReportViewerDialog
from settings import settings, TEMPLATE_TYPES
from logic.models.tablemodels import GenericTableModel
from logic.registry import ReportRegistry
from ui.widgets.RTemplateEngineErrorMessageBox import \
    RTemplateEngineErrorMessageBox


def datetimeformat(value, format='%d.%m.%Y - %H:%M:%S'):
    return value.strftime(format)


filters.FILTERS['datetimeformat'] = datetimeformat


DEFAULT_ERROR_TEMPLATE = u"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="content-type" content="text/html;charset=UTF-8">
        <title>!</title>
        <style type="text/css" media="screen">
            body {
                color: #444;
                margin: 0px;
            }
            div.container {
                margin: 0 auto;
                margin-top: 100px;
                text-align: left;
                width: 80%;
            }
            p.label {
                color: #dedede;
                font-size: 5em;
                margin-bottom: -36px;
                margin-left: -6px;
                padding: 0px;
                font-weight: bold;
            }
            p.message {
                text-align: center;
                padding: 10px;
                border: 1px solid #ddd;
                font-size: 1.1em;
                display: block;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <p class="label">
                {{ error_label }}
            </p>
            <p class="message">
                {{ error_message }}
            </p>
        </div>
    </body>
</html>
"""


class RReportViewerDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_RReportViewerDialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.__init()
        
    def __init(self):
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowMaximizeButtonHint)
        
        ReportRegistry.reload()

        templates = {}
        for template_type, template_file in TEMPLATE_TYPES.iteritems():
            template_path = os.path.join(settings.get('template_path'), template_file)
            template = QtCore.QFile(template_path)
            if template.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
                template_str = unicode(QtCore.QString.fromUtf8(template.readAll()))
                templates.update({template_type: template_str})
                template.close()
        self.templates = templates
                
        items = [[report.date.strftime('%d.%m.%Y %H:%M:%S')] for report in ReportRegistry.itervalues()]
        
        if items:
            items.sort(reverse=True)
        else:
            self.ui.saveButton.setEnabled(False)
            
        self.model = GenericTableModel(items)
        self.ui.tableView.setModel(self.model)
        self.selection_model = self.ui.tableView.selectionModel()
        
        self.connect(self.selection_model, QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"), self.show_report)
        
        self.ui.tableView.selectRow(0)
        
    @QtCore.pyqtSlot()
    def on_saveButton_clicked(self):
        if settings.get('locale') == 'ru_RU':
            header = u'Сохранение отчёта'
            extensions = u'Файлы отчётов (*.html)'
        else:
            header = u'Save report'
            extensions = u'Report files (*.html)'
            
        filename = QtGui.QFileDialog.getSaveFileName(self, header, os.path.expanduser('~'), extensions)
        if not filename.isEmpty():
            outfile = QtCore.QFile(filename)
            if outfile.open(QtCore.QIODevice.WriteOnly | QtCore.QIODevice.Text):
                outfile.writeData(QtCore.QString.fromUtf8(self.content))
                outfile.close()
            else:
                raise IOError

    def show_report(self):
        current_selected_row = len(self.model.cells) - self.selection_model.currentIndex().row()
        report = ReportRegistry.get(current_selected_row)
        
        template = self.templates.get(report.template_type)
        
        if template is None:
            self.ui.saveButton.setEnabled(False)
            if settings.get('locale') == 'ru_RU':
                data = {
                        'error_label': u'Ошибка!',
                        'error_message': u'Невозможно загрузить шаблон "%s"' % TEMPLATE_TYPES.get(report.template_type),
                        }
            else:
                data = {
                        'error_label': u'Error!',
                        'error_message': u'Could not load template "%s"' % TEMPLATE_TYPES.get(report.template_type),
                        }
                
            template = Template(DEFAULT_ERROR_TEMPLATE)
            content = template.render(data)
            
        else:
            self.ui.saveButton.setEnabled(True)
            try:
                p_list_roentgen = report.data.get('p_list')
                p_list_sievert = [p * 10 for p in p_list_roentgen]
                p_list_combined = list()
                for p_roentgen, p_sievert in zip(p_list_roentgen, p_list_sievert):
                    p_list_combined.append(dict(roentgen=p_roentgen,
                                                sievert=p_sievert))
                
                from radiance import __version__
                data = dict()
                data.update(report.data)
                data.update(dict(version=__version__))
                data.update(dict(p_list=p_list_combined))
                data.update(dict(p_sievert=report.data.get('p') * 10))
                
                content = Template(template).render(data)
                self.ui.webView.setHtml(content)
            except exceptions.UndefinedError, e:
                messagebox = RTemplateEngineErrorMessageBox(self, str(e))
                messagebox.exec_()
            except:
                message = self.trUtf8('Unknown error')
                messagebox = RTemplateEngineErrorMessageBox(self, message)
            else:
                self.content = content
                
