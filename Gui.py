import sys
from equations_util import *
from Equations import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QErrorMessage, QMessageBox
from PyQt5.uic import loadUi


class EquationSolverUi(QMainWindow):
    def __init__(self, *args):
        super(EquationSolverUi, self).__init__(*args)
        loadUi('part1.ui', self)
        self.method_list = [bisection, fixed_point, newton, newton_mod1, newton_mod2, regula_falsi, secant]
        self.solve_btn.clicked.connect(self.solve_eq)

    @staticmethod
    def extract_guesses(guesses):
        return [float(x) for x in str(guesses).strip().split(',')]

    @QtCore.pyqtSlot()
    def solve_eq(self):
        expr = iter = eps = guesses = None
        try:
            expr = string_to_expression(self.equ_line.text())
        except:
            self.show_error_message("Error: Invalid Equation Format")
            return
        try:
            iter = int(self.iter_line.text())
        except ValueError:
            self.show_error_message("Error: Invalid Maximum Iterations Format")
            return
        try:
            eps = float(self.eps_line.text())
        except ValueError:
            self.show_error_message("Error: Invalid Epsilon Format")
            return
        try:
            guesses = self.extract_guesses(self.guess_line.text())
        except:
            self.show_error_message("Error: Invalid 'Guesses' Format")
            return
        try:
            # Clear all tabs and clear table and plots.
            # For each method used, add a new tab with the name of the method and print the table in this tab.
            if self.method_select.currentText() == "All methods":
                for method in self.method_list:
                    method(expr, guesses, iter, eps)
            else:
                self.method_list[self.method_select.currentIndex()](expr, guesses, iter, eps)
        except Exception as e:
            self.show_error_message(str(e))
            return

    def show_error_message(self, msg):
        self.error_msg.setText(msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = EquationSolverUi()
    widget.show()
    sys.exit(app.exec_())
