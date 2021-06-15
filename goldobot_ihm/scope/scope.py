from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QDial
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QTabWidget

from PyQt5.QtCore import QTimer

#from widgets.plot_dialog import PlotDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.ticker
import numpy as np

from .channel_base import ChannelBase

scales = [
    (0.01, '10m'),
    (0.02, '20m'),
    (0.05, '50m'),
    (0.1, '100m'),
    (0.2, '200m'),
    (0.5, '500m'),
    (1, '1'),
    (2, '2'),
    (5, '5'),
    (10, '10'),
    (20, '20'),
    (50, '50'),
    (100, '100'),
    (200, '200'),
    (500, '500'),
    (1000, '1k'),
    (2000, '2k'),
    (5000, '5k'),
    (10000, '10k'),
    (20000, '20k'),
    ]

class ScaleSelectorWidget(QSpinBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setRange(0,len(scales) - 1)
        
    def textFromValue(self, value):
        return scales[value][1]
        
    def valueFromText(self, text):
        print('vft')
        
    @property
    def scale(self):
        return scales[self.value()][0]
        
    

class ScopeChannel(QWidget, ChannelBase):    
    def __init__(self, parent):
        #super(ChannelBase, self).__init__(parent._timebase)     
        super(QWidget, self).__init__(parent)           
        self._parent = parent
        self.timebase= self._parent._timebase
        self._axes = parent._scope_view._axes
        self._lines = self._axes.plot([],[], marker='.', linestyle='')[0]
        layout = QGridLayout()
        
        self._listbox_select_variable = QComboBox()
        self._checkbox_enable = QCheckBox()
        self._dial_offset = QDial(wrapping=True, minimum=0, maximum=100)
        self._spinbox_range = QSpinBox()
        self._scale_selector = ScaleSelectorWidget()
        
        layout.addWidget(self._listbox_select_variable,0,0) 
        layout.addWidget(self._checkbox_enable,1,0) 
        layout.addWidget(self._dial_offset,0,1) 
        layout.addWidget(self._scale_selector,0,2) 
        self.setLayout(layout)
        
        self._dial_offset.sliderMoved.connect(self._on_dial_offset_moved)
        self._scale_selector.valueChanged.connect(self._on_scale_value_changed)
        self._dial_offset_old = 0
        
        for v in self._parent.variables:
            self._listbox_select_variable.addItem(v)   
        self.update_scale(self._scale_selector.scale)  
        self.set_data([0,1,2,3], [0,1,-1,2])
        
    
    def _on_scale_value_changed(self, value):
        self.update_scale(self._scale_selector.scale)
        
    def _on_dial_offset_moved(self, val: int):
        diff = (val - self._dial_offset_old) % 100
        if diff > 50:
            diff -= 100
        self._dial_offset_old = val
        self.update_offset(self.offset + diff * 0.01 * self.scale)
        
    def update_display(self, x, y):
        self._lines.set_data(x, y)        
        #todo cleanup
        self._parent._scope_view._canvas.draw()
        
class ScopeTimeBase(QWidget):
    
    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent        
        layout = QGridLayout()
        self._listbox_select_variable = QComboBox()
        layout.addWidget(self._listbox_select_variable)        
        self.setLayout(layout)
        self.reference_timestamp = 5
        
        self.min_value = 0
        self.max_value = 10
        self.scale = 1
        self.time_per_div = 1
        
    def _on_scale(self):
        pass
        
    def _on_offset(self):
        pass
        
class ScopeView(QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # matplotlib graph
        self._figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self._canvas = FigureCanvas(self._figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self._toolbar = NavigationToolbar(self._canvas, self)
        
        layout = QVBoxLayout()
        #layout.addWidget(self._toolbar)
        layout.addWidget(self._canvas)
        self.setLayout(layout)
        
        self._axes = self._figure.add_subplot(111)
        
        self._axes.grid(True, 'major')

        self._axes.set_xlim(-5,5)
        self._axes.set_ylim(-5,5)
        
        self._axes.tick_params(which='both', top=True, bottom=True, left = True, right = True,
                                labeltop=False, labelbottom=False, labelleft=False, labelright=False)
                                
        self._axes.set_xticks([-5 + i for i in range(11)])
        self._axes.set_yticks([-5 + i for i in range(11)])
        
        self._axes.xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(5))
        self._axes.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(5))

        #self._figure.clf()
        self._axes.plot([-5,5], [   0,   0], '--k')
        plt = self._axes.plot([],[])[0]
        self._canvas.draw()
        
class ScopeDialog(QDialog):
    default_Kp_val = 4.0
    default_Ki_val = 0.0625
    default_Kd_val = 1.0
    default_range_val = 4095
    default_clamp_val = 448
    default_bltrig_val = 80
    default_goto_speed_val = 40
    
    
    @property
    def variables(self):
        return ['test', 'foo']
        
    def _update_data(self, channel, x, y):
        pass

    def __init__(self, parent = None):
        super().__init__(parent)

        # FIXME : TODO : parametrize
        self.fpga_cmd_reg = 0x80008500

        ctrl_layout = QGridLayout()

        li = 0

        self._button_enable = QPushButton('Enable')
        self._button_enable.setFixedWidth(100)
        ctrl_layout.addWidget(self._button_enable, li, 0)
        self._button_disable = QPushButton('Disable')
        self._button_disable.setFixedWidth(100)
        ctrl_layout.addWidget(self._button_disable, li, 1)
        self._button_reset_error = QPushButton('Reset\nError')
        self._button_reset_error.setFixedWidth(100)
        ctrl_layout.addWidget(self._button_reset_error, li, 2)
        li += 1

        # set the layout
        self._scope_view = ScopeView()
        
        #graph_layout = QVBoxLayout()
        #graph_layout.addWidget(self._toolbar)
        #graph_layout.addWidget(self._canvas)

        global_layout = QHBoxLayout()

        global_layout.addLayout(ctrl_layout)
        global_layout.addWidget(self._scope_view)

        self.setLayout(global_layout)
        
        self._timebase = ScopeTimeBase(self)
        self._channels = []
        
        channel = ScopeChannel(self)
        self._channels.append(channel)
        ctrl_layout.addWidget(channel)     
        

        self._button_enable.clicked.connect(lambda:self.cmd_generic("Enable",0x10000001))
        self._button_disable.clicked.connect(lambda:self.cmd_generic("Disable",0x10000000))
        self._button_reset_error.clicked.connect(lambda:self.cmd_generic("Reset error",0xf0000000))
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_timer)
        self._timer.start(20)
        self._ts = 0
        
    def _on_timer(self):        
        import math
        #x = np.array([self._ts + 0.001 * i for i in range(10)])
        #y = np.array([math.cos(t) for t in x])
        #self._ts += 0.01
        #self._timebase.reference_timestamp = self._ts - 5
        #self._channels[0].append_data(x,y)
        self._channels[0].refresh()
        
    def set_client(self, client):
        self._client = client
        self._client.registerCallback('main/propulsion/scope/values', self._on_scope_values)
        
    def _on_scope_values(self, msg):
        for i, channel in enumerate(msg.channels):
            print(len(msg.timestamps), len(channel.float_values) )
            self._channels[0].append_data(np.array(msg.timestamps), np.array(channel.float_values))
        self._timebase.reference_timestamp = max(msg.timestamps) - 5

    def _on_asserv_plot(self, ts, pos):
        print (" {} {}".format(ts, pos))
        if ((ts>0) and (ts<1000)):
            self._ts_plot.append(ts)
            self._pos_plot.append(pos)
        if ((ts>895) and (ts<905)):
            self._axes.plot(self._ts_plot, self._pos_plot, '-')
        self._canvas.draw()
        

