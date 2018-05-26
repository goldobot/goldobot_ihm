from PyQt5 import QtCore, QtGui, QtWidgets


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class PlotDialog(QtWidgets.QDialog):
    def __init__(self,  parent=None):
        super(PlotDialog, self).__init__(parent)
        self.resize(1200,400)

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

        self._ax = self.figure.add_subplot(211)
        self._ax2 = self.figure.add_subplot(212)

        # discards the old graph
        self._ax.clear()

        # plot data
        #ax.plot(data, '*-')

        self.canvas.draw()

    def plot_curve(self,idx, points):
        if idx == 0:
            self._ax.plot(points, '*-')
        if idx == 1:
            self._ax2.plot(points, '*-')
        self.canvas.draw()
