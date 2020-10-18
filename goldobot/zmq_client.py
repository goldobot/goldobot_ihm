import zmq
import struct
from PyQt5.QtCore import QObject, QSocketNotifier, pyqtSignal
from PyQt5.QtGui import QPixmap

from goldobot.messages import NucleoFirmwareVersion
from goldobot.messages import PropulsionTelemetry
from goldobot.messages import PropulsionTelemetryEx
from goldobot.messages import RplidarPlot
from goldobot.messages import RplidarRobotDetection
from goldobot.messages import OdometryConfig
from goldobot.messages import PropulsionControllerConfig

from goldobot import message_types

import goldobot.pb2 as _goldo_pb2

import google.protobuf as _pb
_sym_db = _pb.symbol_database.Default()

class ZmqClient(QObject):
    nucleo_firmware_version = pyqtSignal(str)
    message_received = pyqtSignal(object)
    heartbeat = pyqtSignal(int)
    start_of_match = pyqtSignal(int)
    match_state_change = pyqtSignal(int,int)
    comm_stats = pyqtSignal(object)
    propulsion_telemetry = pyqtSignal(object)
    propulsion_telemetry_ex = pyqtSignal(object)
    rplidar_plot = pyqtSignal(object)
    rplidar_robot_detection = pyqtSignal(object)
    astar_dbg_map = pyqtSignal(object)
    odometry_config = pyqtSignal(object)
    propulsion_controller_config = pyqtSignal(object)
    dynamixel_registers = pyqtSignal(int, int, object)
    fpga_registers = pyqtSignal(int, int)
    fpga_registers_crc = pyqtSignal(int, int, int)
    sensors = pyqtSignal(int)
    gpio = pyqtSignal(int)
    debug_goldo = pyqtSignal(int)
    robot_end_load_config_status = pyqtSignal(bool)
    sequence_event = pyqtSignal(int, object)
    odrive_response = pyqtSignal(int, bytes)
    camera_image = pyqtSignal(object)

    def __init__(self, ip=None, parent = None):
        super(ZmqClient, self).__init__(None)
        self._context = zmq.Context()

        self._sub_socket = self._context.socket(zmq.SUB)
        self._sub_socket.connect('tcp://{}:3001'.format(ip))
        self._sub_socket.setsockopt(zmq.SUBSCRIBE,b'')

        self._sub_socket_rplidar = self._context.socket(zmq.SUB)
        self._sub_socket_rplidar.connect('tcp://{}:3101'.format(ip))
        self._sub_socket_rplidar.setsockopt(zmq.SUBSCRIBE,b'')
        
        self._push_socket = self._context.socket(zmq.PUB)
        self._push_socket.connect('tcp://{}:3002'.format(ip))

        self._push_socket_rplidar = self._context.socket(zmq.PUB)
        self._push_socket_rplidar.connect('tcp://{}:3102'.format(ip))

        self._notifier = QSocketNotifier(self._sub_socket.getsockopt(zmq.FD), QSocketNotifier.Read, self)
        self._notifier.activated.connect(self._on_sub_socket_event)

        self._notifier_rplidar = QSocketNotifier(self._sub_socket_rplidar.getsockopt(zmq.FD), QSocketNotifier.Read, self)
        self._notifier_rplidar.activated.connect(self._on_sub_socket_rplidar_event)
               
        self._socket_main_sub = self._context.socket(zmq.SUB)
        self._socket_main_sub.connect('tcp://{}:3801'.format(ip))
        self._socket_main_sub.setsockopt(zmq.SUBSCRIBE,b'')
        
        self._socket_main_pub = self._context.socket(zmq.PUB)
        self._socket_main_pub.connect('tcp://{}:3802'.format(ip))
        
        self._notifier_main = QSocketNotifier(self._socket_main_sub.getsockopt(zmq.FD), QSocketNotifier.Read, self)
        self._notifier_main.activated.connect(self._on_socket_main_sub)
        
        self.odrive_buff = b''
        self.odrive_seq = 129

    def send_message(self, message_type, message_body):
        self._push_socket.send_multipart([struct.pack('<H',message_type), message_body])
        
    def publishTopic(self, topic, msg):
        self._socket_main_pub.send_multipart([topic.encode('utf8'),
                                              msg.DESCRIPTOR.full_name.encode('utf8'),
                                              msg.SerializeToString()])
                                              
    def _on_socket_main_sub(self):        
        self._notifier_main.setEnabled(False)
        socket = self._socket_main_sub
        flags = socket.getsockopt(zmq.EVENTS)
        while flags & zmq.POLLIN:
            topic, full_name, payload = socket.recv_multipart()
            flags = socket.getsockopt(zmq.EVENTS)
            topic = topic.decode('utf8')
            full_name = full_name.decode('utf8')
            
            msg_class = _sym_db.GetSymbol(full_name)
            if msg_class is not None:
                msg = msg_class()
                msg.ParseFromString(payload)
            else:
                msg = None
            if topic == 'nucleo/out/os/heartbeat':
                self.heartbeat.emit(msg.timestamp)
            if topic == 'nucleo/out/robot/config/load_status':
                self.robot_end_load_config_status.emit(msg.status==0)
        self._notifier_main.setEnabled(True)

    def send_message_rplidar(self, message_type, message_body):
        print("= send_message_rplidar ========================")
        print("message_type = {}".format(message_type))
        dbg_msg = struct.pack('<H',message_type) + message_body
        hexdump(dbg_msg)
        print("===============================================")
        print()

        self._push_socket_rplidar.send_multipart([struct.pack('<H',message_type), message_body])
    
    def send_message_odrive(self, endpoint_id, expected_response_size, payload, protocol_version):
        seq = self.odrive_seq
        self.odrive_seq += 1
        msg = _sym_db.GetSymbol('goldo.nucleo.odrive.Request')
        msg.sequence_number = seq
        msg.endpoint_id = endpoint_id
        msg.expected_response_size = expected_response_size
        msg.payload = payload
        msg.protocol_version = protocol_version        
        self.publishTopic('nucleo/in/odrive/request', msg)
        return seq
        
        
    def _on_sub_socket_event(self):        
        self._notifier.setEnabled(False)
        flags = self._sub_socket.getsockopt(zmq.EVENTS)
        while flags & zmq.POLLIN:
            received = self._sub_socket.recv_multipart()
            self._on_message_received(b''.join(received))
            flags = self._sub_socket.getsockopt(zmq.EVENTS)
        self._notifier.setEnabled(True)
        
    def _on_sub_socket_camera_image_event(self):        
        self._notifier_camera_image.setEnabled(False)

        flags = self._sub_socket_camera_image.getsockopt(zmq.EVENTS)
        while flags & zmq.POLLIN:
            topic, body = self._sub_socket_camera_image.recv_multipart()
            print(topic)
            image_msg = Image()
            image_msg.ParseFromString(body)
            flags = self._sub_socket_camera_image.getsockopt(zmq.EVENTS)
            image = QPixmap()
            image.loadFromData(image_msg.data)
            self.camera_image.emit(image)
        self._notifier_camera_image.setEnabled(True)

    def _on_sub_socket_rplidar_event(self):        
        self._notifier_rplidar.setEnabled(False)
        flags = self._sub_socket_rplidar.getsockopt(zmq.EVENTS)
        while flags & zmq.POLLIN:
            received = self._sub_socket_rplidar.recv_multipart()
            self._on_message_received(b''.join(received))
            flags = self._sub_socket_rplidar.getsockopt(zmq.EVENTS)
        self._notifier_rplidar.setEnabled(True)

    def _on_message_received(self, msg):
        return
        self.message_received.emit(msg)
        msg_type = struct.unpack('<H', msg[0:2])[0]

        if msg_type == message_types.GetNucleoFirmwareVersion:
            firm_ver = NucleoFirmwareVersion(msg[2:])
            #print("firm_ver : " + firm_ver.s)
            self.nucleo_firmware_version.emit(firm_ver.s)

        if msg_type == message_types.SensorsChange:
            self.sensors.emit(struct.unpack('<I',msg[2:])[0])
        if msg_type == message_types.GPIODebug:
            self.gpio.emit(struct.unpack('<I',msg[2:])[0])
        if msg_type == message_types.SequenceEvent:
            event_id = struct.unpack('<B',msg[2:3])[0]
            self.sequence_event.emit(event_id, msg[3:])
            print(event_id, msg[3:])
        if msg_type == message_types.DebugGoldo:
            self.debug_goldo.emit(struct.unpack('<I',msg[2:])[0])
            
        if msg_type == message_types.MainSequenceLoadStatus:
            status = bool(struct.unpack('<B',msg[2:]))
            print('sequence loaded, status: ', status)
            
           
        if msg_type == message_types.MatchStateChange:
            state,side = struct.unpack('<BB', msg[2:4])
            self.match_state_change.emit(state,side)

        if msg_type == message_types.PropulsionTelemetry:
            telemetry = PropulsionTelemetry(msg[2:])
            self.propulsion_telemetry.emit(telemetry)

        if msg_type == message_types.PropulsionTelemetryEx:
            telemetry = PropulsionTelemetryEx(msg[2:])
            self.propulsion_telemetry_ex.emit(telemetry)

        if msg_type == message_types.RplidarPlot:
            my_plot = RplidarPlot(msg[2:])
            self.rplidar_plot.emit(my_plot)

        if msg_type == message_types.RplidarRobotDetection:
            other_robot = RplidarRobotDetection(msg[2:])
            self.rplidar_robot_detection.emit(other_robot)

        if msg_type == message_types.RobotStratDbgAstarMap:
            astar_dbg_map_bytes = msg[3:]
            self.astar_dbg_map.emit(astar_dbg_map_bytes)

        if msg_type == message_types.StartOfMatch:
            timestamp = struct.unpack('<I', msg[2:6])[0]
            self.start_of_match.emit(timestamp)

        if msg_type == message_types.CommStats:
            #self.comm_stats.emit(struct.unpack('<HHIIIII', msg[2:]))
            pass

        if msg_type == message_types.DbgGetOdometryConfig:
            self.odometry_config.emit(OdometryConfig(msg[2:]))

        if msg_type == message_types.DbgGetPropulsionConfig:
            self.propulsion_controller_config.emit(PropulsionControllerConfig(msg[2:]))

        if msg_type == message_types.DbgDynamixelGetRegisters:
            id_, address = struct.unpack('<BB', msg[2:4])
            self.dynamixel_registers.emit(id_, address, msg[4:])

        if msg_type == message_types.FpgaDbgReadReg:
            apb_addr, apb_data = struct.unpack('<II', msg[2:])
            self.fpga_registers.emit(apb_addr, apb_data)
            
        if msg_type == message_types.FpgaDbgReadRegCrc:
            apb_addr, apb_data, crc = struct.unpack('<III', msg[2:])
            self.fpga_registers_crc.emit(apb_addr, apb_data, crc)
            
        if msg_type == message_types.FpgaDbgGetErrCnt:
            v = struct.unpack('<'+'I'*16, msg[2:])

            
        if msg_type == message_types.NucleoLog:
            log = msg[2:].split(bytes([0]),1)[0].decode("utf-8")
            print("" + log)

        if msg_type == 90:
            print(struct.unpack('<BB', msg[2:]))
        if msg_type == 411:
            seq = struct.unpack('<H', msg[2:4])[0] & 0xf7fff
            self.odrive_response.emit(seq, msg[4:])