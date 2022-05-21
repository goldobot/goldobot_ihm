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

from goldobot_ihm.widgets.table_view import TableViewWidget
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

from .widgets.goldo_1 import Goldo1


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

        self._F5_shortcut = QShortcut(QKeySequence(Qt.Key_F5), self)
        self._F5_shortcut.activated.connect(self._upload_config)

        # FIXME : DEBUG : GOLDO
        self._F6_shortcut = QShortcut(QKeySequence(Qt.Key_F6), self)
        self._F6_shortcut.activated.connect(self._dialogs[5].show)

        self._main_widget = QWidget()
        self._table_view = TableViewWidget()
        #self._table_view.set_strategy(cfg.strategy)
        self._widget_robot_status = RobotStatusWidget()

        self.setCentralWidget(self._main_widget)

       
        main_layout = QHBoxLayout()

        status_layout = QVBoxLayout()
        status_layout.addWidget(self._widget_robot_status)

        table_layout = QVBoxLayout()
        table_layout.addWidget(self._table_view)
        table_layout.addStretch(1)
        
        self._widget_goldo1 = Goldo1(self._client, table_view=self._table_view, parent=self)
        self._table_view._scene.dbg_mouse_info.connect(self._widget_goldo1._update_mouse_dbg)

      

        main_layout.addLayout(status_layout)
        main_layout.addLayout(table_layout)
        main_layout.addWidget(self._widget_goldo1)

        self._main_widget.setLayout(main_layout)


        self._action_upload_config.triggered.connect(self._upload_config)
        self._action_prematch.triggered.connect(self._prematch)
        self._action_start_match.triggered.connect(self._start_match)
        self._action_simulation.toggled.connect(self._set_simulation)

        self._client.robot_end_load_config_status.connect(self._upload_status)

 
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
        
        self._client.camera_image.connect(self._dbg_image)
        
        
        #self._table_view.set_strategy(cfg.strategy)
        #self._table_view.set_config(cfg)
        #self._lab.show()
        #plt = ControlPlots()
        #plt.show()qt display QImage
        
        #self.plt = plt
        #plt.plot_curve([0,2,1])

    def _dbg_image(self, image):
        self._lab.setPixmap(image)

    def _send_exit_debug(self):
        self._client.publishTopic('nucleo/in/match/timer/start', _sym_db.GetSymbol('google.protobuf.Empty')())

    def _on_comm_stats(self, stats):
        self._status_link_state.setText('download {} {}'.format(*stats))

    def _on_match_state_change(self, state,side):
        self._status_match_state.setText('{} {}'.format(state, side))
      
    def _upload_config(self):
        cfg = config.robot_config
        cfg.update_config()
        #self._table_view.set_strategy(cfg.strategy)
        #self._table_view.set_config(cfg)
        self._client.publishTopic('config/test/put', cfg.robot_config)
        self._client.publishTopic('gui/out/commands/config_nucleo')
        
    def _prematch(self):
        purple = 1
        yellow = 2
        self._client.publishTopic('gui/out/side', _sym_db.GetSymbol('google.protobuf.Int32Value')(value=yellow))
        self._client.publishTopic('gui/out/commands/prematch')
        
    def _start_match(self):
        self._client.publishTopic('gui/out/commands/debug_start_match')
        
    def _set_simulation(self, enable):
        self._client.publishTopic('nucleo/in/propulsion/simulation/enable', _sym_db.GetSymbol('google.protobuf.BoolValue')(value=enable))
        
    def _upload_status(self, status):
        if status == True:
            QMessageBox.information(self, "Upload config status", "Success")
            self._set_simulation(self._action_simulation.isChecked())
        else:
            QMessageBox.critical(self, "Upload config status", "Failure")

    def _enable_theme_display(self):
        TableViewWidget.g_show_theme = self.showThemeC.isChecked()
        self._table_view.refreshTheme()

    def _update_mouse_dbg(self, x_mm, y_mm, rel_x_mm, rel_y_mm, d_mm):
        self.posXL.setText(" x: {:>6.1f}".format(x_mm))
        self.posYL.setText(" y: {:>6.1f}".format(y_mm))
        self.posXRL.setText(" xr: {:>6.1f}".format(rel_x_mm))
        self.posYRL.setText(" yr: {:>6.1f}".format(rel_y_mm))
        self.posDRL.setText(" dr: {:>6.1f}".format(d_mm))

    def _start_simulation(self):
        # FIXME : TODO : define "StartSimulation" properly
        #                for now use the "RobotStratDbgStartMatch=2048" message from the "Strat" project
        self._client.send_message_new_header(2048,b'')

    def _pause_simulation(self):
        # FIXME : TODO : define "PauseSimulation" properly
        #                for now use the "RobotStratDbgPauseMatch=2049" message from the "Strat" project
        self._client.send_message_new_header(2049,b'')

    def _resume_simulation(self):
        # FIXME : TODO : define "ResumeSimulation" properly
        #                for now use the "RobotStratDbgResumeMatch=2050" message from the "Strat" project
        self._client.send_message_new_header(2050,b'')

    def _test_astar(self):
        print ("Test A*")
        msg = _sym_db.GetSymbol('google.protobuf.Empty')()
        self._client.publishTopic('robot/test_astar', msg)

