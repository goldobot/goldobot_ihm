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
from PyQt5.QtWidgets import QStackedWidget 

from PyQt5.QtCore import QTimer

#from widgets.plot_dialog import PlotDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.ticker
import matplotlib.style
import numpy as np

from .qt.channel import Channel
from .qt.timebase import TimeBase

import google.protobuf as _pb
_sym_db = _pb.symbol_database.Default()

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
        layout.addWidget(self._toolbar)
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
        
        
propulsion_variables = [
    '',
    'pose.x',
    'pose.y',
    'pose.yaw',
    'pose.speed',
    'pose.yaw_rate',
    'pose.acceleration',
    'target.x',
    'target.y',
    'target.yaw',
    'target.speed',
    'target.yaw_rate',
    'target.acceleration',
    'low_level.longi_error',
    'low_lewel.yaw_error',
    'low_level.speed_error',
    'low_level.yaw_rate_error',
    'motor0.vel_setpoint',
    'motor1.vel_setpoint',
    'odrive.axis0.vel_estimate',
    'odrive.axis1.vel_estimate',
    'odrive.axis0.current_iq_setpoint',
    'odrive.axis1.current_iq_setpoint',
    'odrive.vbus',  
    'odrive.ibus', 
    'encoders.left_counts',
    'encoders.right_counts',
    'blocking_detector.speed_estimate',
    'blocking_detector.force_estimate',
    'blocking_detector.left_slip_speed',
    'blocking_detector.right_slip_speed'
    ]
    
propulsion_variables_dict = {v:i for i, v in enumerate(propulsion_variables)}

class ScopeDialog(QDialog):
    
    @property
    def variables(self):
        return propulsion_variables
        
    def _update_data(self, channel, x, y):
        pass

    def __init__(self, parent = None):
        super().__init__(parent)

        ctrl_layout = QVBoxLayout()

        # set the layout
        with matplotlib.style.context('bmh'):
            self._scope_view = ScopeView()        

            global_layout = QHBoxLayout()

            global_layout.addLayout(ctrl_layout)
            global_layout.addWidget(self._scope_view)

            self.setLayout(global_layout)
            
            self._timebase = TimeBase(self)
            ctrl_layout.addWidget(self._timebase)
            self._channels = []
            
            for i in range(4):
                channel = Channel(self, i , name='{}'.format(i+1))
                self._channels.append(channel)
                ctrl_layout.addWidget(channel)
                channel.variableChanged.connect((lambda n: lambda variable: self._on_channel_variable_changed(n, variable))(i))
                channel.scaleChanged.connect(self._update_config)
            ctrl_layout.addStretch(1) 

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_timer)
        self._timer.start(20)
        self._ts = 0
        
    def _update_config(self):
        msg = _sym_db.GetSymbol('goldo.nucleo.ScopeConfig')(period=10)
        for channel in self._channels:        
            if channel.variable != '':
                chan_msg = _sym_db.GetSymbol('goldo.nucleo.ScopeChannelConfig')(
                    variable = propulsion_variables_dict[channel.variable],
                    encoding = 4,
                    min_value=channel.lim_min,
                    max_value=channel.lim_max)                    
                msg.channels.append(chan_msg) 
        self._client.publishTopic('nucleo/in/propulsion/scope/config/set', msg)
        
    def _on_timer(self):        
        import math
        #x = np.array([self._ts + 0.001 * i for i in range(10)])
        #y = np.array([math.cos(t) for t in x])
        #self._ts += 0.01
        #self._timebase.reference_timestamp = self._ts - 5
        #self._channels[0].append_data(x,y)
        if self._timebase.state == 'running':
            self._timebase.reference_timestamp = self._timebase.max_timestamp - 5 * self._timebase.time_per_div
        for channel in self._channels:
            channel.refresh()
        self._scope_view._canvas.draw()
        
    def set_client(self, client):
        self._client = client
        self._client.registerCallback('main/propulsion/scope/values', self._on_scope_values)
        
    def _on_channel_variable_changed(self, i, variable):
        self._update_config()
        
    def _on_scope_values(self, msg):
        for i, channel in enumerate(msg.channels):
            self._channels[i].append_data(np.array(msg.timestamps), np.array(channel.float_values))
        self._timebase.max_timestamp = max(msg.timestamps)        

    def _on_asserv_plot(self, ts, pos):
        print (" {} {}".format(ts, pos))
        if ((ts>0) and (ts<1000)):
            self._ts_plot.append(ts)
            self._pos_plot.append(pos)
        if ((ts>895) and (ts<905)):
            self._axes.plot(self._ts_plot, self._pos_plot, '-')
        self._canvas.draw()
        

