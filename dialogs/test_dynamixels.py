from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTabWidget

import struct
from goldobot import message_types

ax12_registers = [
    ('model_number',0x00, 2, 'r'),
    ('firmware_version',0x02, 1, 'r'),
    ('id',0x03, 1, 'rwp'),
    ('baud_rate',0x04, 1, 'rwp'),
    ('return_delay_time', 0x05, 1, 'rwp'),
    ('cw_angle_limit', 0x06, 2, 'rw'),
    ('ccw_angle_limit', 0x08, 2, 'rw'),
    ('temperature_max_limit', 0x0B, 1, 'rw'),
    ('voltage_min_limit', 0x0C, 1, 'rw'),
    ('voltage_max_limit', 0x0D, 1, 'rw'),
    ('max_torque', 0x0E, 2, 'rw'),
    ('status_return_level', 0x10, 1, 'rw'),
    ('alarm_led', 0x11, 1, 'rw'),
    ('alarm_shutdown', 0x12, 1, 'rw'),
    ('down_calibration', 0x14, 2, 'r'),
    ('up_calibration', 0x16, 2, 'r'),
    ]
dynamixel_registers = [
    ('model_number',0x00, 2, 'r'),
    ('firmware_version',0x02, 1, 'r'),
    ('id',0x03, 1, 'rwp'),
    ('baud_rate',0x04, 1, 'rwp'),
    ('return_delay_time', 0x05, 1, 'rwp')
    ]

class TestDynamixelAx12Dialog(QDialog):
    def __init__(self, parent = None):
        super(TestDynamixelAx12Dialog, self).__init__(None)
        self._registers = ax12_registers

        layout = QGridLayout()
        self._spinbox_id = QSpinBox()
        self._spinbox_id.setRange(0,253)
        layout.addWidget(self._spinbox_id, 0,1)

        self._widgets = {}
        i = 1
        for k,a,s,r in self._registers:            
            wid = QLineEdit()
            layout.addWidget(QLabel(k), i, 0)
            layout.addWidget(wid, i, 1)
            self._widgets[k] = wid
            i += 1

        self._button_read_registers = QPushButton('Read')
        layout.addWidget(self._button_read_registers, i, 0)

        self._button_write_registers = QPushButton('Write')
        layout.addWidget(self._button_write_registers, i, 1)

        self.setLayout(layout)

        self._button_read_registers.clicked.connect(self.read_registers)
        self._button_write_registers.clicked.connect(self.write_registers)       

    def set_client(self, client):
        self._client = client
        self._client.dynamixel_registers.connect(self._on_dynamixel_registers)

    def read_registers(self):
        id_ = self._spinbox_id.value()
        for k, a, s, r in self._registers:
            self._client.send_message(77,struct.pack('<BBB',id_, a, s))

    def write_registers(self):
        id_ = self._spinbox_id.value()
        for k, a, s, r in self._registers:
            if 'w' in r and 'p' not in r:
                if s == 1:
                    self._client.send_message(78,struct.pack('<BBB',id_, a, int(self._widgets[k].text())))
                else:
                    self._client.send_message(78,struct.pack('<BBH',id_, a, int(self._widgets[k].text())))
                    


    def _on_dynamixel_registers(self, id_, address, data):
        if id_ == self._spinbox_id.value():
            for k, a, s, r in self._registers:
                if address == a and len(data) == s:
                    if s == 1:
                        val = struct.unpack('<B', data)[0]
                    else:
                        val = struct.unpack('<H', data)[0]
                    self._widgets[k].setText(str(val))