import sys
import signal
import math
import struct
import config

from optparse import OptionParser

import PyQt5.QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QLineEdit, QGridLayout, QFrame, QPushButton, QSpinBox, QSizePolicy
from PyQt5.QtCore import QObject, pyqtSignal, QSize, QRectF, QPointF, Qt, QTimer
from PyQt5.QtWidgets import QTabWidget, QAction, QDialog, QVBoxLayout, QCheckBox
from PyQt5.QtWidgets import  QHBoxLayout, QComboBox, QMessageBox, QShortcut
from PyQt5.QtGui import QKeySequence

from widgets.table_view import TableViewWidget
from widgets.plot_dialog import PlotDialog, ControlPlots

from goldobot.zmq_client import ZmqClient

from widgets.robot_status import RobotStatusWidget
from widgets.properties_editor import PropertiesEditorWidget
from dialogs.odometry_config import OdometryConfigDialog
from dialogs.propulsion_controller_config import PropulsionControllerConfigDialog
from dialogs.test_propulsion import PropulsionTestDialog
from dialogs.test_arms import TestArmsDialog
from dialogs.test_actuators import TestActuatorsDialog
from dialogs.test_dynamixels import TestDynamixelAx12Dialog
from dialogs.debug_fpga import DebugFpgaDialog
from dialogs.debug_asserv import DebugAsservDialog
from dialogs.sequences import SequencesDialog
from dialogs.score import ScoreDialog
from dialogs.test_hal import HalTestDialog
from dialogs.odrive import ODriveDialog
from .dialogs.console import ConsoleDialog
from goldobot_ihm.dialogs.rec_player import RecPlayerDialog
from dialogs.test_rplidar import TestRPLidarDialog
from goldobot_ihm.scope.scope import ScopeDialog

from parse_sequence import SequenceParser

from goldobot import message_types

from goldobot import config

import google.protobuf as _pb
_sym_db = _pb.symbol_database.Default()

import goldobot_ihm.dialogs as _dialogs

dialogs = [
    ("Test Hal", HalTestDialog),
    ("ODrive", ODriveDialog),
    ("Configure Odometry", OdometryConfigDialog),
    ("Configure Propulsion controller", PropulsionControllerConfigDialog),
    ("Test propulsion", PropulsionTestDialog),
    ("Scope", ScopeDialog),
    ("Test RPLidar", TestRPLidarDialog),
    ("Test dynamixels", TestDynamixelAx12Dialog),
    ("Test actionneurs", TestActuatorsDialog),
    ("Debug FPGA", DebugFpgaDialog),
    ("Debug Lifts", DebugAsservDialog),
    ("Test sequences", SequencesDialog),
    ("Console", ConsoleDialog),
    ("RecPlayer", RecPlayerDialog)
 ]

class MenuHelper:
    def __init__(self, menu):
        self._actions = []
        self._menu = menu
        
    def addDialog(self, name, dialog):
        action = QAction(name)
        widget = dialog()
        #tools_menu.addAction(action)
        #self._actions.append(action)
        #self._dialogs.append(widget)
        #action.triggered.connect(widget.show)
        
