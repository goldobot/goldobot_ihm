from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTabWidget

import struct
import message_types
import config as cfg

class ArmValuesWidget(QWidget):
    def __init__(self, servos):
        super(ArmValuesWidget, self).__init__()
        self.ids = [s[1] for s in servos]        
        self._widgets = {}
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
        self._button_read_state = QPushButton('read')
        self._button_copy_state = QPushButton('copy')

        self._combobox_position = QComboBox()

        self._button_go_position = QPushButton('go')
        self._button_reload = QPushButton('reload')
        self._button_set_position = QPushButton('set')
        self._button_get_position = QPushButton('get')

        layout.addWidget(self._button_read_state,i, 0)
        layout.addWidget(self._button_copy_state,i, 1)
        layout.addWidget(self._button_get_position, i, 2)
        layout.addWidget(self._button_set_position, i, 3)
        layout.addWidget(self._combobox_position, i, 4)
        layout.addWidget(self._button_go_position, i, 5)
        layout.addWidget(self._button_reload, i, 6)
 
        self.setLayout(layout)
        self._button_get_position.clicked.connect(self._get_position)
        self._button_read_state.clicked.connect(self.read_dynamixels_state)
        self._button_go_position.clicked.connect(self._go_position)
        self._button_reload.clicked.connect(self.reload_positions)

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

    def reload_positions(self):
        cfg.robot_config.load_dynamixels_config()
        self._combobox_position.clear()
        i = 0
        for k,v in cfg.robot_config.dynamixels_positions.items():
            self._combobox_position.addItem(k)
            msg = struct.pack('<BB', 0, i) + b''.join([struct.pack('<H', p) for p in v])
            self._client.send_message(160, msg)
        
    def _on_dynamixel_registers(self, id_, address, data):
        if address == 36 and len(data) == 8:
            vals = struct.unpack('<HHHBB', data)
            self.update_dynamixel_state(id_,vals)

    def _copy_pos(self):
        for wids in self._widgets.values():
            wids[0].setValue(int(wids[3].text()))
            
    def _get_position(self):
        pos_index = self._combobox_position.currentIndex()
        pos = list(cfg.dynamixels_positions.items())[pos_index][1]
        for i in range(len(pos)):
            self._widgets[self.ids[i]][0].setValue(pos[i])

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
   
    def _go_position(self):
        pos_index = self._combobox_position.currentIndex()
        pos = list(cfg.robot_config.dynamixels_positions.items())[pos_index][1]
        
        #first update position
        msg = struct.pack('<BB', 0, pos_index)
        msg = msg + b''.join([struct.pack('<H', v) for v in pos])
        self._client.send_message(message_types.DbgArmsSetPose,msg)            
       
        self._client.send_message(message_types.DbgArmsGoToPosition,
            struct.pack('<BBH', pos_index, 0, 50))

    def update_values(self, values):
        for k, v in values.items():
            self._widgets[k].setValue(v)

    

class TestArmsDialog(QDialog):
    def __init__(self, parent = None):
        super(TestArmsDialog, self).__init__(None)
        robot_config = cfg.robot_config
        self._client = None
        self._button = QPushButton('set pwm')
        self._left_pwm_spinbox = QSpinBox()
        self._left_pwm_spinbox.setRange(0,1024)
        self._left_arm_values = ArmValuesWidget([(d['name'], d['id']) for d in robot_config.yaml['dynamixels']])
        self._button_reset = QPushButton('Reset')
        self._button_pump = QPushButton('Pompe On')
        self._button_shutdown = QPushButton('Shutdown')
        self._pump_state = False
        #self._button_send_config = QPushButton('send config')       

        layout = QGridLayout()        
        layout.addWidget(self._left_arm_values,0,0,1,7)

        #layout.addWidget(self._button_reset,1,1)
        #layout.addWidget(self._button_send_config,1,2)
        layout.addWidget(self._button_pump,1,3)
        layout.addWidget(self._button_shutdown,1,4)

        self._spinbox_arm_id = QSpinBox()
        self._spinbox_arm_id.setRange(0,5)

        self._spinbox_position = QSpinBox()
        self._spinbox_position.setRange(0,32)

        self._spinbox_sequence = QSpinBox()
        self._spinbox_sequence.setRange(0,32)
        
        self.setLayout(layout)
        self._button_pump.clicked.connect(self._switch_pump)
        #self._button_send_config.clicked.connect(self._send_config)
        self._button_shutdown.clicked.connect(self._shutdown)


    def set_client(self, client):
        self._client = client
        self._left_arm_values.set_client(client)
        
    def _shutdown(self):
        self._client.send_message(167,b'')
        
    def _send_config(self):
        pass

    def _switch_pump(self):
        self._pump_state = not self._pump_state
        if self._pump_state:
            self._button_pump.setText('Pompe Off')
            self._client.send_message(288,struct.pack('<Bh',0,400))
        else:
            self._button_pump.setText('Pompe On')
            self._client.send_message(288,struct.pack('<Bh',0,000))


