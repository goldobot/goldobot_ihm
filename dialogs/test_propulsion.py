from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import  QTimer

from widgets.properties_editor import PropertiesEditorWidget

from messages import PropulsionControllerConfig
from messages import PIDConfig
import message_types

import struct
import math

from widgets.plot_dialog import PlotDialog

class PropulsionTestDialog(QDialog):
    def __init__(self, parent = None):
        super(PropulsionTestDialog, self).__init__(None)
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
        self._yaw_rate_steps_button = QPushButton('yaw rate steps')
        self._execute_trajectory_button = QPushButton('trajectory')

        self._pose_x_edit = QLineEdit('0')
        self._pose_y_edit = QLineEdit('0')
        self._pose_yaw_edit = QLineEdit('0')
        self._button_set_pose = QPushButton('set pose')
        self._button_reposition = QPushButton('reposition')

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
        layout.addWidget(self._speed_steps_button,5,0)
        layout.addWidget(self._yaw_rate_steps_button,5,1)

        layout.addWidget(QLabel('x(mm)'),6,0)
        layout.addWidget(self._pose_x_edit,6,1)

        layout.addWidget(QLabel('y(mm)'),7,0)
        layout.addWidget(self._pose_y_edit,7,1)
        
        layout.addWidget(QLabel('yaw(deg'),8,0)
        layout.addWidget(self._pose_yaw_edit,8,1)

        layout.addWidget(self._button_set_pose, 9,0)
        layout.addWidget(self._button_reposition, 11,0)
        layout.addWidget(self._execute_trajectory_button, 10,0)

        self.setLayout(layout)
        
        self._propulsion_enable_button.clicked.connect(self._propulsion_enable)
        self._propulsion_disable_button.clicked.connect(self._propulsion_disable)
        self._motors_enable_button.clicked.connect(self._motors_enable)
        self._motors_disable_button.clicked.connect(self._motors_disable)
        self._set_pwm_button.clicked.connect(self._set_pwm)
        self._zero_pwm_button.clicked.connect(self._zero_pwm)

        self._speed_steps_button.clicked.connect(self._speed_steps)
        self._yaw_rate_steps_button.clicked.connect(self._yaw_rate_steps)

        self._button_set_pose.clicked.connect(self._set_pose)
        self._button_reposition.clicked.connect(self._reposition_forward)
        self._execute_trajectory_button.clicked.connect(self._test_trajectory)
        self._telemetry_buffer = []
        self._current_telemetry = None
        self._current_telemetry_ex = None

    def set_client(self, client):
        self._client = client
        self._client.propulsion_telemetry.connect(self._on_telemetry)
        self._client.propulsion_telemetry_ex.connect(self._on_telemetry_ex)

    def _on_telemetry(self, telemetry):
        self._telemetry_buffer.append((telemetry, self._current_telemetry_ex))
        self._current_telemetry = telemetry

    def _on_telemetry_ex(self, telemetry):
        self._current_telemetry_ex = telemetry

    def _propulsion_enable(self):
        print(struct.pack('<B',1))
        self._client.send_message(message_types.DbgSetPropulsionEnable, struct.pack('<B',1))

    def _propulsion_disable(self):
        self._client.send_message(message_types.DbgSetPropulsionEnable, struct.pack('<B',0))

    def _motors_enable(self):
        self._client.send_message(message_types.DbgSetMotorsEnable, struct.pack('<B',1))

    def _motors_disable(self):
        self._client.send_message(message_types.DbgSetMotorsEnable, struct.pack('<B',0))

    def _set_pwm(self):
        self._client.send_message(message_types.DbgSetMotorsPwm, struct.pack('<ff',self._left_pwm_spinbox.value() * 0.01, self._right_pwm_spinbox.value() * 0.01 ))
    
    def _zero_pwm(self):
        self._left_pwm_spinbox.setValue(0)
        self._right_pwm_spinbox.setValue(0)
        self._set_pwm()

    def _set_pose(self):
        x = int(self._pose_x_edit.text()) * 1e-3
        y = int(self._pose_y_edit.text()) * 1e-3
        yaw = int(self._pose_yaw_edit.text()) * math.pi / 180
        self._client.send_message(message_types.DbgPropulsionSetPose, struct.pack('<fff', x, y, yaw))

    def _reposition_forward(self):
        self._client.send_message(message_types.DbgPropulsionExecuteReposition, struct.pack('<bffff', 1, 0.2, 0, -1, 1.500))

    def _speed_steps(self):
        self._client.send_message(message_types.DbgPropulsionTest, struct.pack('<B',0))
        self._telemetry_buffer = []
        QTimer.singleShot(5000, self.foo)

    def _yaw_rate_steps(self):
        self._client.send_message(message_types.DbgPropulsionTest, struct.pack('<B',1))
        self._telemetry_buffer = []
        QTimer.singleShot(5000, self.foo)

    def _test_trajectory(self):
        self._client.send_message(message_types.DbgPropulsionExecuteTrajectory, struct.pack('<Bfff',0, 0.2,0.2,0.2))
        self._telemetry_buffer = []
        QTimer.singleShot(5000, self.foo)


    def foo(self):
        self._plt_widget = PlotDialog()
        self._plt_widget.plot_curve(0,[t[1].target_x for t in self._telemetry_buffer])
        self._plt_widget.plot_curve(0,[t[0].x for t in self._telemetry_buffer])

        self._plt_widget.plot_curve(1,[t[1].target_speed for t in self._telemetry_buffer])
        self._plt_widget.plot_curve(1,[t[0].speed for t in self._telemetry_buffer])

        self._plt_widget.plot_curve(2,[t[1].target_yaw for t in self._telemetry_buffer])
        self._plt_widget.plot_curve(2,[t[0].yaw for t in self._telemetry_buffer])

        self._plt_widget.plot_curve(3,[t[1].target_yaw_rate for t in self._telemetry_buffer])
        self._plt_widget.plot_curve(3,[t[0].yaw_rate for t in self._telemetry_buffer])

        self._plt_widget.show()
        self._telemetry_buffer = []