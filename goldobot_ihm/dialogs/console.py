from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QTextEdit
from widgets.properties_editor import PropertiesEditorWidget

from typing import Optional

import google.protobuf as _pb
_sym_db = _pb.symbol_database.Default()

class ConsoleDialog(QDialog):
    _client : Optional['goldobot.zmq_client.ZmqClient']
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self._client = None


        self._text_edit = QTextEdit()

        self._button_reset_counts = QPushButton('reset counts')

        layout = QGridLayout()


        layout.addWidget(self._text_edit)
        self.setLayout(layout)


    def set_client(self, client: ''):
        self._client = client
        self._client.registerCallback('*', self._onLogMessage)
        
    def _onLogMessage(self, msg):
        print(msg)
        

     