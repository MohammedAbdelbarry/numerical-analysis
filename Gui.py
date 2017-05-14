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
        self.method_list = [self.exec_bisection, self.exec_fixed_point, self.exec_newton,
                            self.exec_newton_mod1, self.exec_newton_mod2, self.exec_regula_falsi, self.exec_secant]
        self.solve_btn.clicked.connect(self.solve_eq)

    @staticmethod
    def extract_guesses(guesses):
        return [float(guesses.strip()) for x in guesses.split(',')]

    @QtCore.pyqtSlot()
    def solve_eq(self):
        func = iter = eps = guesses = None
        try:
            func = string_to_lambda(self.equ_line.text())
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
            if self.method_select.currentText() == "All methods":
                for method in self.method_list:
                    method(func, iter, eps, guesses)
            else:
                self.method_list[self.method_select.currentIndex()](func, iter, eps, guesses)
        except ValueError as e:
            print(e)

    @staticmethod
    def exec_bisection(f, iter, eps, guesses):
        if len(guesses) != 2:
            raise RuntimeError("There needs to be two guesses")
        bisection(f, guesses[0], guesses[1], eps, iter)

    @staticmethod
    def exec_fixed_point(f, iter, eps, guesses):
        if len(guesses) != 1:
            raise RuntimeError("There needs to be one guess")
        fixed_point(f, guesses[0], eps, iter)

    def exec_newton(self, f, iter, eps, guesses):
        pass

    def exec_newton_mod1(self, f, iter, eps, guesses):
        pass

    def exec_newton_mod2(self, f, iter, eps, guesses):
        pass

    def exec_regula_falsi(self, f, iter, eps, guesses):
        pass

    def exec_secant(self, f, iter, eps, guesses):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = EquationSolverUi()
    widget.show()
    sys.exit(app.exec_())
