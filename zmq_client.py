import zmq
import struct
from PyQt5.QtCore import QObject, QSocketNotifier, pyqtSignal

from messages import PropulsionTelemetry
from messages import PropulsionTelemetryEx
from messages import OdometryConfig
from messages import PropulsionControllerConfig

import message_types

class ZmqClient(QObject):
    heartbeat = pyqtSignal(int)
    debug_gpio = pyqtSignal(int)
    start_of_match = pyqtSignal(int)
    propulsion_telemetry = pyqtSignal(object)
    propulsion_telemetry_ex = pyqtSignal(object)
    odometry_config = pyqtSignal(object)
    propulsion_controller_config = pyqtSignal(object)
    dynamixel_registers = pyqtSignal(int, int, object)
    fpga_registers = pyqtSignal(int, int)

    def __init__(self, ip=None, parent = None):
        super(ZmqClient, self).__init__(None)
        self._context = zmq.Context()

        self._sub_socket = self._context.socket(zmq.SUB)
        self._sub_socket.connect('tcp://{}:3001'.format(ip))
        self._sub_socket.setsockopt(zmq.SUBSCRIBE,b'')

        self._push_socket = self._context.socket(zmq.PUSH)
        self._push_socket.connect('tcp://{}:3002'.format(ip))

        self._notifier = QSocketNotifier(self._sub_socket.getsockopt(zmq.FD), QSocketNotifier.Read, self)
        self._notifier.activated.connect(self._on_sub_socket_event)

    def send_message(self, message_type, message_body):
        self._push_socket.send_multipart([struct.pack('<H',message_type), message_body])

    def _on_sub_socket_event(self):        
        self._notifier.setEnabled(False)

        flags = self._sub_socket.getsockopt(zmq.EVENTS)

        while flags & zmq.POLLIN:
            received = self._sub_socket.recv_multipart()
            self._on_message_received(b''.join(received))
            flags = self._sub_socket.getsockopt(zmq.EVENTS)
        self._notifier.setEnabled(True)

    def _on_message_received(self, msg):
        msg_type = struct.unpack('<H', msg[0:2])[0]

        if msg_type == message_types.Heartbeat:
            timestamp = struct.unpack('<I', msg[2:6])[0]
            self.heartbeat.emit(timestamp)

        if msg_type == message_types.DbgGPIO:
            gpio_mask = struct.unpack('<I', msg[2:6])[0]
            self.debug_gpio.emit(gpio_mask)

        if msg_type == message_types.PropulsionTelemetry:
            telemetry = PropulsionTelemetry(msg[2:])
            self.propulsion_telemetry.emit(telemetry)

        if msg_type == message_types.PropulsionTelemetryEx:
            telemetry = PropulsionTelemetryEx(msg[2:])
            self.propulsion_telemetry_ex.emit(telemetry)

        if msg_type == message_types.StartOfMatch:
            timestamp = struct.unpack('<I', msg[2:6])[0]
            self.start_of_match.emit(timestamp)

# FIXME : DEBUG : GOLDO
#        if msg_type == message_types.CommStats:
#            print(struct.unpack('<HH', msg[2:]))
        if msg_type == message_types.DbgEvent:
            event_type, event_arg1, event_arg2, event_arg3 = struct.unpack('<Iiii', msg[2:])
            if event_type == message_types.DbgEventRobotHoming:
                my_color = "??"
                if event_arg1 == 1:
                    my_color = "Green"
                if event_arg1 == 2:
                    my_color = "Orange"
                print("RobotHoming: " + str(my_color))
            if event_type == message_types.DbgEventStartMatch:
                my_color = "??"
                if event_arg1 == 1:
                    my_color = "Green"
                if event_arg1 == 2:
                    my_color = "Orange"
                print("StartMatch: " + str(my_color))
            if event_type == message_types.DbgEventStartSequence:
                print("StartSequence: " + str(event_arg1))
            if event_type == message_types.DbgEventExecuteCommand:
                if event_arg1 == 8:
                    print("ExecuteCommand: Delay: " + str(event_arg2))
                if event_arg1 == 1:
                    print("ExecuteCommand: SetPose: (%d,%d)"%(event_arg2,event_arg3))
                if event_arg1 == 2:
                    print("ExecuteCommand: Rotation: " + str(event_arg2))
                if event_arg1 == 3:
                    print("ExecuteCommand: PointTo: ??")
                if event_arg1 == 4:
                    print("ExecuteCommand: Trajectory: " + str(event_arg2))
                if event_arg1 == 5:
                    print("ExecuteCommand: Reposition: " + str(event_arg2))
                if event_arg1 == 6:
                    print("ExecuteCommand: ArmsGoToPosition: (id=%d,pos=%d)"%(event_arg2,event_arg3))
                if event_arg1 == 7:
                    print("ExecuteCommand: ArmsExecuteSequence: (id=%d,pos=%d)"%(event_arg2,event_arg3))
            if event_type == message_types.DbgEventGoWaypoint:
                print("  WayPoint: (%d,%d)"%(event_arg1,event_arg2))

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

