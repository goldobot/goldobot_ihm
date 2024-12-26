from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QFileDialog

from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt

from goldobot.rec_loader import RecLoader, reconstruct_stream


from typing import Optional
from datetime import datetime
import bisect

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
        self._button_menu = QPushButton('...')
        
        self._menu = QMenu()
        self._button_menu.setMenu(self._menu)
        
        self._button_load.clicked.connect(self.load)
        self._button_play.clicked.connect(self.play)
        self._button_stop.clicked.connect(self.stop)

        self._slider_timestamp = QSlider(Qt.Horizontal)
        self._slider_timestamp.sliderReleased.connect(self._onSliderReleased)
        self._slider_timestamp.sliderMoved.connect(self._onSliderMoved)

        layout = QGridLayout()

        layout.addWidget(self._button_load, 0, 1)
        layout.addWidget(self._button_play, 0, 2)
        layout.addWidget(self._button_stop, 0, 3)
        layout.addWidget(self._button_menu, 0, 4)
        layout.addWidget(self._slider_timestamp, 1,0,1,4)
        self.setLayout(layout)
        
        self._menu.addAction('Export Odometry Counts').triggered.connect(self._export_odometry_counts)

    def loadRecordFile(self, path):
        self._loader.open(path)
        if len(self._loader._timestamps) > 0:
            self._ts_min = self._loader._timestamps[0]
            self._ts_max = self._loader._timestamps[-1]
        else:
            self._ts_min = 0
            self._ts_max = 0
        self._ts_next = self._ts_min
        self._ts_current = self._ts_min
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
        
    def setTimestamp(self, timestamp):
        i = bisect.bisect_left(self._loader._timestamps, timestamp)
        self._index = i
        self._playNextMessage()
        
        
    def _playNextMessage(self):
        if self._index == len(self._loader._timestamps):
            return False
        topic, msg = self._loader._messages[self._index]
        self._client.onMessage(topic, msg)
        
        self._index += 1
        if self._index < len(self._loader._timestamps):
            self._ts_next = self._loader._timestamps[self._index]
        else:
            self.stop()
        return True
        
    def _playMessages(self, ts_target):
        ts = self._ts_next
        while self._ts_next < ts_target and self._index < len(self._loader._timestamps):
            ts = self._ts_next
            self._playNextMessage()
        self._ts_current = ts
            
    def _onSliderReleased(self):
        self._dt_last = datetime.now()
        self._ts_target = self._ts_next

    def _onSliderMoved(self, timestamp):
        self.setTimestamp(timestamp)
        
    def _onTimer(self):
        if self._slider_timestamp.isSliderDown():
            return
        dt = datetime.now()
        self._ts_target += int((dt - self._dt_last).total_seconds() * 1000)
        self._dt_last = dt
        
        self._playMessages(self._ts_target)
        self._slider_timestamp.setValue(self._ts_current)


    def set_client(self, client: ''):
        self._client = client

    def onUpdateClicked(self):
        self._model.load(self._last)
        
    def _export_odometry_counts(self):
        path = QFileDialog.getSaveFileName(self, 'Save file')[0]
        c_left, c_right = reconstruct_stream(self._loader)
        file = open(path, 'w')
        file.write('encoder_left,encoder_right\n')
        for cl,cr in zip(c_left, c_right):
            file.write(f'{cl},{cr}\n')
        
    
        



