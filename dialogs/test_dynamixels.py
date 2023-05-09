from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTabWidget

import struct

from goldobot import message_types
from goldobot import config
import goldobot.pb2 as _pb2
import google.protobuf as _pb

_sym_db = _pb.symbol_database.Default()


class Dynamixel():
    index = 0
    enable = False
    id = 0
    name = "Dynamixel"
    pos = 0

    def __init__(self, index, enable, id, name, pos):
        self.index = index
        self.enable = enable
        self.id = id
        self.name = name
        self.pos = pos

    def toggle(self):
        self.enable = not self.enable
        print("Dynamixel index = " + str(self.index) + ", enable = " + str(self.enable) + ", id = " + str(self.id) + ",name =" + self.name + ", pos = " + str(self.pos))


class TestDynamixelAx12Dialog(QDialog):
    def __init__(self, parent = None):
        super(TestDynamixelAx12Dialog, self).__init__(None)

        layout = QGridLayout()
        self.dynamixels = []
        self.pos_labels = []
        i = 0

        for s in config.robot_config.config_proto.servos:
            if s.type == _pb2.goldo.nucleo.servos_pb2.ServoType.DYNAMIXEL_AX12 or s.type == _pb2.goldo.nucleo.servos_pb2.ServoType.DYNAMIXEL_MX28 : 
                self.dynamixels.append(Dynamixel(i, False, s.id, s.name, 0))
                # Checkbox enable
                enable_box = QCheckBox()
                enable_box.setChecked = False
                enable_box.toggled.connect(self.dynamixels[i].toggle)
                layout.addWidget(enable_box, i, 0)
                layout.addWidget(QLabel(str(self.dynamixels[i].id)), i, 1)
                layout.addWidget(QLabel(str(self.dynamixels[i].name)), i, 2)
                self.pos_labels.append(QLabel(str(self.dynamixels[i].pos)))
                layout.addWidget(self.pos_labels[i], i, 3)
                i += 1

        self._text_field = QTextEdit()
        layout.addWidget(self._text_field, i, 0, 1, 4)

        self._button_read = QPushButton('Read')
        layout.addWidget(self._button_read, i+1, 0, 1, 4)

        self.setLayout(layout)

        self._button_read.clicked.connect(self.read_registers)    

    def set_client(self, client):
        self._client = client
        self._client.registerCallback('gui/in/robot_state', self._on_robot_state)

    def read_registers(self):
        values = ""
        for d in self.dynamixels:
            if d.enable is True:
                if values:
                    values += ",\n"
                values += "'" + d.name + "': " + str(d.pos)
        self._text_field.setText(values)

    def _on_robot_state(self, msg):
        self._servo_states = msg.servos
        for d in self.dynamixels:
            d.pos = self._servo_states[d.name].measured_position
            self.pos_labels[d.index].setText(str(d.pos))