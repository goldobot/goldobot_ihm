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

import json
import struct
import message_types

def parse_item(js, prefix, endpoints, functions):
    if js['type'] == 'object':
        for m in js['members']:
            parse_item(m, prefix + js['name'] + '.', endpoints, functions)
        return
    if js['type'] == 'function':
        functions[prefix + js['name']] = js
        return
    if js['id'] == 0:
        return
    endpoints[prefix + js['name']] = (js['id'], js['type'], js['access'])
    
ODRIVE_CRC = 0x7411
ODRIVE_TYPES = {
    'bool': (1, '?', bool),
    'uint8': (1, 'B', int),
    'uint16': (2, 'H', int),
    'uint32': (4, 'I', int),
    'uint64': (8, 'Q', int),
    'int8': (1, 'b', int),
    'int16': (2, 'h', int),
    'int32': (4, 'i', int),
    'int64': (8, 'q', int),
    'float': (4, '<f', float)
   }
    

class ODriveDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(None)

        layout = QGridLayout()

        self._endpoint_select_combobox = QComboBox()
        layout.addWidget(self._endpoint_select_combobox,1,0)
        
        self._endpoint_value_lineedit = QLineEdit()
        layout.addWidget(self._endpoint_value_lineedit,1,1)
        
        self._endpoint_read_button = QPushButton('Read')
        layout.addWidget(self._endpoint_read_button,1,2)        
        
        self._endpoint_write_button = QPushButton('Write')
        layout.addWidget(self._endpoint_write_button,1,3)
        self._endpoint_write_button.setEnabled(False)

        self.setLayout(layout)
        
        js = json.load(open('doc/odrive_schema.json'))
        endpoints = {}
        functions = {}
        
        for item in js:
            parse_item(item, '', endpoints, functions)
        self._endpoints = endpoints
        self._functions = functions
        
        for ep in endpoints:
            self._endpoint_select_combobox.addItem(ep)


        self._endpoint_read_button.clicked.connect(self._read_endpoint)
        self._endpoint_write_button.clicked.connect(self._write_endpoint)
        self._endpoint_select_combobox.currentTextChanged.connect(self._on_endpoint_select_changed)
        #self._button_write_registers.clicked.connect(self.write_registers)
         #self._button_get_err_cnt.clicked.connect(self.get_err_cnt)

    def set_client(self, client):
        self._client = client
        self._client.odrive_response.connect(self._on_odrive_response)
        self._seq = None
        #self._client.fpga_registers_crc.connect(self._on_fpga_registers_crc)
        #self._client.send_message(message_types.FpgaDbgReadReg, struct.pack('<I', 0x8000800c))
        
    def _on_endpoint_select_changed(self, text):
        endpoint = self._endpoints[text]
        self._endpoint_write_button.setEnabled('w' in endpoint[2])
        
    def _read_endpoint(self):
        endpoint = self._endpoints[self._endpoint_select_combobox.currentText()]
        type = ODRIVE_TYPES[endpoint[1]]
        self._seq = self._client.send_message_odrive(endpoint[0] | 0x8000, type[0], b'', ODRIVE_CRC)
        self._selected_endpoint = endpoint
        
    def _write_endpoint(self):
        endpoint = self._endpoints[self._endpoint_select_combobox.currentText()]
        type = ODRIVE_TYPES[endpoint[1]]
        val = struct.pack(type[1], type[2](self._endpoint_value_lineedit.text()))
        self._seq = self._client.send_message_odrive(endpoint[0], 0, val, ODRIVE_CRC)
        
    def _on_odrive_response(self, seq, payload):
        if seq == self._seq:
            type = ODRIVE_TYPES[self._selected_endpoint[1]]
            value = struct.unpack(type[1], payload)[0]
            self._endpoint_value_lineedit.setText(str(value))

    def read_registers(self):
        my_addr = int(self._line_edit_apb_addr.text(),16)
        self._client.send_message(message_types.FpgaDbgReadRegCrc, struct.pack('<I', my_addr))


