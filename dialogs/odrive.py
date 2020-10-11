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
from goldobot import message_types
from goldobot_ihm.odrive import calc_json_crc, parse_item, ODRIVE_TYPES

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

        self._function_select_combobox = QComboBox()
        layout.addWidget(self._function_select_combobox,2,0)
        
        self._read_json_button = QPushButton('Read JSON')
        layout.addWidget(self._read_json_button,3,0)

        self.setLayout(layout)

        self._update_schema(open('doc/odrive_schema.json', 'rb').read())

        self._endpoint_read_button.clicked.connect(self._read_endpoint)
        self._endpoint_write_button.clicked.connect(self._write_endpoint)
        self._endpoint_select_combobox.currentTextChanged.connect(self._on_endpoint_select_changed)
        self._function_select_combobox.currentTextChanged.connect(self._on_function_select_changed)
        self._read_json_button.clicked.connect(self._read_json)

    def set_client(self, client):
        self._client = client
        self._client.odrive_response.connect(self._on_odrive_response)
        self._seq = {}
        self._json_schema_buffer = b''

    def _update_schema(self, json_schema):
        crc = calc_json_crc(json_schema)
        print('odrive crc: 0x{:02x}'.format(crc))
        self._schema_crc = crc
        js = json.loads(json_schema.decode('utf8'))
        endpoints = {}
        functions = {}
        for item in js:
            parse_item(item, '', endpoints, functions)
        self._endpoints = endpoints
        self._functions = functions
        
        self._endpoint_select_combobox.clear()
        for ep in endpoints:
            self._endpoint_select_combobox.addItem(ep)
            
        self._function_select_combobox.clear()
        for fn in functions:
            self._function_select_combobox.addItem(fn)

    def _on_endpoint_select_changed(self, text):
        endpoint = self._endpoints[text]
        self._endpoint_write_button.setEnabled('w' in endpoint[2])
        
    def _on_function_select_changed(self, text):
        function = self._functions[text]
        print(function)

    def _read_endpoint(self):
        endpoint = self._endpoints[self._endpoint_select_combobox.currentText()]
        type = ODRIVE_TYPES[endpoint[1]]
        self._seq[endpoint[0]] = self._client.send_message_odrive(endpoint[0] | 0x8000, type[0], b'', self._schema_crc)
        self._selected_endpoint = endpoint

    def _write_endpoint(self):
        endpoint = self._endpoints[self._endpoint_select_combobox.currentText()]
        type = ODRIVE_TYPES[endpoint[1]]
        val = struct.pack(type[1], type[2](self._endpoint_value_lineedit.text()))
        self._client.send_message_odrive(endpoint[0], 0, val, self._schema_crc)

    def _read_json(self):
        self._reading_json = True
        self._json_schema_buffer = b''
        self._seq[0] = self._client.send_message_odrive(0x8000, 512, struct.pack('<I',0), 1)

    def _on_odrive_response(self, seq, payload):
        if seq == self._seq.get(0):
            self._json_schema_buffer += payload
            if len(payload):
                offset = len(self._json_schema_buffer)
                self._seq[0] = self._client.send_message_odrive(0x8000, 512, struct.pack('<I',offset), 1)
            else:
                del self._seq[0]
                open('odrive_schema.json', 'wb').write(self._json_schema_buffer)
                self._update_schema(self._json_schema_buffer)
        if seq == self._seq.get(self._selected_endpoint[0]):
            type = ODRIVE_TYPES[self._selected_endpoint[1]]
            value = struct.unpack(type[1], payload)[0]
            self._endpoint_value_lineedit.setText(str(value))
            del self._seq[self._selected_endpoint[0]]

    def read_registers(self):
        my_addr = int(self._line_edit_apb_addr.text(),16)
        self._client.send_message(message_types.FpgaDbgReadRegCrc, struct.pack('<I', my_addr))


