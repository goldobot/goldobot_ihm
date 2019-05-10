from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QGridLayout, QLabel, QGridLayout, QFrame
from widgets.properties_editor import PropertiesEditorWidget

class RobotStatusWidget(QWidget):
    def __init__(self, parent = None):
        super(RobotStatusWidget, self).__init__(None)
        self._client = None
        self._time_wid = QLineEdit()
        self._debug_gpio_wid = QLineEdit()
        self._x_wid = QLineEdit()
        self._y_wid = QLineEdit()
        self._button = QPushButton('Emergency Stop')
        self._robot_state_wid = QLineEdit('Iddle (?)')
        self._color_gpio_wid = QLineEdit('Unknown color')

        self._time_wid.setReadOnly(True)
        self._debug_gpio_wid.setReadOnly(True)
        self._debug_gpio_wid.setText('NA')

        layout = QGridLayout()
        layout.addWidget(self._robot_state_wid,0,0,1,1)
        layout.addWidget(self._color_gpio_wid,0,1,1,1)

        layout.addWidget(QLabel('time:'),1,0)
        layout.addWidget(self._time_wid,1,1,1,1)
        layout.addWidget(QLabel('GPIO:'),2,0)
        layout.addWidget(self._debug_gpio_wid,2,1,1,1)

        frame = QFrame()
        frame.setFrameShape(QFrame.HLine)
        layout.addWidget(frame,3,0,1,2)

        self._telemetry_props = PropertiesEditorWidget(None,
            [
            ('x', float,),
            ('y', float,),
            ('yaw', float,),
            ('speed', float,),
            ('yaw_rate', float,),
            ('acceleration', float),
            ('angular_\nacceleration', float),
            ('left_encoder', float,),
            ('right_encoder', float,),
            ('left_pwm', float,),
            ('right_pwm', float,),
            ('state', int),
            ('error',int)
            ],True)

        self._telemetry_ex_props = PropertiesEditorWidget(None,
            [
            ('target_x', float,),
            ('target_y', float,),
            ('target_yaw', float,),
            ('target_speed', float,),
            ('target_yaw_\nrate', float,),
            ('longitudinal_\nerror', float,),
            ('lateral_error', float,)  
            ],True)

        layout.addWidget(self._telemetry_props,4,0,1,2)
        layout.addWidget(self._telemetry_ex_props,5,0,1,2)
        layout.addWidget(self._button,6,0,1,2)
        self.setLayout(layout)
        self._button.clicked.connect(self._on_emergency_stop_button_clicked)

    def set_client(self, client):
        self._client = client
        self._client.propulsion_telemetry_ex.connect(self.update_telemetry_ex)
        self._client.heartbeat.connect(self.update_heartbeat)
        self._client.debug_gpio.connect(self.update_debug_gpio)
        self._client.propulsion_telemetry.connect(self.update_telemetry)

    def update_heartbeat(self, timestamp):
        self._time_wid.setText(str(timestamp*1e-3))

    def update_debug_gpio(self, gpio_mask):
        self._debug_gpio_wid.setText('%.8X'%(gpio_mask&0xffffffff))
        if ((gpio_mask&0x80000000) == 0x80000000):
            self._robot_state_wid.setStyleSheet("background-color: red")
        else:
            self._robot_state_wid.setStyleSheet("background-color: white")
        if ((gpio_mask&0x07000000) == 0x00000000):
            self._robot_state_wid.setText('Idle')
        if ((gpio_mask&0x07000000) == 0x01000000):
            self._robot_state_wid.setText('Debug')
        if ((gpio_mask&0x07000000) == 0x02000000):
            self._robot_state_wid.setText('PreMatch')
        if ((gpio_mask&0x07000000) == 0x03000000):
            self._robot_state_wid.setText('WaitForStartOfMatch')
        if ((gpio_mask&0x07000000) == 0x04000000):
            self._robot_state_wid.setText('Match')
        if ((gpio_mask&0x07000000) == 0x05000000):
            self._robot_state_wid.setText('PostMatch')
        if ((gpio_mask&0x07000000) == 0x06000000):
            self._robot_state_wid.setText('ManualControl')
        if ((gpio_mask&0x07000000) == 0x07000000):
            self._robot_state_wid.setText('??')
        if ((gpio_mask&0x00000002) == 0x00000002):
            self._color_gpio_wid.setStyleSheet("background-color: green")
            self._color_gpio_wid.setText('green')
        else:
            self._color_gpio_wid.setStyleSheet("background-color: orange")
            self._color_gpio_wid.setText('orange')

    def update_telemetry(self, telemetry):
        self._telemetry_props.set_value(telemetry)
    def update_telemetry_ex(self, telemetry_ex):
        self._telemetry_ex_props.set_value(telemetry_ex)

    def _on_emergency_stop_button_clicked(self):
        self._client.send_message(16,b'')
