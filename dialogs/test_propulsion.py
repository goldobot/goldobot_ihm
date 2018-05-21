from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QTabWidget
from widgets.properties_editor import PropertiesEditorWidget

from messages import PropulsionControllerConfig
from messages import PIDConfig

from widgets.plot_dialog import PlotDialog

class TestPropulsionDialog(QDialog):
    def __init__(self, parent = None):
        super(TestPropulsionDialog, self).__init__(None)
        self._client = None
        self._propulsion_enable_button = QPushButton('propulsion enable')
        self._propulsion_disable_button = QPushButton('propulsion disable')
        self._motors_enable_button = QPushButton('motor enable')
        self._motors_disable_button = QPushButton('motors disable')
        self._left_pwm_spinbox = QSpinBox()
        self._left_pwm_spinbox.setRange(-100,100)
        self._right_pwm_spinbox = QSpinBox()
        self._right_pwm_spinbox.setRange(-100,100)
        self._set_pwm_button = QPushButton('set pwm')
        self._zero_pwm_button = QPushButton('zero pwm')

        self._position_steps_button = QPushButton('position steps')
        self._speed_steps_button = QPushButton('speed steps')

        layout = QGridLayout()
        layout.addWidget(self._propulsion_enable_button,0,0)
        layout.addWidget(self._propulsion_disable_button,0,1)

        layout.addWidget(self._motors_enable_button,1,0)
        layout.addWidget(self._motors_disable_button,1,1)

        layout.addWidget(QLabel('left pwm'),2,0)
        layout.addWidget(self._left_pwm_spinbox,3,0)

        layout.addWidget(QLabel('right pwm'),2,1)
        layout.addWidget(self._right_pwm_spinbox,3,1)

        layout.addWidget(self._set_pwm_button,4,0)
        layout.addWidget(self._zero_pwm_button,4,1)

        #layout.addWidget(self._set_pwm_button,5,0)
        layout.addWidget(self._speed_steps_button,5,1)

        self.setLayout(layout)
        
        self._propulsion_enable_button.clicked.connect(self._propulsion_enable)
        self._propulsion_disable_button.clicked.connect(self._propulsion_disable)
        self._motors_enable_button.clicked.connect(self._motors_enable)
        self._motors_disable_button.clicked.connect(self._motors_disable)
        self._set_pwm_button.clicked.connect(self._set_pwm)
        self._zero_pwm_button.clicked.connect(self._zero_pwm)
        self._speed_steps_button.clicked.connect(self._speed_steps)
        self._telemetry_buffer = []

    def set_client(self, client):
        self._client = client
        self._client.propulsion_telemetry.connect(self._on_telemetry)

    def _on_telemetry(self, telemetry):
        self._telemetry_buffer.append(telemetry)

    def _propulsion_enable(self):
        self._client.send_message(69, struct.pack('<B',1))
    def _propulsion_disable(self):
        self._client.send_message(69, struct.pack('<B',0))
    def _motors_enable(self):
        self._client.send_message(70, struct.pack('<B',1))
    def _motors_disable(self):
        self._client.send_message(70, struct.pack('<B',0))
    def _set_pwm(self):
        print('pwm')
        self._client.send_message(71, struct.pack('<ff',self._left_pwm_spinbox.value() * 0.01, self._right_pwm_spinbox.value() * 0.01 ))
    def _zero_pwm(self):
        self._left_pwm_spinbox.setValue(0)
        self._right_pwm_spinbox.setValue(0)
        self._set_pwm()
    def _speed_steps(self):
        self._client.send_message(72, struct.pack('<B',0))
        self._telemetry_buffer = []
        QTimer.singleShot(1000, self.foo)

    def foo(self):
        self._plt_widget = PlotDialog([t.speed for t in self._telemetry_buffer])
        self._plt_widget.show()
        self._telemetry_buffer = []