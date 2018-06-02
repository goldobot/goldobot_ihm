from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTabWidget

import struct
import message_types

class ArmValuesWidget(QWidget):
    def __init__(self, servos, motor_id):
        super(ArmValuesWidget, self).__init__()
        self.ids = [s[1] for s in servos]        
        self._widgets = {}
        self._motor_id = motor_id
        layout = QGridLayout()

        i = 1
        layout.addWidget(QLabel('Goal position'),0,1)
        layout.addWidget(QLabel('Torque enable'),0,2)
        layout.addWidget(QLabel('Torque limit'),0,3)
        layout.addWidget(QLabel('Current position'),0,4)
        layout.addWidget(QLabel('Current speed'),0,5)
        layout.addWidget(QLabel('Current load'),0,6)
        layout.addWidget(QLabel('Voltage'),0,7)
        layout.addWidget(QLabel('Temperature'),0,8)
        for k, id_ in servos:
            wid_goal_pos = QSpinBox()
            wid_goal_pos.setRange(0,4096)
            cb = (lambda b: lambda : self._on_goal_position_changed(b))(id_)
            wid_goal_pos.valueChanged.connect(cb)

            wid_torque_enable = QCheckBox()
            cb = (lambda b: lambda : self._on_torque_enable_changed(b))(id_)
            wid_torque_enable.stateChanged.connect(cb)

            wid_torque_limit = QSpinBox()
            wid_torque_limit.setRange(0,4096)
            cb = (lambda b: lambda : self._on_torque_limit_changed(b))(id_)
            wid_torque_limit.valueChanged.connect(cb)

            wid_current_pos = QLineEdit()
            wid_current_pos.setReadOnly(True)

            wid_current_speed = QLineEdit()
            wid_current_speed.setReadOnly(True)

            wid_current_load = QLineEdit()
            wid_current_load.setReadOnly(True)

            wid_current_voltage = QLineEdit()
            wid_current_voltage.setReadOnly(True)

            wid_current_temp = QLineEdit()
            wid_current_temp.setReadOnly(True)


            layout.addWidget(QLabel(k),i,0)
            layout.addWidget(wid_goal_pos,i,1)
            layout.addWidget(wid_torque_enable,i,2)
            layout.addWidget(wid_torque_limit,i,3)
            layout.addWidget(wid_current_pos,i,4)
            layout.addWidget(wid_current_speed,i,5)
            layout.addWidget(wid_current_load,i,6)
            layout.addWidget(wid_current_voltage,i,7)
            layout.addWidget(wid_current_temp,i,8)
            self._widgets[id_] = (wid_goal_pos, wid_torque_enable, wid_torque_limit, wid_current_pos, wid_current_speed,
             wid_current_load, wid_current_voltage, wid_current_temp)
            i+=1
        self._button_read_state = QPushButton('Read')
        self._button_copy_pos = QPushButton('Copy')
        self._spinbox_motor = QSpinBox()
        self._spinbox_motor.setRange(-511,511)
        self._button_motor_activate = QPushButton('Motor')
        self._button_motor_activate.setCheckable(True)

        self._spinbox_position = QSpinBox()
        self._spinbox_position.setRange(0,32)
        self._button_go_position = QPushButton('sxecute sequence')
        self._button_set_position = QPushButton('Set position')

        layout.addWidget(self._button_read_state,i, 0)
        layout.addWidget(self._button_copy_pos,i, 1)
        layout.addWidget(self._spinbox_motor,i, 2)
        layout.addWidget(self._button_motor_activate,i, 3)

        self._spinbox_servo_id = QSpinBox()
        self._spinbox_servo_id.setRange(0,32)

        self._line_edit_servo = QLineEdit()
        layout.addWidget(self._spinbox_servo_id, i, 4)
        layout.addWidget(self._line_edit_servo, i, 5)

        layout.addWidget(self._spinbox_position, i, 6)
        layout.addWidget(self._button_go_position, i, 7)
        #layout.addWidget(self._button_set_position, i, 7)


        self.setLayout(layout)

        self._button_read_state.clicked.connect(self.read_dynamixels_state)
        self._button_copy_pos.clicked.connect(self._copy_pos)
        self._button_motor_activate.toggled.connect(self._motor_activate)
        self._line_edit_servo.returnPressed.connect(self._servoo)
        self._button_go_position.clicked.connect(self._execute_sequence)

    def update_dynamixel_state(self, id_, values):
        if id_ in self._widgets:
            wids = self._widgets[id_]
            wids[3].setText(str(values[0]))
            velocity = values[1] & ((1 << 10) -1)
            if values[1] & (1 << 10):
                velocity = - velocity
            wids[4].setText(str(values[1]))
            load = values[2] & ((1 << 10) -1)
            if values[2] & (1 << 10):
                load = -load
            wids[5].setText(str(load))
            wids[6].setText(str(values[3]))
            wids[7].setText(str(values[4]))

    def set_client(self, client):
        self._client = client
        self._client.dynamixel_registers.connect(self._on_dynamixel_registers)

    def read_dynamixels_state(self):
        for id_ in self.ids:
            self._client.send_message(message_types.DbgDynamixelGetRegisters,struct.pack('<BBB',id_, 0x24, 8))

    def _on_dynamixel_registers(self, id_, address, data):
        if address == 36 and len(data) == 8:
            vals = struct.unpack('<HHHBB', data)
            self.update_dynamixel_state(id_,vals)

    def _copy_pos(self):
        for wids in self._widgets.values():
            wids[0].setValue(int(wids[3].text()))

    def _on_goal_position_changed(self, id_):
        wids = self._widgets[id_]
        # Set position
        if wids[1].isChecked():
            self._client.send_message(message_types.DbgDynamixelSetGoalPosition,struct.pack('<BH',id_, wids[0].value()))
        # Read registers
        self._client.send_message(message_types.DbgDynamixelGetRegisters, struct.pack('<BBB',id_, 0x24, 8))

    def _on_torque_limit_changed(self, id_):
        wids = self._widgets[id_]
        # Set position
        if wids[1].isChecked():
            self._client.send_message(message_types.DbgDynamixelSetTorqueLimit,struct.pack('<BH',id_, wids[2].value()))
        # Read registers
        self._client.send_message(message_types.DbgDynamixelGetRegisters, struct.pack('<BBB',id_, 0x24, 8))

    def _on_torque_enable_changed(self, id_):
        wids = self._widgets[id_]
        # Set torque enable
        self._client.send_message(message_types.DbgDynamixelSetTorqueEnable,struct.pack('<BB',id_, wids[1].isChecked()))
        # Read registers
        self._client.send_message(message_types.DbgDynamixelGetRegisters,struct.pack('<BBB',id_, 0x24, 8))

    def _motor_activate(self):
        if self._button_motor_activate.isChecked():
            self._client.send_message(message_types.FpgaCmdDCMotor,struct.pack('<Bh', self._motor_id, self._spinbox_motor.value()))
        else:
            self._client.send_message(message_types.FpgaCmdDCMotor,struct.pack('<Bh', self._motor_id, 0))

    def _servoo(self):
        val = int(self._line_edit_servo.text())
        self._client.send_message(message_types.FpgaCmdServo,struct.pack('<BI', self._spinbox_servo_id.value() ,val))

    def _execute_sequence(self):
        self._client.send_message(message_types.DbgArmsExecuteSequence,
            struct.pack('<BB', self._motor_id, self._spinbox_position.value()))

    def update_values(self, values):
        for k, v in values.items():
            self._widgets[k].setValue(v)

    

