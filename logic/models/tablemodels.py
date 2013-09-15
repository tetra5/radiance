# -*- coding: utf-8 -*-


"""
Created on 13.10.2010

@author: vda
"""


from PyQt4 import QtCore, QtGui

from logic.misc.functions import transpose


class GenericTableModel(QtCore.QAbstractTableModel):
    def __init__(self, cells, v_header=[], h_header=[], parent=None, *args):
        """
        Generic table model, suites for most needs to display data via
        QTableView.
        
        @param v_header: vertical header, list of strings
        @param h_header: horizontal header, list of strings
        @param cells: cell data, list of lists of values
        """
        super(GenericTableModel, self).__init__(parent, *args)
        
        self.v_header = v_header
        self.h_header = h_header
        self.cells = cells
        self.parent = parent
        
    def rowCount(self, parent):
        return len(self.cells)
    
    def columnCount(self, parent):
        try:
            return len(self.cells[0])
        except IndexError:
            return 0
    
    def data(self, index, role):
        if not index.isValid(): 
            return QtCore.QVariant() 
        
        if role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
            return QtCore.QVariant(self.cells[index.row()][index.column()])
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.QVariant(QtCore.Qt.AlignCenter)
        
        return QtCore.QVariant()
    
    def headerData(self, index, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if not self.h_header:
                return QtCore.QVariant("%s" % str(index + 1))
            else:
                try:
                    return QtCore.QVariant(self.h_header[index])
                except IndexError:
                    return QtCore.QVariant("%s" % str(index + 1))
        
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            if not self.v_header:
                return QtCore.QVariant("%s" % str(index + 1))
            else:
                return QtCore.QVariant(self.v_header[index])
        
        return QtCore.QVariant()
    
    def insert_blank_rows(self, position, rows_num, parent=QtCore.QModelIndex()):
        """
        Inserts multiple blank rows into a table model at specified position.
        
        @param position: row number
        @param rows_num: number of empty rows to be inserted
        """
        self.beginInsertRows(parent, position, position + rows_num - 1)
        self.endInsertRows()
    
    def append_row(self, row):
        """
        Appends row to the end of table model.
        
        @param row: ['col1', 'col2', ...]
        """
        self.insert_blank_rows(self.rowCount(self), 1)
        self.cells.append(row)
    
    def append_empty_row(self):
        if all(self.cells[-1]):
            self.append_row([0 for _ in self.cells[0]])
    
    def append_empty_column(self):
        m = transpose(self.cells)
        if all(m[-1]):
            self.append_column([0])
    
    def append_rows(self, rows):
        """
        Appends multiple rows to the end of table model.
        
        @param rows: [['col1-1', 'col1-2'], ['col2-1', 'col2-2'], ...]
        """
        self.insert_blank_rows(self.rowCount(self), len(rows))
        self.cells.extend(rows)
        
    def insert_row(self, position, row):
        """
        Inserts row into table model at specified position.
        
        @param position: row number
        @param row: ['col1', 'col2', ...]
        """
        self.insert_blank_rows(position, position)
        self.cells.insert(position, row)
        
    def insert_rows(self, position, rows):
        """
        Inserts multiple rows into table model at specified position.
        
        @param position: row number
        @param rows: [['col1-1', 'col1-2'], ['col2-1', 'col2-2'], ...]
        """
        self.insert_blank_rows(position, len(rows))
        for i, row in enumerate(rows):
            self.cells.insert(position + i, row)
            
    def insert_blank_columns(self, position, cols_num, parent=QtCore.QModelIndex()):
        """
        Inserts multiple blank columns into a table model at specified position.
        
        @param position: column number
        @param cols_num: number of empty columns to be inserted.
        """
        self.beginInsertColumns(parent, position, position + cols_num - 1)
        self.endInsertColumns()
        
    def append_column(self, column):
        """
        Appends blank column to table model.
        """
        self.insert_blank_columns(self.columnCount(self), 1)
        self.cells[0].extend(column)
                    
    def remove_row(self, position, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position)
        self.cells.pop(position)
        self.endRemoveRows()
        
    def remove_column(self, position, parent=QtCore.QModelIndex()):
        self.beginRemoveColumns(parent, position, position)
        m = transpose(self.cells)
        m.pop(position)
        self.cells = transpose(m)
        for row_num, row in enumerate(self.cells):
            self.cells[row_num] = list(row)
        self.endRemoveColumns()
    
    def _row_is_valid(self, position):
        return all(self.cells[position])
    
    def _column_is_valid(self, position):
        m = transpose(self.cells)
        return all(m[position])
    
        
class GenericEditableTableModel(GenericTableModel):
    def __init__(self, cells, v_header=[], h_header=[], parent=None, *args):
        GenericTableModel.__init__(self, cells, v_header, h_header, parent)
        
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid() and role == QtCore.Qt.EditRole:
            self.cells[index.row()][index.column()] = float(QtCore.QVariant(value).toString())
            self.dataChanged.emit(index, index)
            return True
        else:
            return False
    
    def flags(self, index):
        if not index.isValid():
            return 0

        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    
    def data_is_valid(self):
        """
        Valid:
            [
             [1, 1],
             [1, 1],
             [0, 0],
             ]
        
        Invalid:
            [
             [1, 1],
             [0, 0],
             [1, 1]
            ]
        """
        
        if self.rowCount(self) == 1:
            return False
        
        for row_num in xrange(self.rowCount(self)):
            if not self._row_is_valid(row_num) and row_num != self.rowCount(self) - 1:
                return False
            
        return True
    

class GenericEditableTableModelWithRowHighlight(GenericEditableTableModel):
    def __init__(self, cells, v_header=[], h_header=[], parent=None, *args):
        GenericEditableTableModel.__init__(self, cells, v_header, h_header, parent)
        
    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            return QtCore.QVariant(self.cells[index.row()][index.column()])
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.QVariant(QtCore.Qt.AlignCenter)
        
        if self._row_is_valid(index.row()):
            if role == QtCore.Qt.BackgroundRole:
                background = QtGui.QBrush(QtGui.QColor("#AADDAA"))
                background.setStyle(QtCore.Qt.BDiagPattern)
                return QtCore.QVariant(background)
            elif role == QtCore.Qt.ForegroundRole:
                foreground = QtGui.QBrush(QtGui.QColor("#000000"))
                return QtCore.QVariant(foreground)
        
    def flags(self, index):
        if not index.isValid():
            return 0
        
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
    
    
class GenericEditableTableModelWithColumnHighlight(GenericEditableTableModel):
    def __init__(self, cells, v_header=[], h_header=[], parent=None, *args):
        GenericEditableTableModel.__init__(self, cells, v_header, h_header, parent)
        
    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            return QtCore.QVariant(self.cells[index.row()][index.column()])
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.QVariant(QtCore.Qt.AlignCenter)
        
        if self._column_is_valid(index.column()):
            if role == QtCore.Qt.BackgroundRole:
                background = QtGui.QBrush(QtGui.QColor("#AADDAA"))
                background.setStyle(QtCore.Qt.BDiagPattern)
                return QtCore.QVariant(background)
            elif role == QtCore.Qt.ForegroundRole:
                foreground = QtGui.QBrush(QtGui.QColor("#000000"))
                return QtCore.QVariant(foreground)
        
    def flags(self, index):
        if not index.isValid():
            return 0
        
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled


class GenericEditableTableModelWithAutoColumnAppend(GenericEditableTableModelWithColumnHighlight):
    def __init__(self, cells, v_header=[], h_header=[], parent=None, *args):
        GenericEditableTableModelWithColumnHighlight.__init__(self, cells, v_header, h_header, parent)
        
        self.dataChanged.connect(self._auto_append_column)
        self.dataChanged.connect(self._auto_remove_column)
        
    def _auto_append_column(self, index):
        """
        Appends empty column whenever last table cell is changed,
        but only if previous column if filled with something.
        
        @param index: current index, do not touch
        """
        if index.column() == self.columnCount(self) - 1 and self._column_is_valid(index.column()):
            self.append_empty_column()
    
    def _auto_remove_column(self, index):
        """
        Removes empty column in the middle of table.
        """
        if index.column() != self.columnCount(self) - 1 and not self._column_is_valid(index.column()):
            self.remove_column(index.column())


class GenericEditableTableModelWithAutoRowAppend(GenericEditableTableModelWithRowHighlight):
    def __init__(self, cells, v_header=[], h_header=[], parent=None, *args):
        GenericEditableTableModelWithRowHighlight.__init__(self, cells, v_header, h_header, parent)
        
        self.dataChanged.connect(self._auto_append_row)
        self.dataChanged.connect(self._auto_remove_row)

    def _auto_append_row(self, index):
        """
        Appends empty row whenever last table cell is changed,
        but only if previous row if filled with something.
        
        @param index: current index, do not touch
        """
        if index.row() == self.rowCount(self) - 1 and self._row_is_valid(index.row()):
            self.append_empty_row()
    
    def _auto_remove_row(self, index):
        """
        Removes empty row in the middle of table.
        """
        if index.row() != self.rowCount(self) - 1 and not self._row_is_valid(index.row()):
            self.remove_row(index.row())
    

class LayeredMaterialTableModel(GenericTableModel):
    def __init__(self, cells=[], v_header=[], h_header=[], parent=None, *args):
        GenericTableModel.__init__(self, cells, v_header, h_header, parent)
        
        self.h_header = [
                         self.trUtf8("Material"),
                         self.trUtf8("Layer thickness, cm"),
                         ]

    def headerData(self, index, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if not self.h_header:
                return QtCore.QVariant("%s" % str(index + 1))
            else:
                return QtCore.QVariant(self.h_header[index])
        
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            if not self.v_header:
                return QtCore.QVariant("%s %s" % (self.trUtf8("Layer"), str(index + 1)))
            else:
                return QtCore.QVariant(self.v_header[index])
        
        return QtCore.QVariant()
    
    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            return QtCore.QVariant(self.cells[index.row()][index.column()])
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.QVariant(QtCore.Qt.AlignCenter)
        
        if not self._row_is_valid(index.row()):
            if role == QtCore.Qt.BackgroundRole:
                background = QtGui.QBrush(QtGui.QColor("#FF0000"))
                background.setStyle(QtCore.Qt.BDiagPattern)
                return QtCore.QVariant(background)
            elif role == QtCore.Qt.ForegroundRole:
                foreground = QtGui.QBrush(QtGui.QColor("#000000"))
                return QtCore.QVariant(foreground)
            
    def data_is_valid(self):
        if self.rowCount(self) < 3:
            return False
        
        for row_num in xrange(self.rowCount(self)):
            if not self._row_is_valid(row_num) and row_num != self.rowCount(self) - 1:
                return False
            elif self._row_is_totally_invalid(row_num) and row_num != self.rowCount(self) - 1:
                return False
            
        return True


class LayeredMaterialEditableTableModel(GenericEditableTableModelWithAutoRowAppend):
    def __init__(self, cells=[], v_header=[], h_header=[], parent=None, *args):
        GenericEditableTableModelWithAutoRowAppend.__init__(self, cells, v_header, h_header, parent)
        
        self.h_header = [
                         self.trUtf8("Material"),
                         self.trUtf8("Layer thickness, cm")
                         ]
        
        if not cells:
            self.cells = [[self.trUtf8("None"), 0.01], ]
        else:
            self.append_empty_row()
            
    def headerData(self, index, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if not self.h_header:
                return QtCore.QVariant("%s" % str(index + 1))
            else:
                return QtCore.QVariant(self.h_header[index])
        
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            if not self.v_header:
                return QtCore.QVariant("%s %s" % (self.trUtf8("Layer"), str(index + 1)))
            else:
                return QtCore.QVariant(self.v_header[index])
        
        return QtCore.QVariant()
            
    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            return QtCore.QVariant(self.cells[index.row()][index.column()])
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.QVariant(QtCore.Qt.AlignCenter)
        
        if self._row_is_totally_invalid(index.row()):
            if role == QtCore.Qt.BackgroundRole:
                background = QtGui.QBrush(QtGui.QColor("#FF0000"))
                background.setStyle(QtCore.Qt.BDiagPattern)
                return QtCore.QVariant(background)
            elif role == QtCore.Qt.ForegroundRole:
                foreground = QtGui.QBrush(QtGui.QColor("#000000"))
                return QtCore.QVariant(foreground)
        elif self._row_is_valid(index.row()):
            if role == QtCore.Qt.BackgroundRole:
                background = QtGui.QBrush(QtGui.QColor("#AADDAA"))
                background.setStyle(QtCore.Qt.BDiagPattern)
                return QtCore.QVariant(background)
            elif role == QtCore.Qt.ForegroundRole:
                foreground = QtGui.QBrush(QtGui.QColor("#000000"))
                return QtCore.QVariant(foreground)    
    
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid() and role == QtCore.Qt.EditRole:
            if index.column() == 0:
                self.cells[index.row()][index.column()] = QtCore.QVariant(value).toString()
            elif index.column() == 1:
                self.cells[index.row()][index.column()] = float(QtCore.QVariant(value).toString())
                
            self.dataChanged.emit(index, index)
            return True
        else:
            return False
        
    def append_empty_row(self):
        self.insert_blank_rows(self.rowCount(self), 1)
        self.cells.append([self.trUtf8("None"), 0.01])
        
    def _row_is_valid(self, position):
        return self.trUtf8("None") not in self.cells[position]
    
    def _row_is_totally_invalid(self, position):
        return QtCore.QString(u'') in self.cells[position] or None in self.cells[position]
    
    def data_is_valid(self):
        if self.rowCount(self) < 3:
            return False
        
        for row_num in xrange(self.rowCount(self)):
            if not self._row_is_valid(row_num) and row_num != self.rowCount(self) - 1:
                return False
            elif self._row_is_totally_invalid(row_num) and row_num != self.rowCount(self) - 1:
                return False
            
        return True
    
class MuDEditableTableModel(GenericEditableTableModelWithAutoColumnAppend):
    def __init__(self, cells=[], v_header=[], h_header=[], parent=None, *args):
        GenericEditableTableModelWithAutoColumnAppend.__init__(self, cells, v_header, h_header, parent)
        
        if not cells:
            self.cells = [[0, ]]
        else:
            self.append_empty_column()
            
    def data_is_valid(self):
        if not self.cells[0][::-1]:
            return False
        return True
            

class EEditableTableModel(GenericEditableTableModelWithAutoRowAppend):
    def __init__(self, cells=[], v_header=[], h_header=[], parent=None, *args):
        GenericEditableTableModelWithAutoRowAppend.__init__(self, cells, v_header, h_header, parent)
        
        if not cells:
            self.cells = [[0, ]]
        else:
            self.append_empty_row()
            

class DoseBuildUpFactorEditableTableModel(GenericEditableTableModelWithRowHighlight):
    def __init__(self, cells=[], v_header=[], h_header=[], parent=None, *args):
        GenericEditableTableModelWithRowHighlight.__init__(self, cells, v_header, h_header, parent)
        
    def _row_is_valid(self, position):
        return any(self.cells[position])
    
    def data_is_valid(self):
        """
        Valid:
            [
             [1, 1],
             ]
        
        Invalid:
            [
             [1, 0],
            ]
        """
        if self.rowCount(self) == 0:
            return False
    
        for row_num in xrange(self.rowCount(self)):
            if not self._row_is_valid(row_num):
                return False
            
        return True
        
        
class GammaSpectrumEditableTableModel(GenericEditableTableModelWithAutoRowAppend):
    def __init__(self, cells=[], v_header=[], h_header=[], parent=None, *args):
        GenericEditableTableModelWithAutoRowAppend.__init__(self, cells, v_header, h_header, parent)
        
        self.h_header = [
                         self.trUtf8("Energy (E, MeV)"),
                         self.trUtf8("Output (n, absolute value)"),
                         ]
        
        if not cells:
            self.cells = [[0, 0]]
        else:
            self.append_empty_row()
        
    def headerData(self, index, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if not self.h_header:
                return QtCore.QVariant("%s" % str(index + 1))
            else:
                return QtCore.QVariant(self.h_header[index])
        
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            if not self.v_header:
                return QtCore.QVariant("%s %s" % (self.trUtf8("Line"), str(index + 1)))
            else:
                return QtCore.QVariant(self.v_header[index])
        
        return QtCore.QVariant()


class MassAttenuationCoefficientEditableTableModel(GenericEditableTableModelWithAutoRowAppend):
    def __init__(self, cells=[], v_header=[], h_header=[], parent=None, *args):
        GenericEditableTableModelWithAutoRowAppend.__init__(self, cells, v_header, h_header, parent, args)
        
        self.h_header = [
                         self.trUtf8("x"),
                         self.trUtf8("f(x)"),
                         ]
        
        if not cells:
            self.cells = [[0, 0]]
        else:
            self.append_empty_row()
            

class GammaSpectrumTableModel(GenericTableModel):
    def __init__(self, cells, parent=None, *args):
        GenericTableModel.__init__(self, cells, v_header=[], h_header=[], parent=None, *args)
        
        self.h_header = [
                         self.trUtf8("Energy (E, MeV)"),
                         self.trUtf8("Output (n, absolute value)"),
                         ]
        
    def headerData(self, index, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if not self.h_header:
                return QtCore.QVariant("%s" % str(index + 1))
            else:
                return QtCore.QVariant(self.h_header[index])
        
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            if not self.v_header:
                return QtCore.QVariant("%s %s" % (self.trUtf8("Line"), str(index + 1)))
            else:
                return QtCore.QVariant(self.v_header[index])
    
        return QtCore.QVariant()
        

class MassAttenuationCoefficientTableModel(GenericTableModel):
    def __init__(self, cells, parent=None, *args):
        GenericTableModel.__init__(self, cells, v_header=[], h_header=[], parent=None, *args)
        
        self.h_header = [
                         self.trUtf8("x"),
                         self.trUtf8("f(x)"),
                         ]

        
class ExposureDoseRateTableModel(GenericTableModel):
    def __init__(self, cells, parent=None, *args):
        GenericTableModel.__init__(self, cells, v_header=[], h_header=[], parent=None, *args)
        
        self.h_header = [
                         self.trUtf8("Exposure dose rate, R/h"),
                         ]
        
    def headerData(self, index, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if not self.h_header:
                return QtCore.QVariant("%s" % str(index + 1))
            else:
                return QtCore.QVariant(self.h_header[index])
        
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            if not self.v_header:
                return QtCore.QVariant("%s %s" % (self.trUtf8("Line"), str(index + 1)))
            else:
                return QtCore.QVariant(self.v_header[index])
        
        return QtCore.QVariant()
    
    
class EmptyNuclideTableModel(GenericTableModel):
    def __init__(self, parent=None, *args):
        GenericTableModel.__init__(self, cells=[], v_header=[], h_header=[], parent=None, *args)
        self.cells = [[self.trUtf8("No entries found.")]]
        

class EmptyMaterialTableModel(GenericTableModel):
    def __init__(self, parent=None, *args):
        GenericTableModel.__init__(self, cells=[], v_header=[], h_header=[], parent=None, *args)
        self.cells = [[self.trUtf8("No entries found.")]]
        
        
class EmptyLayeredMaterialTableModel(GenericTableModel):
    def __init__(self, parent=None, *args):
        GenericTableModel.__init__(self, cells=[], v_header=[], h_header=[], parent=None, *args)
        self.cells = [[self.trUtf8("No entries found.")]]
