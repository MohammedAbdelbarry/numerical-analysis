import sys
from equations_util import *
from Equations import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QErrorMessage, QMessageBox, QWidget, QFormLayout, QTableView
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
        self.method_list = [self.exec_bisection, self.exec_fixed_point, self.exec_newton,
                            self.exec_newton_mod1, self.exec_newton_mod2, self.exec_regula_falsi,
                            self.exec_secant, self.exec_birge_vieta]
        self.solve_btn.clicked.connect(self.solve_eq)

    @staticmethod
    def extract_guesses(guesses):
        return [float(x.strip()) for x in str(guesses).strip().split(',')]

    @QtCore.pyqtSlot()
    def solve_eq(self):
        expr = iter = eps = guesses = None
        try:
            expr = string_to_expression(self.equ_line.text())
        except:
            print("Equation is invalid bruh")
            return
        try:
            iter = int(self.iter_line.text())
        except ValueError:
            print("Max iterations are invalid you lil' piece of shit")
            return
        try:
            eps = float(self.eps_line.text())
        except ValueError:
            print("Epsilon is invalid you ugly shite")
            return
        try:
            guesses = self.extract_guesses(self.guess_line.text())
        except:
            print("Your guesses are incorrect you fucking asshole")
            return
        try:
            # Clear all tabs and clear table and plots.
            self.tabWidget_2.clear()
            if self.method_select.currentText() == "All methods":
                for method in self.method_list:
                    new_tab, tab_name = method(expr, iter, eps, guesses)
                    self.tabWidget_2.addTab(new_tab, tab_name)
            else:
                new_tab, tab_name = self.method_list[self.method_select.currentIndex()](expr, iter, eps, guesses)
                self.tabWidget_2.addTab(new_tab, tab_name)
        except ValueError as e:
            print(e)

    @staticmethod
    def exec_bisection(expr, iter, eps, guesses):
        if len(guesses) != 2:
            raise RuntimeError("There needs to be two guesses")
        out = bisection(expr, guesses, eps, iter)
        # print("Bisection Selected Successfully!")
        return _setup_tab(out), out.title

    @staticmethod
    def exec_fixed_point(expr, iter, eps, guesses):
        if len(guesses) != 1:
            raise RuntimeError("There needs to be one guess")
        out = fixed_point(expr, guesses, eps, iter)
        return _setup_tab(out), out.title

    @staticmethod
    def exec_newton(expr, iter, eps, guesses):
        out = newton(expr, guesses, eps, iter)
        return _setup_tab(out), out.title

    @staticmethod
    def exec_newton_mod1(expr, iter, eps, guesses):
        out = newton_mod1(expr, guesses, eps, iter)
        return _setup_tab(out), out.title

    @staticmethod
    def exec_newton_mod2(expr, iter, eps, guesses):
        out = newton_mod2(expr, guesses, eps, iter)
        return _setup_tab(out), out.title

    @staticmethod
    def exec_regula_falsi(expr, iter, eps, guesses):
        out = regula_falsi(expr, guesses, eps, iter)
        return _setup_tab(out), out.title

    @staticmethod
    def exec_secant(expr, iter, eps, guesses):
        out = secant(expr, guesses, eps, iter)
        return _setup_tab(out), out.title

    @staticmethod
    def exec_birge_vieta(expr, iter, eps, guesses):
        out = birge_vieta(expr, iter, eps, guesses)
        return _setup_tab(out), out.title


def _setup_tab(out : Output):
    new_tab = QWidget()
    layout = QFormLayout()
    view = QTableView()
    model = PandasModel(out.dataframes[0])
    view.setModel(model)
    layout.addWidget(view)
    new_tab.setLayout(layout)
    return new_tab


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = EquationSolverUi()
    widget.show()
    sys.exit(app.exec_())