from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import  QTimer

from widgets.properties_editor import PropertiesEditorWidget
from widgets.table_view import TableViewWidget


import message_types

import struct
import math



class HalTestDialog(QDialog):


    def __init__(self, parent = None):
        super().__init__(parent)
        self._client = None
        
        layout = QGridLayout()
        #layout.addWidget(self._propulsion_enable_button,0,0)
        
        
        
        

        #gpio
        self._gpio_select_spinbox = QSpinBox()
        self._gpio_select_spinbox.setRange(0,31)
        
        self._gpio_checkbox = QCheckBox()
        
        self._gpio_get_button = QPushButton('Get')
        self._gpio_set_button = QPushButton('Set')        
        
        layout.addWidget(self._gpio_select_spinbox,0, 1)
        layout.addWidget(self._gpio_checkbox,0, 2)
        layout.addWidget(self._gpio_get_button,0, 3)
        layout.addWidget(self._gpio_set_button,0, 4)
        
        self._gpio_set_button.clicked.connect(self._gpio_set)
        
        # pwm
        self._pwm_select_spinbox = QSpinBox()
        self._pwm_select_spinbox.setRange(0,31)
        
        self._pwm_spinbox = QSpinBox()
        self._pwm_spinbox.setRange(-100,100)
        
        self._pwm_get_button = QPushButton('Get')
        self._pwm_set_button = QPushButton('Set')        
        
        layout.addWidget(self._pwm_select_spinbox,1, 1)
        layout.addWidget(self._pwm_spinbox,1, 2)
        layout.addWidget(self._pwm_get_button,1, 3)
        layout.addWidget(self._pwm_set_button,1, 4)   

        self._pwm_set_button.clicked.connect(self._pwm_set)        
      

        self.setLayout(layout)
        
        #self._propulsion_enable_button.clicked.connect(self._propulsion_enable)
       

    def set_client(self, client):
        self._client = client

    def _gpio_set(self):
        msg = struct.pack('<BB', self._gpio_select_spinbox.value(), self._gpio_checkbox.isChecked())
        self._client.send_message(501, msg)

    def _pwm_set(self):
        msg = struct.pack('<Bf', self._pwm_select_spinbox.value(), self._pwm_spinbox.value() * 0.01)
        self._client.send_message(502, msg)