from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QCheckBox



import math

import google.protobuf as _pb
_sym_db = _pb.symbol_database.Default()


class TestRPLidarDialog(QDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client = None
        layout = QGridLayout()
        
        self._start_button = QPushButton('start')
        self._stop_button = QPushButton('stop')
        self._theta_offset_spinbox = QSpinBox()
        self._theta_offset_spinbox.setRange(-180, 180)
        self._autotest_checkbox = QCheckBox('autotest')        
        
        layout.addWidget(self._start_button, 0,0)
        layout.addWidget(self._stop_button, 1,0)
        layout.addWidget(self._theta_offset_spinbox, 2,0)
        layout.addWidget(self._autotest_checkbox, 3,0)
        self.setLayout(layout)
        
        self._start_button.clicked.connect(self._on_start)
        self._stop_button.clicked.connect(self._on_stop)
        self._autotest_checkbox.toggled.connect(self._on_autotest)
        self._theta_offset_spinbox.valueChanged.connect(self._on_theta)

    def _on_start(self):
        msg = _sym_db.GetSymbol('google.protobuf.Empty')()
        self._client.publishTopic('rplidar/in/start', msg)
        
    def _on_stop(self):
        msg = _sym_db.GetSymbol('google.protobuf.Empty')()
        self._client.publishTopic('rplidar/in/stop', msg)
        
    def _on_autotest(self):
        msg = _sym_db.GetSymbol('google.protobuf.BoolValue')(value=self._autotest_checkbox.isChecked())
        self._client.publishTopic('rplidar/in/config/autotest_enable', msg)
        
    def _on_theta(self, value):
        msg = _sym_db.GetSymbol('google.protobuf.FloatValue')(value = value * math.pi / 180)
        self._client.publishTopic('rplidar/in/config/theta_offset', msg)

        
    def set_client(self, client):
        self._client = client