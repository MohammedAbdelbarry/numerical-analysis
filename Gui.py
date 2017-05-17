import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from pandas import DataFrame
from Equations import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QErrorMessage,
                             QMessageBox, QWidget, QFormLayout, QTableView, QVBoxLayout, QLineEdit, QLabel, QFileDialog)
from PyQt5.uic import loadUi
import os.path
from bisect import bisect_left

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
                            newton_mod2, regula_falsi, secant, birge_vieta, illinois]
        self.solve_btn.clicked.connect(self.solve_eq)
        self.func_plot = self.error_plot = None
        self.figs = [[plt.figure(0), self.func_plot, self.func_tab], [plt.figure(1), self.error_plot, self.error_tab]]
        self.tabWidget_2.currentChanged.connect(self.tab_changed)
        self.outs = []
        self.indices = [0]
        self.func_canvas = self.error_canvas = None
        self.render_figs()
        self.actionLoad_File.triggered.connect(self.load_file)
        self.actionSave_File.triggered.connect(self.save_file)

    def render_figs(self):
        canvases = []
        for i, (fig, plot, tab) in enumerate(self.figs):
            self.figs[i][1] = fig.add_subplot(111)
            self.figs[i][1].grid(True)
            canvas = FigureCanvas(fig)
            layout = QVBoxLayout()
            layout.addWidget(canvas)
            toolbar = NavigationToolbar(canvas, tab, coordinates=True)
            layout.addWidget(toolbar)
            tab.setLayout(layout)
            canvases.append(canvas)
            canvas.draw()
        self.func_plot = self.figs[0][1]
        self.error_plot = self.figs[1][1]
        self.func_canvas, self.error_canvas = canvases[0], canvases[1]

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
                counter = 0
                for method in self.method_list:
                    out = method(expr, guesses, eps, iter)
                    self.outs.append(out)
                    self.update_plots(out)
                    self.indices.append(self.indices[counter] + len(out.dataframes))
                    counter += 1
                    if len(out.dataframes > 1):
                        for i in range(0, len(out.dataframes)):
                            self.tabWidget_2.addTab(self._setup_tab(out, i), out.title + " " + str(i + 1))
                    else:
                        self.tabWidget_2.addTab(self._setup_tab(out), out.title)
            else:
                out = self.method_list[self.method_select.currentIndex()](expr, guesses, eps, iter)
                self.indices.append(self.indices[0] + len(out.dataframes))
                self.outs.append(out)
                self.update_plots(out)
                if len(out.dataframes) > 1:
                    for i in range(0, len(out.dataframes)):
                        self.tabWidget_2.addTab(self._setup_tab(out, i), out.title + " " + str(i + 1))
                else:
                    self.tabWidget_2.addTab(self._setup_tab(out), out.title)
        except Exception as e:
            self.show_error_msg(str(e))

    def show_error_msg(self, msg):
        self.error_msg.setText(msg)

    def update_plots(self, out):
        x = numpy.arange(-20, 20, 0.1)
        self.func_plot.clear()
        self.func_plot.grid(True)
        self.func_plot.plot(x, [out.function(z) for z in x], 'r', label="f")
        self.func_plot.plot(x, [out.boundary_function(z) for z in x], 'g', label="g")
        self.func_plot.legend(["Function", "Boundary Function"])
        self.func_canvas.draw()

    @staticmethod
    def _setup_tab(out: Output, index=None):
        new_tab = QWidget()
        vbox_layout = QVBoxLayout()
        form_layout = QFormLayout()
        view = QTableView()

        model = PandasModel(out.dataframes[0])
        root_label = QLabel()
        root_label.setText("Root: " + str(out.roots[0]))
        error_label = QLabel()
        error_label.setText("Error: " + str(out.errors[0]))
        exec_time_label = QLabel()
        exec_time_label.setText("Execution Time: " + str(out.execution_time))
        error_bound_label = QLabel()
        error_bound_label.setText("Error bound: " + str(out.error_bound))
        if index is not None:
            model = PandasModel(out.dataframes[index])
            root_label.setText("Root: " + str(out.roots[index]))
            error_label.setText("Error: " + str(out.errors[index]))

        form_layout.addWidget(root_label)
        form_layout.addWidget(error_label)
        form_layout.addWidget(exec_time_label)
        form_layout.addWidget(error_bound_label)

        view.setModel(model)
        vbox_layout.addWidget(view)
        vbox_layout.addLayout(form_layout)
        new_tab.setLayout(vbox_layout)
        return new_tab

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
                    parts[1] = '='.join(parts[1: ])
                    inp[parts[0].strip()] = parts[1].strip()
            if 'f' in inp:
                self.equ_line.setText(inp['f'])
            if 'max_err' in inp:
                self.eps_line.setText(inp['max_err'])
            if 'max_iter' in inp:
                self.iter_line.setText(inp['max_iter'])
            if 'arguments' in inp:
                self.guess_line.setText(inp['arguments'])
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

    def tab_changed(self, index):
        self.error_plot.clear()
        if self.outs is None:
            return
        i = bisect_left(self.indices, index)
        if i:
            i -= 1
        print(i, index)
        self.outs[i].dataframes[index - self.indices[i]].plot(grid=True,
         title=self.outs[i].title, ax=self.error_plot)  # , ax=self.error_plot
        self.error_canvas.draw()
        print(self.outs[i].error_bound)

    def clear(self):
        self.error_msg.setText("")
        self.outs = []
        self.indices = [0]
        self.error_plot.clear()
        self.func_plot.clear()
        self.error_canvas.draw()
        self.func_canvas.draw()
        self.tabWidget_2.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = EquationSolverUi()
    widget.show()
    sys.exit(app.exec_())
