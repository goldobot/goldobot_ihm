from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QComboBox
from widgets.properties_editor import PropertiesEditorWidget

from messages import OdometryConfig
import message_types
import config
import struct

from widgets.table_view import TableViewWidget


def goldo_debug_seq(sequences,seq,indent):
    for op in seq.ops:
        #print ("   {}".format(op))
        if (op.op in ["propulsion.set_pose"]):
            print (indent + "{}".format(op))
            my_x = int(config.robot_config.sequences.variables[op.args[0].name].default[0]*1000.0)
            my_y = int(config.robot_config.sequences.variables[op.args[0].name].default[1]*1000.0)
            print (indent + "  <x,y> = <{},{}>".format(my_x, my_y))
            TableViewWidget.g_table_view.debug_set_start(my_x, my_y)
        elif (op.op in ["propulsion.set_pose_virtual"]):
            print (indent + "{}".format(op))
            my_x = int(config.robot_config.sequences.variables[op.args[0].name].default[0]*1000.0)
            my_y = int(config.robot_config.sequences.variables[op.args[0].name].default[1]*1000.0)
            print (indent + "  *<x,y> = <{},{}>".format(my_x, my_y))
            TableViewWidget.g_table_view.debug_set_start(my_x, my_y)
        elif (op.op in ["propulsion.move_to", "propulsion.translate", "propulsion.reposition", "propulsion.trajectory"]):
            print (indent + "{}".format(op))
            my_x = int(config.robot_config.sequences.variables[op.args[0].name].default[0]*1000.0)
            my_y = int(config.robot_config.sequences.variables[op.args[0].name].default[1]*1000.0)
            print (indent + "  <x,y> = <{},{}>".format(my_x, my_y))
            TableViewWidget.g_table_view.debug_line_to(my_x, my_y)
        elif (op.op in ["jmp", "jz", "jnz", "je", "jne", "jge", "jl", "jle", "jg", "jge"]):
            #print (indent + "!{}".format(op))
            pass
        elif (op.op in ["call"]):
            #print (indent + "{}".format(op))
            subseq = sequences.sequences[op.args[0].name]
            goldo_debug_seq(sequences,subseq,indent+"  ")
        else:
            #print (indent + ".")
            pass
        
        

class SequencesDialog(QDialog):
    def __init__(self, parent = None):
        super(SequencesDialog, self).__init__(None)
        self._client = None
        self._button_upload = QPushButton('upload')
        self._button_execute = QPushButton('execute')
        self._button_abort = QPushButton('abort')
        self._button_simulate = QPushButton('simulate')
        self._button_clear_simul = QPushButton('clear simul')
        self._combobox_sequence_id = QComboBox()
        
        layout = QGridLayout()        
        layout.addWidget(self._button_upload, 0, 0)
        layout.addWidget(self._button_abort, 0, 1)
        layout.addWidget(self._combobox_sequence_id, 1, 0)
        layout.addWidget(self._button_execute, 1, 1)
        layout.addWidget(self._button_clear_simul, 2, 0)
        layout.addWidget(self._button_simulate, 2, 1)
        self.setLayout(layout)
        self._button_upload.clicked.connect(self._upload)
        self._button_execute.clicked.connect(self._execute)
        self._button_abort.clicked.connect(self._abort)
        self._button_simulate.clicked.connect(self._simulate)
        self._button_clear_simul.clicked.connect(self._clear_simul)
        self._update_sequence_names()
    
        ## FIXME : DEBUG : GOLDO
        #sequences = config.robot_config.sequences
        #for seq_name in sequences.sequences:
        #    print (seq_name)
        #seq = sequences.sequences["match_jaune"]
        #print ("seq 'match_jaune': ")
        #print ("  name        = " + seq.name)
        #print ("  start_index = " + str(seq.start_index))
        ##print ("  variables   : ")
        ##for v in seq.variables:
        ##    print ("    " + v)
        ##print ("  labels      : ")
        ##for l in seq.labels:
        ##    print ("    " + l)
        #print ("  ops         : ")
        #goldo_debug_seq(sequences,seq,"  ")
        

    def set_client(self, client):
        self._client = client
        
    def _update_sequence_names(self):
        sequences = config.robot_config.sequences
        self._combobox_sequence_id.clear()        
        for k in sequences.sequence_names:
            self._combobox_sequence_id.addItem(k)
        
    def _upload(self):
        config.robot_config.update_config()     
        self._update_sequence_names()
        sequences = config.robot_config.sequences
     
            
        buff = sequences.binary

        #Start programming
        self._client.send_message(40, b'')
        #Upload codes by packets
        while len(buff) >32:
            self._client.send_message(42, buff[0:32])
            buff = buff[32:]
        self._client.send_message(42, buff)
        #Finish programming
        self._client.send_message(41, b'')
        
        #upload arms positions
        i = 0
        for n,pos in config.robot_config.dynamixels_positions.items():
            msg = struct.pack('<BB', 0, i)
            msg = msg + b''.join([struct.pack('<H', v) for v in pos])
            self._client.send_message(message_types.DbgArmsSetPose,msg)
            i += 1

    def _execute(self):
        seq_id = self._combobox_sequence_id.currentIndex()
        self._client.send_message(43, struct.pack('<H', seq_id))
        
    def _abort(self):
        self._client.send_message(45, b'')

    def _simulate(self):
        sequences = config.robot_config.sequences
        seq_name = self._combobox_sequence_id.currentText()
        seq = sequences.sequences[seq_name]
        goldo_debug_seq(sequences,seq,"  ")

    def _clear_simul(self):
        TableViewWidget.g_table_view.debug_clear_lines()
        
