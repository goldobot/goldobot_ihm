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
        self._button_abort = QPushButton('abort')
        self._combobox_sequence_id = QComboBox()
        
        layout = QGridLayout()        
        layout.addWidget(self._button_upload, 0, 0)
        layout.addWidget(self._button_abort, 0, 1)
        layout.addWidget(self._combobox_sequence_id, 1, 0)
        layout.addWidget(self._button_execute, 1, 1)
        self.setLayout(layout)
        self._button_upload.clicked.connect(self._upload)
        self._button_execute.clicked.connect(self._execute)
        self._button_abort.clicked.connect(self._abort)
        self._update_sequence_names()
    

    def set_client(self, client):
        self._client = client
        
    def _update_sequence_names(self):
        sequences = config.robot_config.sequences
        self._combobox_sequence_id.clear()        
        for k in sequences.sequence_names:
            self._combobox_sequence_id.addItem(k)
        
    def _upload(self):
        config.robot_config.update_config()     
        self._update_sequence_names()
        sequences = config.robot_config.sequences
     
            
        buff = sequences.binary

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
        for n,pos in config.robot_config.dynamixels_positions.items():
            msg = struct.pack('<BB', 0, i)
            msg = msg + b''.join([struct.pack('<H', v) for v in pos])
            self._client.send_message(message_types.DbgArmsSetPose,msg)
            i += 1

    def _execute(self):
        seq_id = self._combobox_sequence_id.currentIndex()
        self._client.send_message(43, struct.pack('<H', seq_id))
        
    def _abort(self):
        self._client.send_message(45, b'')
