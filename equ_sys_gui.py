import sys
import os.path

from EquSys import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QMessageBox, QWidget, QFormLayout, QTableView, QVBoxLayout, QLineEdit, QLabel, QFileDialog)
from PyQt5.uic import loadUi

from equations_util import equations_to_aug_matrix


class PandasModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """

    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1] + 1

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                if index.column() == 0:
                    return index.row() + 1
                return str(self._data.iloc[index.row(), index.column() - 1])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if col == 0:
                return 'i'
            return self._data.columns[col - 1]
        return None


class LinearEquationsSolver(QMainWindow):
    def __init__(self, *args):
        super(LinearEquationsSolver, self).__init__(*args)
        loadUi('part2.ui', self)
        self.method_list = [gauss, gauss_jordan, lu_decomp, gauss_seidel, jacobi]
        self.solve_btn.clicked.connect(self.solve_linear_eqs)
        self.outs = []
        self.actionLoad_File.triggered.connect(self.load_file)
        self.actionSave_File.triggered.connect(self.save_file)
        self.actionExit.triggered.connect(self.exit)

    @staticmethod
    def extract_equations(equations):
        return [x.strip() for x in str(equations).strip().splitlines()]

    @QtCore.pyqtSlot()
    def solve_linear_eqs(self):
        self.clear()
        eqs = iter = eps = None
        try:
            eqs = self.extract_equations(self.equations_text.toPlainText())
        except:
            self.show_error_msg("Error: Invalid Equations Format")
            return
        try:
            iter = int(self.iter_line.text())
        except ValueError:
            self.show_error_msg("Error: Invalid Maximum Iterations Format")
            return
        try:
            eps = float(self.eps_line.text())
        except ValueError:
            self.show_error_msg("Error: Invalid Epsilon Format")
            return
        try:
            aug_mat, symb_list = equations_to_aug_matrix(eqs)
            if self.method_select.currentText() == "All methods":
                for i in range(len(self.method_list)):
                    if i < 3:
                        out = self.method_list[i](aug_mat, symb_list)
                    else:
                        out = self.method_list[i](aug_mat, symb_list, max_iter=iter, max_err=eps)
                    self.outs.append(out)
                    self.table_tab_widget.addTab(self._setup_tab(out), out.title)
            else:
                if self.method_select.currentIndex() < 3:
                    out = self.method_list[self.method_select.currentIndex()](aug_mat, symb_list)
                else:
                    out = self.method_list[self.method_select.currentIndex()](aug_mat, symb_list, max_iter=iter,
                                                                              max_err=eps)
                self.outs.append(out)
                self.table_tab_widget.addTab(self._setup_tab(out), out.title)
        except Exception as e:
            self.show_error_msg(str(e))

    def show_error_msg(self, msg):
        self.error_msg.setText(msg)

    def load_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file')
        data = None
        inp = {}
        if fname[0]:
            with open(fname[0], 'r') as f:
                data = f.read()
                for line in data.strip().splitlines():
                    parts = line.strip().replace('==', '=').split('=')
                    if len(parts) < 2:
                        continue
                    parts[1] = '='.join(parts[1:])
                    inp[parts[0].strip()] = parts[1].strip()
            if 'equ' in inp:
                equs = [x.strip() for x in inp['equ'].strip().split(',')]
                self.equations_text.clear()
                for eq in equs:
                    self.equations_text.append(eq)
            if 'max_err' in inp:
                self.eps_line.setText(inp['max_err'])
            if 'max_iter' in inp:
                self.iter_line.setText(inp['max_iter'])
            if 'method_name' in inp:
                index = self.method_select.findText(inp['method_name'], QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.method_select.setCurrentIndex(index)

    def save_file(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if fname[0]:
            for out in self.outs:
                for i in range(len(out.dataframes)):
                    out.dataframes[i].to_csv(path_or_buf=os.path.join(fname,
                                                                      out.title + str(i + 1) + '.csv'))

    def exit(self):
        sys.exit(app.exec_())

    @staticmethod
    def _setup_tab(out: Output):
        new_tab = QWidget()
        vbox_layout = QVBoxLayout()
        form_layout = QFormLayout()
        view = QTableView()

        model = PandasModel(out.dataframes[0])
        exec_time_label = QLabel()
        exec_time_label.setText("Execution Time: " + str(out.execution_time))

        form_layout.addWidget(exec_time_label)

        view.setModel(model)
        vbox_layout.addWidget(view)
        vbox_layout.addLayout(form_layout)
        new_tab.setLayout(vbox_layout)
        return new_tab

    def clear(self):
        self.error_msg.setText("")
        self.table_tab_widget.clear()
        self.outs = []


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = LinearEquationsSolver()
    widget.show()
    sys.exit(app.exec_())
