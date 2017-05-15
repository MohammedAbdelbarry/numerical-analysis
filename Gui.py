import sys
from equations_util import *
from Equations import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QErrorMessage, QMessageBox, QWidget, QFormLayout, QTableView, \
    QVBoxLayout, QLineEdit, QLabel
from PyQt5.uic import loadUi


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


class EquationSolverUi(QMainWindow):
    def __init__(self, *args):
        super(EquationSolverUi, self).__init__(*args)
        loadUi('part1.ui', self)
        self.method_list = [bisection, fixed_point, newton, newton_mod1,
                            newton_mod2, regula_falsi, secant, birge_vieta]
        self.solve_btn.clicked.connect(self.solve_eq)

    @staticmethod
    def extract_guesses(guesses):
        return [float(x.strip()) for x in str(guesses).strip().split(',')]

    @QtCore.pyqtSlot()
    def solve_eq(self):
        self.clear()
        expr = iter = eps = guesses = None
        try:
            expr = string_to_expression(self.equ_line.text())
        except:
            self.show_error_msg("Error: Invalid Equation Format")
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
            guesses = self.extract_guesses(self.guess_line.text())
        except:
            self.show_error_msg("Error: Invalid 'Guesses' Format")
            return
        try:
            if self.method_select.currentText() == "All methods":
                for method in self.method_list:
                    out = method(expr, guesses, eps, iter)
                    if len(out.dataframes > 1):
                        for i in range(0, len(out.dataframes)):
                            self.tabWidget_2.addTab(self._setup_tab(out, i), out.title + " " + str(i + 1))
                    else:
                        self.tabWidget_2.addTab(self._setup_tab(out), out.title)
            else:
                out = self.method_list[self.method_select.currentIndex()](expr, guesses, eps, iter)
                if len(out.dataframes) > 1:
                    for i in range(0, len(out.dataframes)):
                        self.tabWidget_2.addTab(self._setup_tab(out, i), out.title + " " + str(i + 1))
                else:
                    self.tabWidget_2.addTab(self._setup_tab(out), out.title)
        except Exception as e:
            self.show_error_msg(str(e))

    def show_error_msg(self, msg):
        self.error_msg.setText(msg)

    @staticmethod
    def _setup_tab(out: Output, index=None):
        new_tab = QWidget()
        layout = QVBoxLayout()
        view = QTableView()
        model = PandasModel(out.dataframes[0])
        root_label = QLabel()
        root_label.setText("Root: " + str(out.roots[0]))
        error_label = QLabel()
        error_label.setText("Error: " + str(out.errors[0]))
        exec_time_label = QLabel()
        exec_time_label.setText("Execution Time: " + str(out.execution_time))
        if index is not None:
            model = PandasModel(out.dataframes[index])
            root_label.setText("Root: " + str(out.roots[index]))
            error_label.setText("Error: " + str(out.errors[index]))
        view.setModel(model)
        layout.addWidget(view)
        layout.addWidget(root_label)
        layout.addWidget(error_label)
        layout.addWidget(exec_time_label)
        new_tab.setLayout(layout)
        return new_tab

    def clear(self):
        self.error_msg.setText("")
        self.tabWidget.clear()
        self.tabWidget_2.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = EquationSolverUi()
    widget.show()
    sys.exit(app.exec_())
