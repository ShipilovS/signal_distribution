from PyQt5 import QtWidgets, QtCore
from destr import Ui_MainWindow
import matplotlib.pyplot as plt
from lib import *
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import sys

BTN = None
 
class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.radioButton.clicked.connect(self.check)
        self.pushButton.clicked.connect(self.analyze)


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

        fig, ax = plt.subplots(ncols=2, figsize=(10, 4))
        ax[0].hist(data, bins=bins)
        ax[0].set_title('Original Signal')
        ax[1].hist(new_sequence, bins=bins)
        ax[1].set_title('Modeled Signal')
        plt.show()



app = QtWidgets.QApplication(sys.argv) 
window = ExampleApp()  
window.show() 
app.exec_() 