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
from dialogs.sequences import SequencesDialog

from parse_sequence import SequenceParser

import message_types

dialogs = [
    ("Configure Odometry", OdometryConfigDialog),
    ("Configure Propulsion controller", PropulsionControllerConfigDialog),
    ("Test propulsion", PropulsionTestDialog),
    ("Test arms", TestArmsDialog),
    ("Test dynamixels", TestDynamixelAx12Dialog),
    ("Test actionneurs", TestActuatorsDialog),
    ("Debug FPGA", DebugFpgaDialog),
    ("Test sequences", SequencesDialog),
 ]
        
class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(None)
        # Create actions
       
        self._action_reset = QAction("Reset",self)
        self._action_enter_debug = QAction("Debug enter",self)
        self._action_exit_debug = QAction("Debug exit",self)
        
        # Add menu
        tools_menu = self.menuBar().addMenu("Tools")
        
        self._actions = []
        self._dialogs = []
        
        for d in dialogs:
            action = QAction(d[0],self)
            widget = d[1]()
            tools_menu.addAction(action)
            self._actions.append(action)
            self._dialogs.append(widget)
            action.triggered.connect(widget.show)
            
        tools_menu.addAction(self._action_enter_debug)
        tools_menu.addAction(self._action_exit_debug)
        tools_menu.addAction(self._action_reset)

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

        self._action_reset.triggered.connect(self._send_reset) 
        self._action_enter_debug.triggered.connect(self._send_enter_debug) 
        self._action_exit_debug.triggered.connect(self._send_exit_debug) 

        #Dirty
        parser = OptionParser()
        parser.add_option('--robot-ip', default='192.168.1.222')
        (options, args) = parser.parse_args(sys.argv)
        self._client = ZmqClient(ip=options.robot_ip)
        
        for d in self._dialogs:
            d.set_client(self._client)
                
        # Add status bar
        self._status_link_state = QLabel('')
        self.statusBar().addWidget(self._status_link_state)
        self._status_match_state = QLabel('')
        self.statusBar().addWidget(self._status_match_state)
        
        self._client.comm_stats.connect(self._on_comm_stats)
        self._client.match_state_change.connect(self._on_match_state_change)
        self._widget_robot_status.set_client(self._client)
        self._table_view.set_client(self._client)
        

    def _send_reset(self):
        self._client.send_message(message_types.DbgReset, b'')
        
    def _send_enter_debug(self):
        self._client.send_message(message_types.SetMatchState, struct.pack('<B', 6))
        
    def _send_exit_debug(self):
        self._client.send_message(message_types.SetMatchState, struct.pack('<B', 1))
        
    def _on_comm_stats(self, stats):
        self._status_link_state.setText('download {} {}'.format(*stats))
        
    def _on_match_state_change(self, state,side):
        self._status_match_state.setText('{} {}'.format(state, side))
        
    def _upload_sequence(self):
        config.load_dynamixels_config()
        config.load_sequence()
        
       

    def _start_sequence(self):
        self._client.send_message(43, struct.pack('<H',1))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #app.setAttribute(Qt.AA_EnableHighDpiScaling)

    main_window = MainWindow()
    main_window.show()
    
    # Ensure that the application quits using CTRL-C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sys.exit(app.exec_())