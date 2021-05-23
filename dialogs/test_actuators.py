from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QComboBox

from widgets.properties_editor import PropertiesEditorWidget

import struct
from goldobot import message_types
from goldobot import config

import struct
import math

import google.protobuf as _pb
_sym_db = _pb.symbol_database.Default()

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
            
            self._client.send_message(message_types.FpgaCmdServo,
            struct.pack('<BH', id_, self._widgets[id_][0].value()))

class TestActuatorsDialog(QDialog):
    def __init__(self, parent = None):
        super(TestActuatorsDialog, self).__init__(None)
        self._client = None
        self._button = QPushButton('set actuator')
        servos = []
        i = 0
        for s in config.robot_config.config_proto.servos:
            servos.append((s.name, i))
            i += 1
        self._servo_values = ActuatorValuesWidget(servos)
        self._button_go = QPushButton('go')

        layout = QGridLayout()
        #tab_widget = QTabWidget()
        #.addTab(self._servo_values, "Servo values")
        #layout.addWidget(tab_widget)
        #layout.addWidget(self._button_reset)
        self.combobox_servo = QComboBox()
        self.spinbox_value = QSpinBox()
        
        self.button_go = QPushButton('go')
        self.spinbox_value.setRange(0, 0x40000)
        for s in config.robot_config.config_proto.servos:
            self.combobox_servo.addItem(s.name)
        
        
        layout.addWidget(self.combobox_servo, 0,0)
        layout.addWidget(self.spinbox_value, 0,1)
        layout.addWidget(self.button_go, 0,2)
        self.setLayout(layout)
        self.button_go.clicked.connect(self._go)

    def _go(self):
        servo_id = self.combobox_servo.currentIndex()
        position = self.spinbox_value.value()
        msg = _sym_db.GetSymbol('goldo.nucleo.servos.Move')(servo_id=servo_id, position=position, speed=0x000f)
        self._client.publishTopic('nucleo/in/servo/move', msg)

        
    def set_client(self, client):
        self._client = client
        self._servo_values._client = client
