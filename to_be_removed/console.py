from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QTreeView

from goldobot_ihm.qjsonmodel import QJsonModel
    
    
from widgets.properties_editor import PropertiesEditorWidget

from typing import Optional

import google.protobuf as _pb
import google.protobuf.json_format
_sym_db = _pb.symbol_database.Default()

class ConsoleDialog(QDialog):
    _client : Optional['goldobot.zmq_client.ZmqClient']
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self._client = None


        self._view = QTreeView()
        self._model = model = QJsonModel()
        # FIXME : TODO : self._view.setModel(model), ca ne marche pas chez Goldo..
        #self._view.setModel(model)
        self._text_edit = QTextEdit()
        self._last = {}
        #self._topic_select = 

        self._button_update = QPushButton('update')

        layout = QGridLayout()


        layout.addWidget(self._view)
        layout.addWidget(self._button_update)
        self.setLayout(layout)
        
        self._button_update.clicked.connect(self.onUpdateClicked)


    def set_client(self, client: ''):
        self._client = client
        self._client.registerCallback('#/*', self._onLogMessage, True)
        
    def onUpdateClicked(self):
        self._model.load(self._last)
        
    def _onLogMessage(self, topic, msg):        
        txt = google.protobuf.json_format.MessageToDict(msg, including_default_value_fields=True)
        if topic == 'gui/in/robot_state':
            #self._text_edit.setText(txt)
            #print(msg.sensors)
            self._last = txt
        

     