class TestArmsDialog(QDialog):
    def __init__(self, parent = None):
        super(TestArmsDialog, self).__init__(None)
        self._client = None
        self._button = QPushButton('set pwm')
        self._left_pwm_spinbox = QSpinBox()
        self._left_pwm_spinbox.setRange(0,1024)
        self._left_arm_values = ArmValuesWidget([
            ('slider',4),
            ('rotation', 83),
            ('shoulder', 84),
            ('elbow', 5),
            ('head', 6)], 0)
        self._right_arm_values = ArmValuesWidget([
            ('slider',1),
            ('rotation', 81),
            ('shoulder', 82),
            ('elbow', 2),
            ('head', 3)], 1)

        self._other_values = ArmValuesWidget([
            ('pince',101),
            ('bascule', 7),
            ('gache', 8)
           ], 2)

        self._button_reset = QPushButton('Reset')
        self._button_send_config = QPushButton('send config')
        layout = QGridLayout()
        tab_widget = QTabWidget()
        tab_widget.addTab(self._left_arm_values, "Left arm")
        tab_widget.addTab(self._right_arm_values, "Right arm")
        tab_widget.addTab(self._other_values, "Others")
        layout.addWidget(tab_widget)
        layout.addWidget(self._button_reset)
        layout.addWidget(self._button_send_config)
        self.setLayout(layout)
        self._button_reset.clicked.connect(self._reset)
        self._button_send_config.clicked.connect(self._send_config)
        

    def set_client(self, client):
        self._client = client
        self._left_arm_values.set_client(client)
        self._right_arm_values.set_client(client)
        self._other_values.set_client(client)

    def _reset(self):
        self._client.send_message(79,b'')

    def _send_config(self):
        #set positions
        left_arm_positions = [[int(e) for e in l.strip().split(',')] for l in open('robot_config/left_arm_positions.txt') if not l.startswith('//')]

        for p in left_arm_positions:
            self._client.send_message(message_types.DbgArmsSetPose,
                struct.pack('<BBHHHHH', 0, p[0], p[1], p[2], p[3], p[4], p[5]))

        right_arm_positions = [[int(e) for e in l.strip().split(',')] for l in open('robot_config/right_arm_positions.txt') if not l.startswith('//')]

        for p in right_arm_positions:
            self._client.send_message(message_types.DbgArmsSetPose,
                struct.pack('<BBHHHHH', 1, p[0], p[1], p[2], p[3], p[4], p[5]))
        #set sequences
        commands = []
        sequences = []
        for l in open('robot_config/arms_sequences.txt'):
            if l.startswith('//'):
                continue
            if l.startswith('#begin'):
                foo = [int(e) for e in l[7:].strip().split(',')]
                cur_seq = [len(commands), len(commands), foo[0], foo[1]]
            elif l.startswith('#end'):
                cur_seq[1] = len(commands)
                sequences.append(cur_seq)
            else:
                foo = l.strip().split(',')
                if foo[0] == 'delay':
                    commands.append(struct.pack('<BBBBH',0,0,0,0, int(foo[1])))
                if foo[0] == 'move':
                    commands.append(struct.pack('<BBBBH',1,0,int(foo[1]), int(foo[2]), int(foo[3])))
                if foo[0] == 'pump':
                    commands.append(struct.pack('<BBhH',2,0,int(foo[1]), int(foo[2])))
                if foo[0] == 'belt':
                    commands.append(struct.pack('<BBhH',3,0,int(foo[1]), int(foo[2])))
        for i in range(len(commands)):
            cmd = commands[i]
            print(cmd)
            self._client.send_message(message_types.DbgArmsSetCommand,struct.pack('<B', i) + cmd)
        seqs = b''.join([struct.pack('<BBBB', 0, 0, s[0], s[1]) for s in sequences])
        self._client.send_message(message_types.DbgArmsSetSequences, seqs)
        print(seqs)


