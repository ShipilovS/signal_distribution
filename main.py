from PyQt5 import QtWidgets, QtCore
from destr import Ui_MainWindow
import matplotlib.pyplot as plt
from lib import *
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import sys
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

BTN = None

class ModelCanvas(FigureCanvas):
    def __init__(self, data, bins, new_sequence):
        fig, ax = plt.subplots(ncols=2, figsize=(10, 5))
        ax[0].hist(data, bins=bins)
        ax[0].set_title('Исходный сигнал')
        ax[0].grid()
        ax[1].hist(new_sequence, bins=bins)
        ax[1].set_title('Промоделированный сигнал')
        ax[1].grid()
        super(ModelCanvas, self).__init__(fig)


class TimeModelCanvas(FigureCanvas):
    def __init__(self, data, bins, new_sequence):
        fig, ax = plt.subplots(ncols=2, figsize=(10, 5))
        # ax[0].hist(new_sequence, bins=bins)
        # ax[0].set_title('Промоделированный сигнал')
        ax[0].plot(data)
        ax[0].set_title('Исходный сигнал')
        ax[0].grid()
        ax[1].plot(new_sequence)
        ax[1].set_title('Промоделированный сигнал')
        ax[1].grid()
        super(TimeModelCanvas, self).__init__(fig)

class Analyze2dModelCanvas(FigureCanvas):
    def __init__(self, x, y, new_sequence):
        fig = plt.figure(figsize=(10, 5))
        ax1 = fig.add_subplot(121, projection='3d')
        hist, xedges, yedges = np.histogram2d(x, y, bins=100)
        xpos, ypos = np.meshgrid(xedges[:-1] + xedges[1:], yedges[:-1] + yedges[1:])
        xpos = xpos.flatten() / 2.
        ypos = ypos.flatten() / 2.
        zpos = np.zeros_like(xpos)
        dx = xedges[1] - xedges[0]
        dy = yedges[1] - yedges[0]
        dz = hist.flatten()
        ax1.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')
        ax1.set_title('Исходный сигнал')

        ax2 = fig.add_subplot(122, projection='3d')
        hist, xedges, yedges = np.histogram2d(new_sequence[:-1], new_sequence[1:], bins=[100, 100])
        xpos, ypos = np.meshgrid(xedges[:-1] + xedges[1:], yedges[:-1] + yedges[1:])
        xpos = xpos.flatten() / 2.
        ypos = ypos.flatten() / 2.
        zpos = np.zeros_like(xpos)
        dx = xedges[1] - xedges[0]
        dy = yedges[1] - yedges[0]
        dz = hist.flatten()
        ax2.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')
        ax2.set_title('Промоделированный сигнал')
        plt.grid()
        super(Analyze2dModelCanvas, self).__init__(fig)

class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.radioButton.clicked.connect(self.check)
        self.pushButton.clicked.connect(self.analyze)
        self.pushButton_2.clicked.connect(self.clear)
        self.pushButton_3.clicked.connect(self.time_realize)
        self.pushButton_4.clicked.connect(self.analyze_2d)
        self.layout = QtWidgets.QVBoxLayout()

    def analyze(self):
        if self.radioButton.isChecked():
            data = init()
            bins, new_sequence = func(data)
        elif self.radioButton_2.isChecked():
            data = init_gamma()
            bins, new_sequence = func(data)
        elif self.radioButton_3.isChecked():
            data = init_norm()
            bins, new_sequence = func(data)


        # scene = QtWidgets.QGraphicsScene()
        # view = self.graphicsView
        # print(view)
        # canvas = FigureCanvas(fig)
        # proxy_widget = scene.addWidget(canvas)
        # view.show()
        # self.canvas.draw()
        # plt.show()
        
        sc = ModelCanvas(data, bins, new_sequence)
        toolbar = NavigationToolbar(sc, self)

        self.layout.addWidget(toolbar)
        self.layout.addWidget(sc)
   
        self.widget.setLayout(self.layout)
        self.show()

    def time_realize(self):
        if self.radioButton.isChecked():
            data = init(size=200)
            bins, new_sequence = func(data)
        elif self.radioButton_2.isChecked():
            data = init_gamma(size=200)
            bins, new_sequence = func(data)
        elif self.radioButton_3.isChecked():
            data = init_norm(size=200)
            bins, new_sequence = func(data)

        sc = TimeModelCanvas(data, bins, new_sequence)
        toolbar = NavigationToolbar(sc, self)

        self.layout.addWidget(toolbar)
        self.layout.addWidget(sc)
   
        self.widget.setLayout(self.layout)
        self.show()

    def analyze_2d(self):
        num_samples = 100000
        shape = 1.5
        loc = 0
        scale = 1
        if self.radioButton.isChecked():
            x, y = nakagami.rvs(shape, loc, scale, size=(num_samples, 2)).T
            transition_matrix, bins = create_markov_chain_2d(np.concatenate((x, y)))
            new_sequence = generate_sequence_2d(transition_matrix, bins, length=num_samples)
        elif self.radioButton_2.isChecked():
            x, y = gamma.rvs(shape, loc, scale, size=(num_samples, 2)).T
            transition_matrix, bins = create_markov_chain_2d(np.concatenate((x, y)))
            new_sequence = generate_sequence_2d(transition_matrix, bins, length=num_samples)
        elif self.radioButton_3.isChecked():
            x, y = norm.rvs(size=(num_samples, 2)).T
            transition_matrix, bins = create_markov_chain_2d(np.concatenate((x, y)))
            new_sequence = generate_sequence_2d(transition_matrix, bins, length=num_samples)

        sc = Analyze2dModelCanvas(x, y, new_sequence)
        toolbar = NavigationToolbar(sc, self)

        self.layout.addWidget(toolbar)
        self.layout.addWidget(sc)

        self.widget.setLayout(self.layout)
        self.show()
       

        
    def clear(self):
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().deleteLater()
            # self.layout.itemAt(i).widget().setParent(None)

app = QtWidgets.QApplication(sys.argv) 
window = ExampleApp()  
window.show() 
app.exec_() 