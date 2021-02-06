from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTabWidget

#from widgets.plot_dialog import PlotDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


import google.protobuf as _pb
_sym_db = _pb.symbol_database.Default()

class DebugAsservDialog(QDialog):
    default_Kp_val = 4.0
    default_Ki_val = 0.0625
    default_Kd_val = 1.0
    default_range_val = 4095
    default_clamp_val = 448
    default_bltrig_val = 80
    default_goto_speed_val = 40

    def __init__(self, parent = None):
        super(DebugAsservDialog, self).__init__(None)

        # FIXME : TODO : parametrize
        self.fpga_cmd_reg = 0x80008500

        ctrl_layout = QGridLayout()

        li = 0

        self._button_enable = QPushButton('Enable')
        self._button_enable.setFixedWidth(100)
        ctrl_layout.addWidget(self._button_enable, li, 0)
        self._button_disable = QPushButton('Disable')
        self._button_disable.setFixedWidth(100)
        ctrl_layout.addWidget(self._button_disable, li, 1)
        self._button_reset_error = QPushButton('Reset\nError')
        self._button_reset_error.setFixedWidth(100)
        ctrl_layout.addWidget(self._button_reset_error, li, 2)
        li += 1

        # choko : 3.0 ; 3.3 ; 3.2
        self._label_Kp = QLabel('Kp')
        self._label_Kp.setFixedWidth(100)
        ctrl_layout.addWidget(self._label_Kp, li, 0)
        self._line_edit_Kp = QLineEdit()
        self._line_edit_Kp.setFixedWidth(100)
        self._line_edit_Kp.setText("{:>f}".format(DebugAsservDialog.default_Kp_val))
        ctrl_layout.addWidget(self._line_edit_Kp, li, 1)
        self._button_set_Kp = QPushButton('Set')
        self._button_set_Kp.setFixedWidth(100)
        ctrl_layout.addWidget(self._button_set_Kp, li, 2)
        li += 1

        # choko : 0.01 ; 0.005
        self._label_Ki = QLabel('Ki')
        self._label_Ki.setFixedWidth(100)
        ctrl_layout.addWidget(self._label_Ki, li, 0)
        self._line_edit_Ki = QLineEdit()
        self._line_edit_Ki.setFixedWidth(100)
        self._line_edit_Ki.setText("{:>f}".format(DebugAsservDialog.default_Ki_val))
        ctrl_layout.addWidget(self._line_edit_Ki, li, 1)
        self._button_set_Ki = QPushButton('Set')
        self._button_set_Ki.setFixedWidth(100)
        ctrl_layout.addWidget(self._button_set_Ki, li, 2)
        li += 1

        # choko : 3.0 ; 3.4 ; 3.3
        self._label_Kd = QLabel('Kd')
        self._label_Kd.setFixedWidth(100)
        ctrl_layout.addWidget(self._label_Kd, li, 0)
        self._line_edit_Kd = QLineEdit()
        self._line_edit_Kd.setFixedWidth(100)
        self._line_edit_Kd.setText("{:>f}".format(DebugAsservDialog.default_Kd_val))
        ctrl_layout.addWidget(self._line_edit_Kd, li, 1)
        self._button_set_Kd = QPushButton('Set')
        self._button_set_Kd.setFixedWidth(100)
        ctrl_layout.addWidget(self._button_set_Kd, li, 2)
        li += 1

        self._label_range = QLabel('Range')
        self._label_range.setFixedWidth(100)
        ctrl_layout.addWidget(self._label_range, li, 0)
        self._line_edit_range = QLineEdit()
        self._line_edit_range.setFixedWidth(100)
        self._line_edit_range.setText("{:>d}".format(DebugAsservDialog.default_range_val))
        ctrl_layout.addWidget(self._line_edit_range, li, 1)
        self._button_set_range = QPushButton('Set')
        self._button_set_range.setFixedWidth(100)
        ctrl_layout.addWidget(self._button_set_range, li, 2)
        li += 1

        self._label_clamp = QLabel('Clamp')
        self._label_clamp.setFixedWidth(100)
        ctrl_layout.addWidget(self._label_clamp, li, 0)
        self._line_edit_clamp = QLineEdit()
        self._line_edit_clamp.setFixedWidth(100)
        self._line_edit_clamp.setText("{:>d}".format(DebugAsservDialog.default_clamp_val))
        ctrl_layout.addWidget(self._line_edit_clamp, li, 1)
        self._button_set_clamp = QPushButton('Set')
        self._button_set_clamp.setFixedWidth(100)
        ctrl_layout.addWidget(self._button_set_clamp, li, 2)
        li += 1

        self._label_bltrig = QLabel('Bltrig')
        self._label_bltrig.setFixedWidth(100)
        ctrl_layout.addWidget(self._label_bltrig, li, 0)
        self._line_edit_bltrig = QLineEdit()
        self._line_edit_bltrig.setFixedWidth(100)
        self._line_edit_bltrig.setText("{:>d}".format(DebugAsservDialog.default_bltrig_val))
        ctrl_layout.addWidget(self._line_edit_bltrig, li, 1)
        self._button_set_bltrig = QPushButton('Set')
        self._button_set_bltrig.setFixedWidth(100)
        ctrl_layout.addWidget(self._button_set_bltrig, li, 2)
        li += 1

        self._label_goto_speed = QLabel('Speed')
        self._label_goto_speed.setFixedWidth(100)
        ctrl_layout.addWidget(self._label_goto_speed, li, 0)
        self._line_edit_goto_speed = QLineEdit()
        self._line_edit_goto_speed.setFixedWidth(100)
        self._line_edit_goto_speed.setText("{:>d}".format(DebugAsservDialog.default_goto_speed_val))
        ctrl_layout.addWidget(self._line_edit_goto_speed, li, 1)
        self._button_set_goto_speed = QPushButton('Set')
        self._button_set_goto_speed.setFixedWidth(100)
        ctrl_layout.addWidget(self._button_set_goto_speed, li, 2)
        li += 1

        self._button_homing = QPushButton('Homing')
        self._button_homing.setFixedWidth(100)
        ctrl_layout.addWidget(self._button_homing, li, 0)
        li += 1

        self._label_Target = QLabel('Target')
        self._label_Target.setFixedWidth(100)
        ctrl_layout.addWidget(self._label_Target, li, 0)
        self._line_edit_target = QLineEdit()
        self._line_edit_target.setFixedWidth(100)
        self._line_edit_target.setText("{:>d}".format(1000))
        ctrl_layout.addWidget(self._line_edit_target, li, 1)
        li += 1

        self._button_jump = QPushButton('Jump')
        self._button_jump.setFixedWidth(100)
        ctrl_layout.addWidget(self._button_jump, li, 0)
        self._button_go = QPushButton('Go')
        self._button_go.setFixedWidth(100)
        ctrl_layout.addWidget(self._button_go, li, 1)
        self._button_jump_zero = QPushButton('ZERO!')
        self._button_jump_zero.setFixedWidth(100)
        ctrl_layout.addWidget(self._button_jump_zero, li, 2)
        li += 1

        self._label_Debug = QLabel('DEBUG')
        self._label_Debug.setFixedWidth(100)
        ctrl_layout.addWidget(self._label_Debug, li, 0)
        self._line_edit_debug = QLineEdit()
        self._line_edit_debug.setFixedWidth(100)
        self._line_edit_debug.setText("{:>08x}".format(0))
        ctrl_layout.addWidget(self._line_edit_debug, li, 1)
        self._button_debug = QPushButton('Send debug')
        self._button_debug.setFixedWidth(100)
        ctrl_layout.addWidget(self._button_debug, li, 2)
        li += 1

        #self.setLayout(layout)

        # GRAPH
        # a figure instance to plot on
        self._figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self._canvas = FigureCanvas(self._figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self._toolbar = NavigationToolbar(self._canvas, self)

        # set the layout
        graph_layout = QVBoxLayout()
        graph_layout.addWidget(self._toolbar)
        graph_layout.addWidget(self._canvas)

        global_layout = QHBoxLayout()

        global_layout.addLayout(ctrl_layout)
        global_layout.addLayout(graph_layout)

        self.setLayout(global_layout)

        self._axes = self._figure.add_subplot(111)
        self._ts_plot = []
        self._pos_plot = []

        #self._figure.clf()
        self._axes.plot([0,1000], [   0,   0], '--k')
        self._axes.plot([0,1000], [ 500, 500], '--k')
        self._axes.plot([0,1000], [1000,1000], '--k')
        self._canvas.draw()

        self._button_enable.clicked.connect(lambda:self.cmd_generic("Enable",0x10000001))
        self._button_disable.clicked.connect(lambda:self.cmd_generic("Disable",0x10000000))
        self._button_reset_error.clicked.connect(lambda:self.cmd_generic("Reset error",0xf0000000))
        self._button_set_Kp.clicked.connect(self.set_Kp)
        self._button_set_Ki.clicked.connect(self.set_Ki)
        self._button_set_Kd.clicked.connect(self.set_Kd)
        self._button_set_range.clicked.connect(self.set_range)
        self._button_set_clamp.clicked.connect(self.set_clamp)
        self._button_set_bltrig.clicked.connect(self.set_bltrig)
        self._button_set_goto_speed.clicked.connect(self.set_goto_speed)
        self._button_homing.clicked.connect(lambda:self.cmd_generic("Homing",0x50000000))
        self._button_jump.clicked.connect(self.cmd_jump)
        self._button_jump_zero.clicked.connect(self.cmd_jump_zero)
        self._button_go.clicked.connect(self.cmd_go)
        self._button_debug.clicked.connect(self.cmd_debug)


    def set_client(self, client):
        self._client = client
        self._client.asserv_plot.connect(self._on_asserv_plot)

    def conv_fp_k_cmd(self,v,code):
        nv = int(v*0x10000)
        nv = nv & 0x0fffffff
        nv = nv | code
        return nv

    def cmd_generic(self,cmd_name,val):
        print (cmd_name)
        msg = _sym_db.GetSymbol('goldo.nucleo.fpga.RegWrite')(apb_address = self.fpga_cmd_reg, apb_value = val)
        print ("val = {:>08x}".format(val))
        self._client.publishTopic('nucleo/in/fpga/reg/write', msg)

    def set_Kp(self):
        Kp_float = float(self._line_edit_Kp.text())
        print ("Kp_float = {:>12.6f}".format(Kp_float))
        Kp_cmd = self.conv_fp_k_cmd(Kp_float, 0x20000000)
        print ("Kp_cmd = {:>08x}".format(Kp_cmd))
        msg = _sym_db.GetSymbol('goldo.nucleo.fpga.RegWrite')(apb_address = self.fpga_cmd_reg, apb_value = Kp_cmd)
        self._client.publishTopic('nucleo/in/fpga/reg/write', msg)

    def set_Ki(self):
        Ki_float = float(self._line_edit_Ki.text())
        print ("Ki_float = {:>12.6f}".format(Ki_float))
        Ki_cmd = self.conv_fp_k_cmd(Ki_float, 0x30000000)
        print ("Ki_cmd = {:>08x}".format(Ki_cmd))
        msg = _sym_db.GetSymbol('goldo.nucleo.fpga.RegWrite')(apb_address = self.fpga_cmd_reg, apb_value = Ki_cmd)
        self._client.publishTopic('nucleo/in/fpga/reg/write', msg)

    def set_Kd(self):
        Kd_float = float(self._line_edit_Kd.text())
        print ("Kd_float = {:>12.6f}".format(Kd_float))
        Kd_cmd = self.conv_fp_k_cmd(Kd_float, 0x40000000)
        print ("Kd_cmd = {:>08x}".format(Kd_cmd))
        msg = _sym_db.GetSymbol('goldo.nucleo.fpga.RegWrite')(apb_address = self.fpga_cmd_reg, apb_value = Kd_cmd)
        self._client.publishTopic('nucleo/in/fpga/reg/write', msg)

    def set_range(self):
        new_range = int(self._line_edit_range.text())
        if ((new_range<0) or (new_range>4095)):
            print ("Illegal range : {:d}".format(new_range))
            return
        print ("new_range = {:d}".format(new_range))
        cmd = (new_range<<16) | 0x80000000
        print ("cmd = {:>08x}".format(cmd))
        msg = _sym_db.GetSymbol('goldo.nucleo.fpga.RegWrite')(apb_address = self.fpga_cmd_reg, apb_value = cmd)
        self._client.publishTopic('nucleo/in/fpga/reg/write', msg)

    def set_clamp(self):
        new_clamp = int(self._line_edit_clamp.text())
        if ((new_clamp<0) or (new_clamp>511)):
            print ("Illegal clamp : {:d}".format(new_clamp))
            return
        print ("new_clamp = {:d}".format(new_clamp))
        cmd = (new_clamp) | 0x80000000
        print ("cmd = {:>08x}".format(cmd))
        msg = _sym_db.GetSymbol('goldo.nucleo.fpga.RegWrite')(apb_address = self.fpga_cmd_reg, apb_value = cmd)
        self._client.publishTopic('nucleo/in/fpga/reg/write', msg)

    def set_bltrig(self):
        new_bltrig = int(self._line_edit_bltrig.text())
        if ((new_bltrig<0) or (new_bltrig>4095)):
            print ("Illegal bltrig : {:d}".format(new_bltrig))
            return
        print ("new_bltrig = {:d}".format(new_bltrig))
        cmd = (new_bltrig<<16) | 0x90000000
        print ("cmd = {:>08x}".format(cmd))
        msg = _sym_db.GetSymbol('goldo.nucleo.fpga.RegWrite')(apb_address = self.fpga_cmd_reg, apb_value = cmd)
        self._client.publishTopic('nucleo/in/fpga/reg/write', msg)

    def set_goto_speed(self):
        new_goto_speed = int(self._line_edit_goto_speed.text())
        if ((new_goto_speed<0) or (new_goto_speed>4095)):
            print ("Illegal goto_speed : {:d}".format(new_goto_speed))
            return
        print ("new_goto_speed = {:d}".format(new_goto_speed))
        cmd = (new_goto_speed) | 0x90000000
        print ("cmd = {:>08x}".format(cmd))
        msg = _sym_db.GetSymbol('goldo.nucleo.fpga.RegWrite')(apb_address = self.fpga_cmd_reg, apb_value = cmd)
        self._client.publishTopic('nucleo/in/fpga/reg/write', msg)

    def cmd_jump(self):
        target = int(self._line_edit_target.text())
        print ("Jump to : {:>d}".format(target))
        if (target<0): target += 0x10000000
        cmd = target | 0x60000000
        print ("cmd = {:>08x}".format(cmd))
        msg = _sym_db.GetSymbol('goldo.nucleo.fpga.RegWrite')(apb_address = self.fpga_cmd_reg, apb_value = cmd)
        self._client.publishTopic('nucleo/in/fpga/reg/write', msg)
        self._ts_plot = []
        self._pos_plot = []
        self._axes.plot(self._ts_plot, self._pos_plot, '-')
        self._canvas.draw()

    def cmd_go(self):
        target = int(self._line_edit_target.text())
        print ("Go to : {:>d}".format(target))
        if (target<0): target += 0x10000000
        cmd = target | 0x70000000
        print ("cmd = {:>08x}".format(cmd))
        msg = _sym_db.GetSymbol('goldo.nucleo.fpga.RegWrite')(apb_address = self.fpga_cmd_reg, apb_value = cmd)
        self._client.publishTopic('nucleo/in/fpga/reg/write', msg)

    def cmd_jump_zero(self):
        target = 0
        print ("Jump to : {:>d}".format(target))
        cmd = target | 0x60000000
        print ("cmd = {:>08x}".format(cmd))
        msg = _sym_db.GetSymbol('goldo.nucleo.fpga.RegWrite')(apb_address = self.fpga_cmd_reg, apb_value = cmd)
        self._client.publishTopic('nucleo/in/fpga/reg/write', msg)
        self._ts_plot = []
        self._pos_plot = []
        self._axes.plot(self._ts_plot, self._pos_plot, '-')
        self._canvas.draw()

    def cmd_debug(self):
        cmd = int(self._line_edit_debug.text(),16)
        print ("DEBUG : {:>08x}".format(cmd))
        msg = _sym_db.GetSymbol('goldo.nucleo.fpga.RegWrite')(apb_address = self.fpga_cmd_reg, apb_value = cmd)
        self._client.publishTopic('nucleo/in/fpga/reg/write', msg)

    def _on_asserv_plot(self, ts, pos):
        print (" {} {}".format(ts, pos))
        if ((ts>0) and (ts<1000)):
            self._ts_plot.append(ts)
            self._pos_plot.append(pos)
        if ((ts>895) and (ts<905)):
            self._axes.plot(self._ts_plot, self._pos_plot, '-')
        self._canvas.draw()

        
