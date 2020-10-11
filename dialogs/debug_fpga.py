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


class DebugFpgaDialog(QDialog):
    def __init__(self, parent = None):
        super(DebugFpgaDialog, self).__init__(None)

        layout = QGridLayout()

        layout.addWidget(QLabel('FPGA bitstream ver.:'),0,0)
        self._fpga_bitstream_ver = QLabel('NA')
        layout.addWidget(self._fpga_bitstream_ver,0,1)

        layout.addWidget(QLabel('APB addr'),1,0)
        self._line_edit_apb_addr = QLineEdit()
        self._line_edit_apb_addr.setText("{:>08x}".format(0x80008008))
        layout.addWidget(self._line_edit_apb_addr,1,1)

        layout.addWidget(QLabel('APB data'),2,0)
        self._line_edit_apb_data = QLineEdit()
        self._line_edit_apb_data.setText("{:>08x}".format(0))
        layout.addWidget(self._line_edit_apb_data,2,1)

        layout.addWidget(QLabel('CRC'),3,0)
        self._line_edit_crc = QLineEdit()
        self._line_edit_crc.setText('NA')
        layout.addWidget(self._line_edit_crc,3,1)

        self._button_read_registers = QPushButton('Read')
        layout.addWidget(self._button_read_registers, 4, 0)

        self._button_write_registers = QPushButton('Write')
        layout.addWidget(self._button_write_registers, 4, 1)

        self._button_get_err_cnt = QPushButton('GetErrCnt')
        layout.addWidget(self._button_get_err_cnt, 5, 0)

        self.setLayout(layout)

        self._button_read_registers.clicked.connect(self.read_registers)
        self._button_write_registers.clicked.connect(self.write_registers)
        self._button_get_err_cnt.clicked.connect(self.get_err_cnt)

    def set_client(self, client):
        self._client = client
        self._client.fpga_registers.connect(self._on_fpga_registers)
        self._client.fpga_registers_crc.connect(self._on_fpga_registers_crc)
        self._client.send_message(message_types.FpgaDbgReadReg, struct.pack('<I', 0x8000800c))

    def read_registers(self):
        my_addr = int(self._line_edit_apb_addr.text(),16)
        self._client.send_message(message_types.FpgaDbgReadRegCrc, struct.pack('<I', my_addr))

    def write_registers(self):
        my_addr = int(self._line_edit_apb_addr.text(),16)
        my_data = int(self._line_edit_apb_data.text(),16)
        self._client.send_message(message_types.FpgaDbgWriteReg, struct.pack('<II', my_addr, my_data))

    def get_err_cnt(self):
        self._client.send_message(message_types.FpgaDbgGetErrCnt, bytes())

    def _on_fpga_registers(self, apb_addr, apb_data):
        self._line_edit_apb_addr.setText("{:>08x}".format(apb_addr&0xffffffff))
        self._line_edit_apb_data.setText("{:>08x}".format(apb_data&0xffffffff))
        self._line_edit_crc.setText('NA')
        if (apb_addr&0xffffffff) == 0x8000800c:
            self._fpga_bitstream_ver.setText("{:>08x}".format(apb_data&0xffffffff))

    def _on_fpga_registers_crc(self, apb_addr, apb_data, crc):
        self._line_edit_apb_addr.setText("{:>08x}".format(apb_addr&0xffffffff))
        self._line_edit_apb_data.setText("{:>08x}".format(apb_data&0xffffffff))
        self._line_edit_crc.setText("{:>08x}".format(crc&0xffffffff))
        if (apb_addr&0xffffffff) == 0x8000800c:
            self._fpga_bitstream_ver.setText("{:>08x}".format(apb_data&0xffffffff))

