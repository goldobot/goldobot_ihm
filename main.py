import sys
import signal
import math
import struct

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

import message_types
from compile_strategy import StrategyCompiler

       



class TestSequencesDialog(QDialog):
    def __init__(self, parent = None):
        super(TestSequencesDialog, self).__init__(None)
        self._client = None
        self._button_upload = QPushButton('upload')
        self._button_execute = QPushButton('execute')
        self._combobox_sequence_id = QComboBox()
        
        layout = QGridLayout()        
        layout.addWidget(self._button_upload, 0, 0)
        layout.addWidget(self._combobox_sequence_id, 1, 0)
        layout.addWidget(self._button_execute, 1, 1)
        self.setLayout(layout)
        self._button_upload.clicked.connect(self._upload)
        self._button_execute.clicked.connect(self._execute)
        self._sequence_ids = []       

    def set_client(self, client):
        self._client = client
        
    def _upload(self):
        sc = StrategyCompiler()
        sc.compile_strategy()
        self._combobox_sequence_id.clear()
        self._sequence_ids = []
        for k,v in sc._sequence_ids.items():
            self._combobox_sequence_id.addItem(k)
            self._sequence_ids.append(v)
        for i in range(len(sc._points)):
            p = sc._points[i]
            self._client.send_message(message_types.DbgRobotSetPoint, struct.pack('<Hff',i,p[0],p[1]))
        for i in range(len(sc._commands)):
            self._client.send_message(message_types.DbgRobotSetCommand, struct.pack('<H', i) + sc._commands[i].serialize())
        for i in range(len(sc._trajectory_buffer)):
            self._client.send_message(message_types.DbgRobotSetTrajectoryPoint, struct.pack('<BB', i,sc._trajectory_buffer[i]))
        for i in range(len(sc._sequences)):
            seq = sc._sequences[i]
            self._client.send_message(message_types.DbgRobotSetSequence, struct.pack('<HHH', i, seq[0], seq[1])) 

    def _execute(self):
        seq_id = self._sequence_ids[self._combobox_sequence_id.currentIndex()]
        print(seq_id)
        self._client.send_message(message_types.DbgRobotExecuteSequence, struct.pack('<B', seq_id))

   
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
        self._action_sequences_test = QAction("Test sequences")
        self._action_reset = QAction("Reset")

        # Add menu
        tools_menu = self.menuBar().addMenu("Tools")
        tools_menu.addAction(self._action_open_odometry_config)
        tools_menu.addAction(self._action_open_propulsion_controller_config)
        tools_menu.addAction(self._action_propulsion_test)
        tools_menu.addAction(self._action_arms_test)
        tools_menu.addAction(self._action_dynamixel_ax12_test)
        tools_menu.addAction(self._action_actuators_test)
        tools_menu.addAction(self._action_sequences_test)
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

        # Connect signals
        self._action_open_odometry_config.triggered.connect(self._open_odometry_config)
        self._action_open_propulsion_controller_config.triggered.connect(self._open_propulsion_controller_config)
        self._action_propulsion_test.triggered.connect(self._open_propulsion_test)
        self._action_arms_test.triggered.connect(self._open_arms_test)
        self._action_dynamixel_ax12_test.triggered.connect(self._open_dynamixel_ax12_test)
        self._action_actuators_test.triggered.connect(self._open_actuators_test)
        self._action_sequences_test.triggered.connect(self._open_sequences_test)

        self._action_reset.triggered.connect(self._send_reset)

        self._dialog_odometry_config = OdometryConfigDialog(self)
        self._dialog_propulsion_controller_config = PropulsionControllerConfigDialog(self)
        self._dialog_propulsion_test = PropulsionTestDialog()
        self._dialog_arms_test = TestArmsDialog()
        self._dialog_dynamixel_ax12_test = TestDynamixelAx12Dialog()
        self._dialog_actuators_test = TestActuatorsDialog()
        self._dialog_sequences_test = TestSequencesDialog()

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
        self._dialog_sequences_test.set_client(self._client)
        self._widget_robot_status.set_client(self._client)
        self._table_view.set_client(self._client)
        
        # Add status bar
        self._status_link_state = QLabel('')
        self.statusBar().addWidget(self._status_link_state)
        
        self._client.comm_stats.connect(self._on_comm_stats)
        

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

    def _send_reset(self):
        self._client.send_message(message_types.DbgReset, b'')
        
    def _on_comm_stats(self, stats):
        print(stats)



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
