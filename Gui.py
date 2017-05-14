import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi


class EquationSolverUi(QMainWindow):
    def __init__(self, *args):
        super(EquationSolverUi, self).__init__(*args)
        loadUi('part1.ui', self)
        self.solve_btn.clicked.connect(self.solve_eq)

    @QtCore.pyqtSlot()
    def solve_eq(self):
        print("SOLVING")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = EquationSolverUi()
    widget.show()
    sys.exit(app.exec_())
