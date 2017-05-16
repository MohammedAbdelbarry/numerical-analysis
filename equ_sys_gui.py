import sys
from EquSys import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QErrorMessage,
                             QMessageBox, QWidget, QFormLayout, QTableView, QVBoxLayout, QLineEdit, QLabel)
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

    @staticmethod
    def extract_equations(equations):
        eqs = equations.splitlines()
        # validate
        return eqs

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
                        out = self.method_list[i](aug_mat, symb_list, max_iter = iter, max_err = eps)
                    self.table_tab_widget.addTab(self._setup_tab(out), out.title)
            else:
                if self.method_select.currentIndex() < 3:
                    out = self.method_list[self.method_select.currentIndex()](aug_mat, symb_list)
                else:
                    out = self.method_list[self.method_select.currentIndex()](aug_mat, symb_list, max_iter = iter, max_err = eps)
                self.table_tab_widget.addTab(self._setup_tab(out), out.title)
        except Exception as e:
            self.show_error_msg(str(e))

    def show_error_msg(self, msg):
        self.error_msg.setText(msg)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = LinearEquationsSolver()
    widget.show()
    sys.exit(app.exec_())
