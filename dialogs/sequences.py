from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QComboBox
from widgets.properties_editor import PropertiesEditorWidget

from messages import OdometryConfig
import message_types
import config
import struct


class SequencesDialog(QDialog):
    def __init__(self, parent = None):
        super(SequencesDialog, self).__init__(None)
        self._client = None
        self._button_upload = QPushButton('upload')
        self._button_execute = QPushButton('execute')
        self._combobox_sequence_id = QComboBox()
        
        layout = QGridLayout()        
        layout.addWidget(self._button_upload, 0, 0)
        layout.addWidget(self._combobox_sequence_id, 1, 0)
        layout.addWidget(self._button_execute, 1, 1)
        self.setLayout(layout)
        self._button_upload.clicked.connect(self._upload)
        self._button_execute.clicked.connect(self._execute)
        self._sequence_ids = []       

    def set_client(self, client):
        self._client = client
        
    def _upload(self):
        config.load_dynamixels_config()
        config.load_sequence()
       
        self._combobox_sequence_id.clear()
        self._sequence_ids = []
        for k in config.compiled_sequences.sequence_names:
            self._combobox_sequence_id.addItem(k)
            
        buff = config.compiled_sequences.binary
        print(config.compiled_sequences.sequence_names)
        #Start programming
        self._client.send_message(40, b'')
        #Upload codes by packets
        while len(buff) >32:
            self._client.send_message(42, buff[0:32])
            buff = buff[32:]
        self._client.send_message(42, buff)
        #Finish programming
        self._client.send_message(41, b'')
        
        #upload arms positions
        i = 0
        for n,pos in config.dynamixels_positions.items():
            print(n,pos)
            msg = struct.pack('<BB', 0, i)
            msg = msg + b''.join([struct.pack('<H', v) for v in pos])
            self._client.send_message(message_types.DbgArmsSetPose,msg)
            i += 1

    def _execute(self):
        seq_id = self._combobox_sequence_id.currentIndex()
        print(seq_id)
        self._client.send_message(43, struct.pack('<H', seq_id))
