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

        self._axes = []
        self._axes.append(self.figure.add_subplot(411))
        self._axes.append(self.figure.add_subplot(412))
        self._axes.append(self.figure.add_subplot(413))
        self._axes.append(self.figure.add_subplot(414))

        # discards the old graph
        #self._ax.clear()

        # plot data
        #ax.plot(data, '*-')

        self.canvas.draw()

    def plot_curve(self,idx, points):
        self._axes[idx].plot(points, '*-')
        self.canvas.draw()
