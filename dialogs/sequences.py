from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QComboBox
from widgets.properties_editor import PropertiesEditorWidget

from goldobot.messages import OdometryConfig
from goldobot import message_types
from goldobot import config
import struct

class SequencesDialog(QDialog):
    def __init__(self, parent = None):
        super(SequencesDialog, self).__init__(None)
        self._client = None
        self._button_upload = QPushButton('upload')
        self._button_execute = QPushButton('execute')
        self._button_abort = QPushButton('abort')
        self._button_simulate = QPushButton('simulate')
        self._button_clear_simul = QPushButton('clear simul')
        self._combobox_sequence_id = QComboBox()
        
        layout = QGridLayout()        
        layout.addWidget(self._button_upload, 0, 0)
        layout.addWidget(self._button_abort, 0, 1)
        layout.addWidget(self._combobox_sequence_id, 1, 0)
        layout.addWidget(self._button_execute, 1, 1)
        layout.addWidget(self._button_clear_simul, 2, 0)
        layout.addWidget(self._button_simulate, 2, 1)
        self.setLayout(layout)
        self._button_upload.clicked.connect(self._upload)
        self._button_execute.clicked.connect(self._execute)
        self._button_abort.clicked.connect(self._abort)
        #self._button_simulate.clicked.connect(self._simulate)
        #self._button_clear_simul.clicked.connect(self._clear_simul)
        self._update_sequence_names()

    def set_client(self, client):
        self._client = client
        
    def _update_sequence_names(self):
        config_proto = config.robot_config.robot_config

        self._combobox_sequence_id.clear()        
        for k in config_proto.sequences_names:
            self._combobox_sequence_id.addItem(k)
        
    def _upload(self):
        cfg = config.robot_config
        cfg.update_config()
        self._update_sequence_names()
        self._client.publishTopic('config/test/put', cfg.robot_config)
        self._client.publishTopic('gui/out/commands/config_nucleo')

    def _execute(self):
        seq_name = self._combobox_sequence_id.currentText()
        self._client.publishTopic('robot/sequence/{}/execute'.format(seq_name))
        
    def _abort(self):
        self._client.send_message(45, b'')
