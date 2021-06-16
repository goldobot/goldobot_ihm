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


from PyQt5.QtCore import pyqtSignal, QObject


import matplotlib.ticker
import numpy as np

from ..channel_base import ChannelBase
from .scale_selector import ScaleSelectorWidget
from .offset_dial import OffsetDial


    
channel_colors = [
    'yellow',
    'cyan',
    'magenta',
    'green'
    ]

class Channel(QWidget, ChannelBase):
    variableChanged = pyqtSignal(str)
    scaleChanged = pyqtSignal(float)
    
    def __init__(self, parent, index, *, name = ''):
        super(QWidget, self).__init__(parent)
        self._name = name
        self._index = index
        self._parent = parent
        self.timebase= self._parent._timebase
        self._axes = parent._scope_view._axes
        foo = self._axes.plot([],[], marker='.', linestyle='')
        self._lines = self._axes.plot([],[], marker='.', linestyle='')[0]
        self._lines.set_color(channel_colors[index])
        layout = QGridLayout()

        self._listbox_select_variable = QComboBox()
        self._checkbox_enable = QCheckBox()
        self._dial_offset = OffsetDial()
        self._scale_selector = ScaleSelectorWidget()

        layout.addWidget(self._listbox_select_variable,0,0)
        layout.addWidget(self._checkbox_enable,1,0)
        layout.addWidget(self._dial_offset,0,1, 2, 1)
        layout.addWidget(self._scale_selector,0,2)
        self.setLayout(layout)

        self._dial_offset.offsetChanged.connect(self.update_offset)
        self._scale_selector.valueChanged.connect(self._on_scale_value_changed)
        self._listbox_select_variable.currentTextChanged.connect(self._on_variable_current_text_changed)

        for v in self._parent.variables:
            self._listbox_select_variable.addItem(v)
        self._variable = self._parent.variables[0]
        
        self.update_scale(self._scale_selector.scale)

    def _on_variable_current_text_changed(self, text):
        self.variable = text
        self.variableChanged.emit(text)
        
    def _on_scale_value_changed(self, value):        
        self.update_scale(self._scale_selector.scale)
        self._dial_offset.scale = self.scale
        self.scaleChanged.emit(self.scale)

    def update_display(self, x, y):
        self._lines.set_data(x, y)
        #todo cleanup
        