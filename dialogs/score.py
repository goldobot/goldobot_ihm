from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QComboBox, QLabel
from PyQt5.QtGui import QFont
from widgets.properties_editor import PropertiesEditorWidget

from goldobot.messages import OdometryConfig
from goldobot import message_types
import config
import struct


class ScoreDialog(QDialog):
    def __init__(self, parent = None):
        super(ScoreDialog, self).__init__(None)
        self._client = None
        self._label = QLabel()
        layout = QGridLayout()        
        layout.addWidget(self._label)        
        self.setLayout(layout)
        f = QFont( "Arial", 32, QFont.Bold);
        self._label.setFont(f)
        self._label.setText("score")
       
    def set_client(self, client):
        self._client = client
        self._client.sequence_event.connect(self.on_sequence_event)
        
    def on_sequence_event(self, event_id, buff):
        if event_id == 1:
            score = struct.unpack('<i', buff)[0]
            self._label.setText(str(score))