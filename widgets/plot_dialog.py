from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QGridLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class PlotDialog(QtWidgets.QWidget):
    def __init__(self,  parent=None):
        super(PlotDialog, self).__init__(parent)
        #self.resize(1200,400)

        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.axes = self.figure.add_subplot(111)     

        self.canvas.draw()

    def plot_curve(self,points):
        self.axes.plot(points, '*-')
        self.canvas.draw()
        
class ControlPlots(QtWidgets.QDialog):
    def __init__(self,  parent=None):
        super(ControlPlots, self).__init__(parent)
        tab_widget = QTabWidget()
        
        self.plot_translation = PlotDialog()
        tab_widget.addTab(self.plot_translation, "translation")
        
        self.plot_yaw = PlotDialog()
        tab_widget.addTab(self.plot_yaw, "yaw")
        
        self.plot_yaw_rate = PlotDialog()
        tab_widget.addTab(self.plot_yaw_rate, "yaw_rate")
        
        
        
        
        
        layout = QGridLayout()
        layout.addWidget(tab_widget)
        self.setLayout(layout)
        self.plot_yaw.plot_curve([0,2,1])
        self.plot_yaw.show()
