from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeySequence

from widgets.properties_editor import PropertiesEditorWidget
from widgets.table_view import TableViewWidget

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

        self._delta_d_edit = QLineEdit('400')
        self._delta_yaw_edit = QLineEdit('180.0')
        self._execute_translation_button = QPushButton('translation (mm)')
        self._execute_rotation_button = QPushButton('rotation (deg)')

        self._pose_x_edit = QLineEdit('0')
        self._pose_y_edit = QLineEdit('0')
        self._pose_yaw_edit = QLineEdit('0')
        self._button_set_pose = QPushButton('set pose')
        self._button_reposition = QPushButton('reposition')

        self._goldo_traj_button = QPushButton('trajectory')
        self._start_traj_edit_button = QPushButton('start_traj_edit')
        self._end_traj_edit_button = QPushButton('end_traj_edit')

        self._F11_shortcut = QShortcut(QKeySequence(Qt.Key_F11), self)
        self._F11_shortcut.activated.connect(self._test_prop_goldo_start)
        self._F12_shortcut = QShortcut(QKeySequence(Qt.Key_F12), self)
        self._F12_shortcut.activated.connect(self._test_prop_goldo_stop)

        li = 0

        layout = QGridLayout()
        layout.addWidget(self._propulsion_enable_button,li,0)
        layout.addWidget(self._propulsion_disable_button,li,1)
        li += 1

        layout.addWidget(self._motors_enable_button,li,0)
        layout.addWidget(self._motors_disable_button,li,1)
        li += 1

        layout.addWidget(QLabel('left pwm'),li,0)
        layout.addWidget(QLabel('right pwm'),li,1)
        li += 1

        layout.addWidget(self._left_pwm_spinbox,li,0)
        layout.addWidget(self._right_pwm_spinbox,li,1)
        li += 1

        layout.addWidget(self._set_pwm_button,li,0)
        layout.addWidget(self._zero_pwm_button,li,1)
        li += 1

        layout.addWidget(self._execute_translation_button,li,0)
        layout.addWidget(self._delta_d_edit,li,1)
        li += 1

        layout.addWidget(self._execute_rotation_button,li,0)
        layout.addWidget(self._delta_yaw_edit,li,1)
        li += 1

        layout.addWidget(QLabel('pose x(mm)'),li,0)
        layout.addWidget(self._pose_x_edit,li,1)
        li += 1

        layout.addWidget(QLabel('pose y(mm)'),li,0)
        layout.addWidget(self._pose_y_edit,li,1)
        li += 1
        
        layout.addWidget(QLabel('pose yaw(deg)'),li,0)
        layout.addWidget(self._pose_yaw_edit,li,1)
        li += 1

        layout.addWidget(self._button_set_pose,li,0)
        layout.addWidget(self._button_reposition,li,1)
        li += 1

        layout.addWidget(self._start_traj_edit_button,li,0)
        layout.addWidget(self._end_traj_edit_button,li,1)
        li += 1

        layout.addWidget(self._goldo_traj_button,li,0)
        li += 1

        self.setLayout(layout)
        
        self._propulsion_enable_button.clicked.connect(self._propulsion_enable)
        self._propulsion_disable_button.clicked.connect(self._propulsion_disable)
        self._motors_enable_button.clicked.connect(self._motors_enable)
        self._motors_disable_button.clicked.connect(self._motors_disable)
        self._set_pwm_button.clicked.connect(self._set_pwm)
        self._zero_pwm_button.clicked.connect(self._zero_pwm)

        self._execute_translation_button.clicked.connect(self._execute_translation)
        self._execute_rotation_button.clicked.connect(self._execute_rotation)

        self._button_set_pose.clicked.connect(self._set_pose)
        self._button_reposition.clicked.connect(self._reposition_forward)

        self._start_traj_edit_button.clicked.connect(self._start_traj_edit)
        self._end_traj_edit_button.clicked.connect(self._end_traj_edit)
        self._goldo_traj_button.clicked.connect(self._test_traj_goldo)

        self._telemetry_buffer = []
        self._current_telemetry = None
        self._current_telemetry_ex = None

        self._editing_traj = False
        self._traj_point_l = [(0.0,0.0)]

    def set_client(self, client):
        self._client = client
        self._client.goldo_telemetry.connect(self._on_goldo_telemetry)

    def _on_goldo_telemetry(self, telemetry):
        self._telemetry_buffer.append(telemetry)

    def _propulsion_enable(self):
        print(struct.pack('<B',1))
        self._client.send_message(message_types.PropulsionSetEnable, struct.pack('<B',1))

    def _propulsion_disable(self):
        self._client.send_message(message_types.PropulsionSetEnable, struct.pack('<B',0))

    def _motors_enable(self):
        self._client.send_message(message_types.SetMotorsEnable, struct.pack('<B',1))

    def _motors_disable(self):
        self._client.send_message(message_types.SetMotorsEnable, struct.pack('<B',0))

    def _set_pwm(self):
        self._client.send_message(message_types.SetMotorsPwm, struct.pack('<ff',self._left_pwm_spinbox.value() * 0.01, self._right_pwm_spinbox.value() * 0.01 ))
    
    def _zero_pwm(self):
        self._left_pwm_spinbox.setValue(0)
        self._right_pwm_spinbox.setValue(0)
        self._set_pwm()

    def _set_pose(self):
        x = int(self._pose_x_edit.text()) * 1e-3
        y = int(self._pose_y_edit.text()) * 1e-3
        yaw = int(self._pose_yaw_edit.text()) * math.pi / 180
        self._client.send_message(message_types.PropulsionSetPose, struct.pack('<fff', x, y, yaw))

    def _reposition_forward(self):
        self._client.send_message(message_types.PropulsionExecuteReposition, struct.pack('<bffff', 1, 0.2, 0, -1, 1.500))

    def _execute_rotation(self):
        delta_yaw_str = self._delta_yaw_edit.text()
        is_jump = "$" in delta_yaw_str
        delta_yaw = math.pi * float(delta_yaw_str.strip("$")) / 180.0
        # ROT?
        yaw_rate = 3.5
        accel = 10.0
        deccel = 10.0
        # TRAJ?
        #yaw_rate = 3.5
        #accel = 2.0
        #deccel = 2.0
        if (is_jump):
            pass # FIXME : TODO
        else:
            self._client.send_message(message_types.DbgPropulsionExecuteRotation, struct.pack('<ffff',delta_yaw,yaw_rate,accel,deccel))
        self._telemetry_buffer = []
        QTimer.singleShot(5000, self._plot_rotation)

    def _execute_translation(self):
        dist = int(self._delta_d_edit.text()) * 1e-3
        speed = 0.2
        accel = 0.2
        deccel = 0.2
        self._client.send_message(message_types.DbgPropulsionExecuteTranslation, struct.pack('<ffff',dist,speed,accel,deccel))
        self._telemetry_buffer = []
        # FIXME : TODO
        #QTimer.singleShot(9000, self._plot_translation)

    def _plot_rotation(self):
        self._plt_widget = PlotDialog()
        l = len (self._telemetry_buffer)
        ts_vec = [t.ts for t in self._telemetry_buffer]
        theta_vec = [t.theta_rad for t in self._telemetry_buffer]
        th_off = 0.0
        new_theta_vec = []
        for i in range(0,l-1):
            new_theta_vec.append(theta_vec[i]+th_off)
            if (theta_vec[i+1]-theta_vec[i])<-270.0:
                th_off += 360.0
            elif (theta_vec[i+1]-theta_vec[i])>270.0:
                th_off -= 360.0
        new_theta_vec.append(theta_vec[l-1]+th_off)
        theta_vec = new_theta_vec
        target_theta_vec = [t.target_theta_rad for t in self._telemetry_buffer]
        th_off = 0.0
        new_target_theta_vec = []
        for i in range(0,l-1):
            new_target_theta_vec.append(target_theta_vec[i]+th_off)
            if (target_theta_vec[i+1]-target_theta_vec[i])<-270.0:
                th_off += 360.0
            elif (target_theta_vec[i+1]-target_theta_vec[i])>270.0:
                th_off -= 360.0
        new_target_theta_vec.append(target_theta_vec[l-1]+th_off)
        target_theta_vec = new_target_theta_vec
        self._plt_widget.plot_curve_with_ts(ts_vec, theta_vec)
        self._plt_widget.plot_curve_with_ts(ts_vec, target_theta_vec)
        self._plt_widget.show()
        #self._telemetry_buffer = []

    def _start_traj_edit(self):
        self._editing_traj = True
        self._traj_point_l = [(0.0,0.0)]
        #TableViewWidget.g_table_view.debug_start_edit(0.0,0.0)
        TableViewWidget.g_table_view.debug_start_edit_rel()

    def _end_traj_edit(self):
        self._editing_traj = False
        self._traj_point_l = TableViewWidget.g_table_view.debug_stop_edit()

    def _test_traj_goldo(self):
        if self._editing_traj: return
        print (self._traj_point_l)
        msg = b''.join([struct.pack('<fff',0.4,0.3,0.3)] + [struct.pack('<ff', p[0]*1e-3, p[1] * 1e-3) for p in self._traj_point_l])
        #self._client.send_message_rplidar(message_types.PropulsionExecuteTrajectory, msg)
        self._client.send_message(message_types.PropulsionExecuteTrajectory, msg)
        self._telemetry_buffer = []

    def _test_prop_goldo_start(self):
        print ("_test_prop_goldo_start")
        self._client.send_message(message_types.PropulsionSetEnable, struct.pack('<B',0))
        self._client.send_message(message_types.SetMotorsEnable, struct.pack('<B',1))
        self._client.send_message(message_types.DbgSetMotorsPwm, struct.pack('<ff',self._left_pwm_spinbox.value() * 0.01, self._right_pwm_spinbox.value() * 0.01 ))

    def _test_prop_goldo_stop(self):
        print ("_test_prop_goldo_stop")
        self._client.send_message(message_types.DbgSetMotorsPwm, struct.pack('<ff', 0.0, 0.0))
        self._client.send_message(message_types.SetMotorsEnable, struct.pack('<B',0))

