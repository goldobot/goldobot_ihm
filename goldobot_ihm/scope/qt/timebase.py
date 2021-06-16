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

from .scale_selector import ScaleSelectorWidget
from .offset_dial import OffsetDial

class TimeBase(QWidget):
    
    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent        
        layout = QGridLayout()
        
        self._dial_offset = OffsetDial()
        self._scale_selector = ScaleSelectorWidget()    
        self._button_pause = QPushButton('pause', checkable=True)
        
        layout.addWidget(self._dial_offset,0,0, 2, 1)
        layout.addWidget(self._scale_selector,0,1)
        layout.addWidget(self._button_pause,0,2)
        
        self.setLayout(layout)
        self.max_timestamp = 0
        self.reference_timestamp = 5
        
        self.min_value = 0
        self.max_value = 10
        self.scale = 1
        self.offset = 0
        self.time_per_div = 1
        self.state = 'running'
        
        self._dial_offset.offsetChanged.connect(self.update_offset)
        self._scale_selector.valueChanged.connect(self._on_scale_value_changed)
        self._button_pause.toggled.connect(self._on_button_pause_toggled)
        
    def update_offset(self, offset):
        self.offset = offset
        
    def _on_scale_value_changed(self, value):
        self.time_per_div = self._scale_selector.scale
        self._dial_offset.scale = self.time_per_div
        
    def _on_button_pause_toggled(self, checked):
        if checked:
            self.state = 'paused'
            self._button_pause.setText('run')
        else:
            self.state = 'running'
            self._button_pause.setText('stop')
        
    def _on_offset(self):
        pass