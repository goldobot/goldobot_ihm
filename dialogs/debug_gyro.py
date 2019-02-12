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
import message_types


class DebugGyroDialog(QDialog):
    def __init__(self, parent = None):
        super(DebugGyroDialog, self).__init__(None)

        layout = QGridLayout()

        layout.addWidget(QLabel('Register addr'),0,0)
        self._line_edit_reg_addr = QLineEdit()
        self._line_edit_reg_addr.setText('%x'%(0x80008008))
        layout.addWidget(self._line_edit_reg_addr,0,1)

        layout.addWidget(QLabel('Register data'),1,0)
        self._line_edit_reg_data = QLineEdit()
        self._line_edit_reg_data.setText('%x'%(0))
        layout.addWidget(self._line_edit_reg_data,1,1)

        self._button_read_registers = QPushButton('Read')
        layout.addWidget(self._button_read_registers, 2, 0)

        self._button_write_registers = QPushButton('Write')
        layout.addWidget(self._button_write_registers, 2, 1)

        layout.addWidget(QLabel('Current angle :'),3,0)
        self._line_edit_angle = QLineEdit()
        self._line_edit_angle.setText('%i'%(0))
        layout.addWidget(self._line_edit_angle,3,1)

        self._button_update_angle = QPushButton('Update')
        layout.addWidget(self._button_update_angle, 4, 1)

        self.setLayout(layout)

        self._button_read_registers.clicked.connect(self.read_registers)
        self._button_write_registers.clicked.connect(self.write_registers)
        self._button_update_angle.clicked.connect(self.update_angle)

    def set_client(self, client):
        self._client = client
        self._client.gyro_registers.connect(self._on_gyro_registers)
        self._client.update_gyro.connect(self._on_update_gyro)
        self._client.send_message(message_types.GyroDbgReadReg, struct.pack('<I', 0x8000800c))

    def read_registers(self):
        my_addr = int(self._line_edit_reg_addr.text(),16)
        self._client.send_message(message_types.GyroDbgReadReg, struct.pack('<I', my_addr))

    def update_angle(self):
        self._client.send_message(message_types.GyroGetAngle, b'')

    def write_registers(self):
        my_addr = int(self._line_edit_reg_addr.text(),16)
        my_data = int(self._line_edit_reg_data.text(),16)
        self._client.send_message(message_types.GyroDbgWriteReg, struct.pack('<II', my_addr, my_data))

    def _on_gyro_registers(self, reg_addr, reg_data):
        self._line_edit_reg_addr.setText('%x'%(reg_addr&0xffffffff))
        self._line_edit_reg_data.setText('%x'%(reg_data&0xffffffff))

    def _on_update_gyro(self, angle):
        self._line_edit_angle.setText('%i'%angle)
