from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QFileDialog

from PyQt5.QtCore import QTimer

from goldobot.rec_loader import RecLoader


from typing import Optional
from datetime import datetime

import google.protobuf as _pb

_sym_db = _pb.symbol_database.Default()

class RecPlayerDialog(QDialog):
    _client : Optional['goldobot.zmq_client.ZmqClient']
    _loader: RecLoader
    def __init__(self, parent = None):
        super().__init__(parent)
        self._client = None
        self._loader = RecLoader()

        self._timer = QTimer()
        self._timer.timeout.connect(self._onTimer)
        self._timer.setInterval(10)

        self._button_load = QPushButton('load')
        self._button_play = QPushButton('play')
        self._button_stop = QPushButton('stop')
        
        self._button_load.clicked.connect(self.load)
        self._button_play.clicked.connect(self.play)
        self._button_stop.clicked.connect(self.stop)

        self._slider_timestamp = QSlider()

        layout = QGridLayout()

        layout.addWidget(self._button_load, 0, 1)
        layout.addWidget(self._button_play, 0, 2)
        layout.addWidget(self._button_stop, 0, 3)
        layout.addWidget(self._slider_timestamp)
        self.setLayout(layout)

    def loadRecordFile(self, path):
        self._loader.open(path)
        self._ts_min = self._loader._timestamps[0]
        self._ts_max = self._loader._timestamps[-1]
        self._ts_next = self._ts_min
        self._ts_target = self._ts_min
        self._dt_last = datetime.now()
        self._index = 0
        self._slider_timestamp.setMinimum(self._ts_min)
        self._slider_timestamp.setMaximum(self._ts_max)

    def load(self):
        path = QFileDialog.getOpenFileName(self, 'Open file')[0]
        self.loadRecordFile(path)
        
    def play(self):
        self._timer.start()
        self._dt_last = datetime.now()
        
    def stop(self):
        self._timer.stop()
        
    def _onTimer(self):
        dt = datetime.now()
        self._ts_target += int((dt - self._dt_last).total_seconds() * 1000)
        self._dt_last = dt
        
        ts = self._ts_next

        while self._ts_next < self._ts_target and self._index < len(self._loader._timestamps):
            ts = self._ts_next
            topic, msg = self._loader._messages[self._index]
            self._index += 1
            if self._index < len(self._loader._timestamps):
                self._ts_next = self._loader._timestamps[self._index]
            self._client.onMessage(topic, msg)
        self._slider_timestamp.setValue(ts)


    def set_client(self, client: ''):
        self._client = client

    def onUpdateClicked(self):
        self._model.load(self._last)