class MainWindow(QMainWindow):
    def __init__(self, options):
        super().__init__(None)

        self._client = ZmqClient(ip=options.robot_ip)
        config.load_config(options.config_path)
        cfg = config.robot_config
        cfg.update_config()        

        # Create actions

        self._action_reset = QAction("Reset")
        self._action_enter_debug = QAction("Debug enter")
        self._action_simulation = QAction("Simulation", checkable=True)
        self._action_upload_config = QAction("Upload config")
        self._action_prematch = QAction("Prematch")
        self._action_start_match = QAction("Start Match")

        self._F5_shortcut = QShortcut(QKeySequence(Qt.Key_F5), self)
        self._F5_shortcut.activated.connect(self._upload_config)

        # Add menu
        tools_menu = self.menuBar().addMenu("Tools")

        self._actions = []
        self._dialogs = []



        for d in dialogs:
            action = QAction(d[0])
            widget = d[1]()
            tools_menu.addAction(action)
            self._actions.append(action)
            self._dialogs.append(widget)
            action.triggered.connect(widget.show)

        tools_menu.addAction(self._action_simulation)
        tools_menu.addAction(self._action_reset)
        tools_menu.addAction(self._action_upload_config)
        tools_menu.addAction(self._action_prematch)
        tools_menu.addAction(self._action_start_match)

        self._main_widget = QWidget()
        self._table_view = TableViewWidget()
        #self._table_view.set_strategy(cfg.strategy)
        self._widget_robot_status = RobotStatusWidget()

        self.setCentralWidget(self._main_widget)

        self.zoomL = QLabel()
        self.zoomL.setText("Zoom")
        self.zoomL.setDisabled(False)

        self.zoomPlusB = QPushButton()
        self.zoomPlusB.setText("+")
        self.zoomPlusB.setDisabled(False)
        self.zoomPlusB.clicked.connect(self._table_view.zoomPlus)

        self.zoomDefB = QPushButton()
        self.zoomDefB.setText("o")
        self.zoomDefB.setDisabled(False)
        self.zoomDefB.clicked.connect(self._table_view.zoomDef)

        self.zoomMinusB = QPushButton()
        self.zoomMinusB.setText("-")
        self.zoomMinusB.setDisabled(False)
        self.zoomMinusB.clicked.connect(self._table_view.zoomMinus)

        self.showThemeC = QCheckBox()
        self.showThemeC.setText("Show Theme")
        self.showThemeC.setDisabled(False)
        self.showThemeC.setChecked(True)
        self.showThemeC.clicked.connect(self.enableThemeDisplay)

        self.clearTelemetryB = QPushButton()
        self.clearTelemetryB.setText("Clear Telemetry")
        self.clearTelemetryB.setDisabled(False)
        self.clearTelemetryB.clicked.connect(self._table_view.clear_telemetry)

        # FIXME : DEBUG : GOLDO
        #self.propulsionTestD = PropulsionTestDialog()

        main_layout = QHBoxLayout()

        status_layout = QVBoxLayout()
        status_layout.addWidget(self._widget_robot_status)

        table_layout = QVBoxLayout()
        table_layout.addWidget(self._table_view)
        table_layout.addStretch(1)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.zoomL)
        right_layout.addWidget(self.zoomPlusB)
        right_layout.addWidget(self.zoomDefB)
        right_layout.addWidget(self.zoomMinusB)
        right_layout.addWidget(self.showThemeC)
        right_layout.addWidget(self.clearTelemetryB)
        # FIXME : DEBUG : GOLDO
        #right_layout.addWidget(self.propulsionTestD)
        right_layout.addStretch(16)

        main_layout.addLayout(status_layout)
        main_layout.addLayout(table_layout)
        main_layout.addLayout(right_layout)

        self._main_widget.setLayout(main_layout)

        self._action_reset.triggered.connect(self._send_reset)
        self._action_enter_debug.triggered.connect(self._send_enter_debug)
        self._action_upload_config.triggered.connect(self._upload_config)
        self._action_prematch.triggered.connect(self._prematch)
        self._action_start_match.triggered.connect(self._start_match)

        self._client.robot_end_load_config_status.connect(self._upload_status)

        for d in self._dialogs:
            d.set_client(self._client)
        # FIXME : DEBUG : GOLDO
        #self.propulsionTestD.set_client(self._client)

        # Add status bar
        self._status_link_state = QLabel('')
        self.statusBar().addWidget(self._status_link_state)
        self._status_match_state = QLabel('')
        self.statusBar().addWidget(self._status_match_state)

        self._client.comm_stats.connect(self._on_comm_stats)
        self._client.match_state_change.connect(self._on_match_state_change)
        self._widget_robot_status.set_client(self._client)
        self._table_view.set_client(self._client)
        
        self._client.camera_image.connect(self._dbg_image)
        
        self._lab = QLabel()
        
        #self._table_view.set_strategy(cfg.strategy)
        #self._table_view.set_config(cfg)
        #self._lab.show()
        #plt = ControlPlots()
        #plt.show()qt display QImage
        
        #self.plt = plt
        #plt.plot_curve([0,2,1])

    def _dbg_image(self, image):
        self._lab.setPixmap(image)

    def _send_reset(self):
        self._client.send_message(message_types.DbgReset, b'')

    def _send_enter_debug(self):
        self._client.send_message(message_types.SetMatchState, struct.pack('<B', 6))

    def _send_exit_debug(self):
        self._client.publishTopic('nucleo/in/match/timer/start', _sym_db.GetSymbol('google.protobuf.Empty')())

    def _on_comm_stats(self, stats):
        self._status_link_state.setText('download {} {}'.format(*stats))

    def _on_match_state_change(self, state,side):
        self._status_match_state.setText('{} {}'.format(state, side))

    def _upload_sequence(self):
        config.load_dynamixels_config()
        config.load_sequence()
        
    def _upload_config(self):
        cfg = config.robot_config
        cfg.update_config()
        #self._table_view.set_strategy(cfg.strategy)
        #self._table_view.set_config(cfg)
        self._client.publishTopic('config/test/put', cfg.robot_config)
        self._client.publishTopic('gui/out/commands/config_nucleo')
        
    def _prematch(self):
        self._client.publishTopic('gui/out/commands/prematch')  
        
    def _start_match(self):
        self._client.publishTopic('gui/out/commands/debug_start_match')  
        
    def _upload_status(self, status):
        if status == True:
            QMessageBox.information(self, "Upload config status", "Success")
            simulation_enable = self._action_simulation.isChecked()
            self._client.publishTopic('nucleo/in/propulsion/simulation/enable', _sym_db.GetSymbol('google.protobuf.BoolValue')(value=simulation_enable))
        else:
            QMessageBox.critical(self, "Upload config status", "Failure")

    def _start_sequence(self):
        self._client.send_message(43, struct.pack('<H',1))

    def enableThemeDisplay(self):
        TableViewWidget.g_show_theme = self.showThemeC.isChecked()
        self._table_view.refreshTheme()
