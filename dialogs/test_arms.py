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
from config import robot_config

class ArmValuesWidget(QWidget):
    def __init__(self, servos, motor_id):
        super(ArmValuesWidget, self).__init__()
        self.ids = [s[1] for s in servos]        
        self._widgets = {}
        self._motor_id = motor_id
        layout = QGridLayout()

        i = 1
        layout.addWidget(QLabel('Goal position'),0,1)
        layout.addWidget(QLabel('Enable'),0,2)
        layout.addWidget(QLabel('Torque limit'),0,3)
        layout.addWidget(QLabel('Position'),0,4)
        layout.addWidget(QLabel('Speed'),0,5)
        layout.addWidget(QLabel('Load'),0,6)

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

            layout.addWidget(QLabel(k),i,0)
            layout.addWidget(wid_goal_pos,i,1)
            layout.addWidget(wid_torque_enable,i,2)
            layout.addWidget(wid_torque_limit,i,3)
            layout.addWidget(wid_current_pos,i,4)
            layout.addWidget(wid_current_speed,i,5)
            layout.addWidget(wid_current_load,i,6)
            self._widgets[id_] = (wid_goal_pos, wid_torque_enable, wid_torque_limit, wid_current_pos, wid_current_speed,
             wid_current_load)
            i+=1
        self._button_read_state = QPushButton('Read')
        self._button_copy_pos = QPushButton('Copy')
        self._spinbox_motor = QSpinBox()
        self._spinbox_motor.setRange(-511,511)
        self._button_motor_activate = QPushButton('Motor')
        self._button_motor_activate.setCheckable(True)

        self._spinbox_position = QSpinBox()
        self._spinbox_position.setRange(0,32)

        self._spinbox_sequence = QSpinBox()
        self._spinbox_sequence.setRange(0,32)

        self._button_execute_sequence = QPushButton('execute sequence')
        self._button_go_position = QPushButton('go to position')
        self._button_set_position = QPushButton('Set position')

        layout.addWidget(self._button_read_state,i, 0)
        layout.addWidget(self._button_copy_pos,i+1, 0)
        layout.addWidget(self._spinbox_motor,i, 1)
        layout.addWidget(self._button_motor_activate,i+1, 1)

        self._spinbox_servo_id = QSpinBox()
        self._spinbox_servo_id.setRange(0,32)

        self._line_edit_servo = QLineEdit()
        layout.addWidget(self._spinbox_servo_id, i, 2)
        layout.addWidget(self._line_edit_servo, i+1, 2)

        layout.addWidget(self._spinbox_position, i, 3)
        layout.addWidget(self._button_go_position, i+1, 3)
        layout.addWidget(self._spinbox_sequence, i, 4)
        layout.addWidget(self._button_execute_sequence, i+1, 4)
        #layout.addWidget(self._button_set_position, i, 7)


        self.setLayout(layout)

        self._button_read_state.clicked.connect(self.read_dynamixels_state)
        self._button_copy_pos.clicked.connect(self._copy_pos)
        self._button_motor_activate.toggled.connect(self._motor_activate)
        self._line_edit_servo.returnPressed.connect(self._servoo)
        self._button_go_position.clicked.connect(self._go_position)
        self._button_execute_sequence.clicked.connect(self._execute_sequence)

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
            #wids[6].setText(str(values[3]))
            #wids[7].setText(str(values[4]))

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

    def _go_position(self):
        self._client.send_message(message_types.DbgArmsGoToPosition,
            struct.pack('<BB', self._motor_id, self._spinbox_position.value()))
    def _execute_sequence(self):
        self._client.send_message(message_types.DbgArmsExecuteSequence,
            struct.pack('<BB', self._motor_id, self._spinbox_sequence.value()))

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
        self._left_arm_values = ArmValuesWidget([(d['name'], d['id']) for d in robot_config['dynamixels']], 0)
        self._button_reset = QPushButton('Reset')
        self._button_send_config = QPushButton('send config')       

        layout = QGridLayout()        
        layout.addWidget(self._left_arm_values,0,0,1,7)

        layout.addWidget(QLabel("General"),1,0)
        layout.addWidget(self._button_reset,1,1)
        layout.addWidget(self._button_send_config,1,2)

        self._spinbox_arm_id = QSpinBox()
        self._spinbox_arm_id.setRange(0,5)

        self._spinbox_position = QSpinBox()
        self._spinbox_position.setRange(0,32)

        self._spinbox_sequence = QSpinBox()
        self._spinbox_sequence.setRange(0,32)
        
        self.setLayout(layout)
        self._button_reset.clicked.connect(self._reset)
        self._button_send_config.clicked.connect(self._send_config)


    def set_client(self, client):
        self._client = client
        self._left_arm_values.set_client(client)

    def _reset(self):
        self._client.send_message(79,b'')

    def _send_config_positions(self, arm_id, name):
        arm_positions = [[int(e) for e in l.strip().split(',')] for l in open('robot_config/{}_positions.txt'.format(name)) if not l.startswith('//')]

        for p in arm_positions:
            msg = struct.pack('<BB', arm_id, p[0])
            msg = msg + b''.join([struct.pack('<H', v) for v in p[1:]])
            print([struct.pack('<H', v) for v in p[1:]])
            print(msg)
            self._client.send_message(message_types.DbgArmsSetPose,msg)

    def _go_position(self):
        self._client.send_message(message_types.DbgArmsGoToPosition,
            struct.pack('<BB', self._spinbox_arm_id.value(), self._spinbox_position.value()))

    def _execute_sequence(self):
        self._client.send_message(message_types.DbgArmsExecuteSequence,
            struct.pack('<BB', self._spinbox_arm_id.value(), self._spinbox_sequence.value()))

    def _calibrate_columns(self):
        self._client.send_message(message_types.FpgaColumnsCalib,
            struct.pack('<B', 0))

    def _columns_go_position(self):
        self._client.send_message(message_types.FpgaColumnsMove,
            struct.pack('<B', self._spinbox_columns_pos.value()))

    def _columns_set_off_l(self):
        val = int(self._line_edit_columns_off_l.text())
        self._client.send_message(message_types.FpgaColumnsSetOffset,
                                  struct.pack('<Bi', 3, val))

    def _columns_set_off_c(self):
        val = int(self._line_edit_columns_off_c.text())
        self._client.send_message(message_types.FpgaColumnsSetOffset,
                                  struct.pack('<Bi', 2, val))

    def _columns_set_off_r(self):
        val = int(self._line_edit_columns_off_r.text())
        self._client.send_message(message_types.FpgaColumnsSetOffset,
                                  struct.pack('<Bi', 1, val))

    def _send_config(self):
        self._send_config_positions(0, 'left_arm')
        self._send_config_positions(1, 'right_arm')
        self._send_config_positions(2, 'grabber')
        self._send_config_positions(3, 'bascule')
        self._send_config_positions(4, 'colonne')
        
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
            self._client.send_message(message_types.DbgArmsSetCommand,struct.pack('<B', i) + cmd)
        seqs = b''.join([struct.pack('<BBBB', 0, 0, s[0], s[1]) for s in sequences])
        self._client.send_message(message_types.DbgArmsSetSequences, seqs)
        print(seqs)


