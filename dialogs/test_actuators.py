from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTabWidget

from widgets.properties_editor import PropertiesEditorWidget

import struct
import message_types

import struct
import math

class ActuatorValuesWidget(QWidget):
    def __init__(self, actuators):
        super(ActuatorValuesWidget, self).__init__()
        self._widgets = {}
        self._actuators = actuators
        layout = QGridLayout()

        layout.addWidget(QLabel('PWM'), 0, 1)
        layout.addWidget(QLabel('Value'), 0, 2)

        i = 1
        for k, id_ in actuators:
            duty_cycle_value = QSpinBox()
            duty_cycle_value.setRange(0, 0x40000)
            current_value = QLineEdit()
            current_value.setReadOnly(True)

            layout.addWidget(QLabel(k), i, 0)
            layout.addWidget(duty_cycle_value, i, 1)
            layout.addWidget(current_value, i, 2)
            self._widgets[id_] = (duty_cycle_value, current_value)
            i += 1

        self._button_read_state = QPushButton('Lecture')
        self._button_send_state = QPushButton('Ecriture')
        layout.addWidget(self._button_read_state, i, 0)
        layout.addWidget(self._button_send_state, i, 1)

        self.setLayout(layout)

        self._button_read_state.clicked.connect(self._read_actuators)
        self._button_send_state.clicked.connect(self._send_data)


# Creation des fonctions vides qui, pour l'instant, ne renvoient rien.
    def _read_actuators(self):
        pass

    def _send_data(self, id_):
        print('send data')
        for k, id_ in self._actuators:
            self._client.send_message(message_types.FpgaCmdServo,
            struct.pack('<BH', id_, self._widgets[id_][0].value()))
            

class TestActuatorsDialog(QDialog):
    def __init__(self, parent = None):
        super(TestActuatorsDialog, self).__init__(None)
        self._client = None
        self._button = QPushButton('set actuator')
        self._servo_values = ActuatorValuesWidget([
            ('avant droit:', 1),
            ('avant gauche :', 2),
            ('chargeur droit :', 0),
            ('bras devant :', 10),
            ('chargeur gauche :', 11),
            ('Servomoteur 9 :', 9)])

        self._button_reset = QPushButton('Reset')

        layout = QGridLayout()
        tab_widget = QTabWidget()
        tab_widget.addTab(self._servo_values, "Servo values")
        layout.addWidget(tab_widget)
        layout.addWidget(self._button_reset)
        self.setLayout(layout)
        self._button_reset.clicked.connect(self._reset)

    def _reset(self):
        pass
        
    def set_client(self, client):
        self._client = client
        self._servo_values._client = client
