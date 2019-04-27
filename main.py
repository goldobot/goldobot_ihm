import sys
import signal
import math
import struct
import config

from optparse import OptionParser

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QLineEdit, QGridLayout, QFrame, QPushButton, QSpinBox, QSizePolicy
from PyQt5.QtCore import QObject, pyqtSignal, QSize, QRectF, QPointF, Qt, QTimer
from PyQt5.QtWidgets import QTabWidget, QAction, QDialog, QVBoxLayout, QCheckBox
from PyQt5.QtWidgets import  QHBoxLayout, QComboBox

from widgets.table_view import TableViewWidget

from zmq_client import ZmqClient

from widgets.robot_status import RobotStatusWidget
from widgets.properties_editor import PropertiesEditorWidget
from dialogs.odometry_config import OdometryConfigDialog
from dialogs.propulsion_controller_config import PropulsionControllerConfigDialog
from dialogs.test_propulsion import PropulsionTestDialog
from dialogs.test_arms import TestArmsDialog
from dialogs.test_actuators import TestActuatorsDialog
from dialogs.test_dynamixels import TestDynamixelAx12Dialog
from dialogs.debug_fpga import DebugFpgaDialog

from parse_sequence import SequenceParser

import message_types

class ServoWidget(QWidget):
    def __init__(self, parent = None):
        super(ServoWidgetWidget, self).__init__(None)
        self._client = None
        wid = QLineEdit()

        self._get_button = QPushButton('Get')

    def set_client(self, client):
        self._client = client



class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(None)
        # Create actions
        self._action_open_odometry_config = QAction("Configure Odometry")
        self._action_open_propulsion_controller_config = QAction("Configure Propulsion controller")
        self._action_propulsion_test = QAction("Test propulsion")
        self._action_arms_test = QAction("Test arms")
        self._action_dynamixel_ax12_test = QAction("Test dynamixel AX12")
        self._action_actuators_test = QAction("Test actionneurs")
        self._action_debug_fpga = QAction("Debug FPGA")
        self._action_reset = QAction("Reset")
        self._action_upload_sequence = QAction('Upload sequence')
        self._action_start_sequence = QAction('Start sequence')
        
        # Add menu
        tools_menu = self.menuBar().addMenu("Tools")
        tools_menu.addAction(self._action_open_odometry_config)
        tools_menu.addAction(self._action_open_propulsion_controller_config)
        tools_menu.addAction(self._action_propulsion_test)
        tools_menu.addAction(self._action_arms_test)
        tools_menu.addAction(self._action_dynamixel_ax12_test)
        tools_menu.addAction(self._action_actuators_test)
        tools_menu.addAction(self._action_reset)
        tools_menu.addAction(self._action_debug_fpga)
        tools_menu.addAction(self._action_upload_sequence)
        tools_menu.addAction(self._action_start_sequence)

        self._main_widget = QWidget()
        self._table_view = TableViewWidget()
        self._widget_robot_status = RobotStatusWidget()

        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        self.setCentralWidget(self._main_widget)
        layout1.addWidget(self._widget_robot_status)
        layout1.addLayout(layout2)
        layout2.addWidget(self._table_view)
        layout2.addStretch(1)

        self._main_widget.setLayout(layout1)

        # Connect signals
        self._action_open_odometry_config.triggered.connect(self._open_odometry_config)
        self._action_open_propulsion_controller_config.triggered.connect(self._open_propulsion_controller_config)
        self._action_propulsion_test.triggered.connect(self._open_propulsion_test)
        self._action_arms_test.triggered.connect(self._open_arms_test)
        self._action_dynamixel_ax12_test.triggered.connect(self._open_dynamixel_ax12_test)
        self._action_actuators_test.triggered.connect(self._open_actuators_test)
        self._action_debug_fpga.triggered.connect(self._open_debug_fpga)
        self._action_upload_sequence.triggered.connect(self._upload_sequence)
        self._action_start_sequence.triggered.connect(self._start_sequence)

        self._action_reset.triggered.connect(self._send_reset)

        self._dialog_odometry_config = OdometryConfigDialog(self)
        self._dialog_propulsion_controller_config = PropulsionControllerConfigDialog(self)
        self._dialog_propulsion_test = PropulsionTestDialog()
        self._dialog_arms_test = TestArmsDialog()
        self._dialog_dynamixel_ax12_test = TestDynamixelAx12Dialog()
        self._dialog_actuators_test = TestActuatorsDialog()
        self._dialog_debug_fpga = DebugFpgaDialog()

        #Dirty
        parser = OptionParser()
        parser.add_option('--robot-ip', default='192.168.1.222')
        (options, args) = parser.parse_args(sys.argv)
        self._client = ZmqClient(ip=options.robot_ip)
        self._dialog_odometry_config.set_client(self._client)
        self._dialog_propulsion_controller_config.set_client(self._client)
        self._dialog_propulsion_test.set_client(self._client)
        self._dialog_arms_test.set_client(self._client)
        self._dialog_dynamixel_ax12_test.set_client(self._client)
        self._widget_robot_status.set_client(self._client)
        self._table_view.set_client(self._client)
        
        self._dialog_actuators_test._servo_values._client = self._client
        
        # Add status bar
        self._status_link_state = QLabel('')
        self.statusBar().addWidget(self._status_link_state)
        self._status_match_state = QLabel('')
        self.statusBar().addWidget(self._status_match_state)
        
        self._client.comm_stats.connect(self._on_comm_stats)
        self._client.match_state_change.connect(self._on_match_state_change)
        
    def _open_odometry_config(self):
        self._dialog_odometry_config.show()

    def _open_propulsion_controller_config(self):
        self._dialog_propulsion_controller_config.show()

    def _open_propulsion_test(self):
        self._dialog_propulsion_test.show()  

    def _open_arms_test(self):
        self._dialog_arms_test.show()

    def _open_dynamixel_ax12_test(self):
        self._dialog_dynamixel_ax12_test.show()

    def _open_actuators_test(self):
        self._dialog_actuators_test.show()

    def _open_sequences_test(self):
        self._dialog_sequences_test.show()
        
    def _open_debug_fpga(self):
        self._dialog_debug_fpga.show()

    def _send_reset(self):
        self._client.send_message(message_types.DbgReset, b'')
        
    def _on_comm_stats(self, stats):
        self._status_link_state.setText('download {} {}'.format(*stats))
        
    def _on_match_state_change(self, state,side):
        self._status_match_state.setText('{} {}'.format(state, side))
        
    def _upload_sequence(self):
        config.load_dynamixels_config()
        parser = SequenceParser()
        parser.parse_file('sequence.txt')
        buff = parser.compile()
        self._client.send_message(40, b'')
        while len(buff) >32:
            self._client.send_message(42, buff[0:32])
            buff = buff[32:]
        self._client.send_message(42, buff)
        self._client.send_message(41, b'')
        #upload arms positions
        i = 0
        for n,pos in config.dynamixels_positions.items():
            print(n,pos)
            msg = struct.pack('<BB', 0, i)
            msg = msg + b''.join([struct.pack('<H', v) for v in pos])
            self._client.send_message(message_types.DbgArmsSetPose,msg)
            i += 1

    def _start_sequence(self):
        self._client.send_message(43, struct.pack('<H',1))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)

    main_window = MainWindow()
    main_window.show()


    #wid5 = TestPropulsionWidget()
    #wid5.set_client(c)
    #wid5.show()

    

    
    # Ensure that the application quits using CTRL-C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sys.exit(app.exec_())
