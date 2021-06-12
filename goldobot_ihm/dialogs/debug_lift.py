from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTabWidget

import google.protobuf as _pb
_sym_db = _pb.symbol_database.Default()

registers = {
    'left': (0x80008494, 0x80008204, 0x80008500),
    'right': (0x8000849c, 0x80008224, 0x80008510)
    }

_default_kp = 0x00030000
_default_ki = 0x00000400
_default_kd = 0x00030000

class DebugLiftTab(QDialog):
    def __init__(self, regs, parent = None):
        super().__init__(parent)
        self._reg_pos = regs[0]
        self._reg_pwm = regs[1]
        self._reg_cmd = regs[2]
        
        layout = QGridLayout()
        self._button_enable = QPushButton('Enable')
        self._button_disable = QPushButton('Disable')
        layout.addWidget(self._button_enable,0,0)
        layout.addWidget(self._button_disable,0,1)
        
        self._line_edit_kp = QLineEdit()
        self._line_edit_ki = QLineEdit()
        self._line_edit_kd = QLineEdit()
        
        self._line_edit_kp.setText("{:>08x}".format(_default_kp))
        self._line_edit_ki.setText("{:>08x}".format(_default_ki))
        self._line_edit_kd.setText("{:>08x}".format(_default_kd))
        
        self._button_set_kp = QPushButton('Set kp')
        self._button_set_ki = QPushButton('Set ki')
        self._button_set_kd = QPushButton('Set kd')
        
        layout.addWidget(self._line_edit_kp,1,0)
        layout.addWidget(self._button_set_kp,1,1)
        
        layout.addWidget(self._line_edit_ki,2,0)
        layout.addWidget(self._button_set_ki,2,1)
        
        layout.addWidget(self._line_edit_kd,3,0)
        layout.addWidget(self._button_set_kd,3,1)
        
        
        self._spinbox_range = QSpinBox()
        self._spinbox_clamp = QSpinBox()
        self._button_set_range_clamp = QPushButton('Set')
        layout.addWidget(QLabel('Range'),4,0)
        layout.addWidget(QLabel('Clamp'),4,1)
        layout.addWidget(self._spinbox_range,5,1)
        layout.addWidget(self._spinbox_clamp,5,0)
        layout.addWidget(self._button_set_range_clamp,6,0)
        
        self._spinbox_bltrig = QSpinBox()
        self._spinbox_speed = QSpinBox()
        self._button_set_bltrig_speed = QPushButton('Set')
        layout.addWidget(QLabel('BlTrig'),7,0)
        layout.addWidget(QLabel('Speed'),7,1)
        layout.addWidget(self._spinbox_bltrig,8,1)
        layout.addWidget(self._spinbox_speed,8,0)
        layout.addWidget(self._button_set_bltrig_speed,9,0)
        
        self._spinbox_target = QSpinBox()
        self._button_jump = QPushButton('Jump')
        self._button_goto = QPushButton('GoTo')
        
        self.setLayout(layout)
        
    def set_client(self, client):
        self._client = client

        #self._client.fpga_registers.connect(self._on_fpga_registers)
        
    def _cmd_enable(self):
        pass #0x1000000v
        
    def _cmd_disable(self):
        pass #0x1000000v
                
    def _on_fpga_registers(self, apb_addr, apb_data):
        self._line_edit_apb_addr.setText("{:>08x}".format(apb_addr&0xffffffff))
        self._line_edit_apb_data.setText("{:>08x}".format(apb_data&0xffffffff))
        self._line_edit_crc.setText('NA')
        if (apb_addr&0xffffffff) == 0x8000800c:
            self._fpga_bitstream_ver.setText("{:>08x}".format(apb_data&0xffffffff))

class DebugLiftsDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)

        layout = QGridLayout()
        self._tab_widget = QTabWidget()
        self._lift_left = DebugLiftTab(registers['left'])
        self._lift_right = DebugLiftTab(registers['right'])
        self._tab_widget.addTab(self._lift_left, 'Left')
        self._tab_widget.addTab(self._lift_right, 'Right')
        layout.addWidget(self._tab_widget)
        self.setLayout(layout)
        return
        
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

        self._button_dbg_goldo = QPushButton('DbgGoldo')
        layout.addWidget(self._button_dbg_goldo, 5, 0)
        self._line_edit_dbg_goldo = QLineEdit()
        self._line_edit_dbg_goldo.setText("{:>08x}".format(0))
        layout.addWidget(self._line_edit_dbg_goldo,5,1)

        

        self._button_read_registers.clicked.connect(self.read_registers)
        self._button_write_registers.clicked.connect(self.write_registers)
        self._button_dbg_goldo.clicked.connect(self.dbg_goldo)

    def set_client(self, client):
        self._client = client
        self._lift_left.set_client(client)
        self._lift_right.set_client(client)
        #self._client.fpga_registers.connect(self._on_fpga_registers)
        #self._client.fpga_registers_crc.connect(self._on_fpga_registers_crc)
        #self._client.send_message(message_types.FpgaDbgReadReg, struct.pack('<I', 0x8000800c))

    def read_registers(self):
        my_addr = int(self._line_edit_apb_addr.text(),16)
        msg = _sym_db.GetSymbol('goldo.nucleo.fpga.RegRead')(apb_address = my_addr)
        self._client.publishTopic('nucleo/in/fpga/reg/read', msg)

    def write_registers(self):
        my_addr = int(self._line_edit_apb_addr.text(),16)
        my_data = int(self._line_edit_apb_data.text(),16)
        msg = _sym_db.GetSymbol('goldo.nucleo.fpga.RegWrite')(apb_address = my_addr, apb_value = my_data)
        self._client.publishTopic('nucleo/in/fpga/reg/write', msg)

    def dbg_goldo(self):
        #self._client.send_message(message_types.FpgaDbgGetErrCnt, bytes())
        val = int(self._line_edit_dbg_goldo.text(),16)
        #msg = _sym_db.GetSymbol('google.protobuf.UInt32Value')(value = 0x00000030)
        msg = _sym_db.GetSymbol('google.protobuf.UInt32Value')(value = val)
        print("{:8x}".format(msg.value))
        self._client.publishTopic('nucleo/in/dbg_goldo', msg)

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

