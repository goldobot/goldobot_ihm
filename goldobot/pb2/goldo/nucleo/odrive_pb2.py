# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: goldo/nucleo/odrive.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from goldo import pb2_options_pb2 as goldo_dot_pb2__options__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='goldo/nucleo/odrive.proto',
  package='goldo.nucleo.odrive',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x19goldo/nucleo/odrive.proto\x12\x13goldo.nucleo.odrive\x1a\x17goldo/pb2_options.proto\"\xa0\x01\n\rRequestPacket\x12\x1d\n\x0fsequence_number\x18\x01 \x01(\rB\x04\x80\xb5\x18\x05\x12\x19\n\x0b\x65ndpoint_id\x18\x02 \x01(\rB\x04\x80\xb5\x18\x05\x12$\n\x16\x65xpected_response_size\x18\x03 \x01(\rB\x04\x80\xb5\x18\x05\x12\x0f\n\x07payload\x18\x04 \x01(\x0c\x12\x1e\n\x10protocol_version\x18\x05 \x01(\rB\x04\x80\xb5\x18\x05\"@\n\x0eResponsePacket\x12\x1d\n\x0fsequence_number\x18\x01 \x01(\rB\x04\x80\xb5\x18\x05\x12\x0f\n\x07payload\x18\x04 \x01(\x0c\"X\n\rAxisTelemetry\x12\x14\n\x0cpos_estimate\x18\x01 \x01(\x02\x12\x14\n\x0cvel_estimate\x18\x02 \x01(\x02\x12\x1b\n\x13\x63urrent_iq_setpoint\x18\x03 \x01(\x02\"\x8e\x01\n\x0e\x41xisErrorState\x12\x12\n\x04\x61xis\x18\x01 \x01(\rB\x04\x80\xb5\x18\x07\x12\x13\n\x05motor\x18\x02 \x01(\rB\x04\x80\xb5\x18\x07\x12\x18\n\ncontroller\x18\x03 \x01(\rB\x04\x80\xb5\x18\x07\x12\x15\n\x07\x65ncoder\x18\x04 \x01(\rB\x04\x80\xb5\x18\x07\x12\"\n\x14sensorless_estimator\x18\x05 \x01(\rB\x04\x80\xb5\x18\x07\"\xc6\x01\n\nAxisState_\x12;\n\rcurrent_state\x18\x01 \x01(\x0e\x32\x1e.goldo.nucleo.odrive.AxisStateB\x04\x80\xb5\x18\x07\x12=\n\x0frequested_state\x18\x02 \x01(\x0e\x32\x1e.goldo.nucleo.odrive.AxisStateB\x04\x80\xb5\x18\x07\x12<\n\x0c\x63ontrol_mode\x18\x03 \x01(\x0e\x32 .goldo.nucleo.odrive.ControlModeB\x04\x80\xb5\x18\x07\"y\n\x0f\x41xisErrorStates\x12\x32\n\x05\x61xis0\x18\x01 \x01(\x0b\x32#.goldo.nucleo.odrive.AxisErrorState\x12\x32\n\x05\x61xis1\x18\x02 \x01(\x0b\x32#.goldo.nucleo.odrive.AxisErrorState\"l\n\nAxisStates\x12.\n\x05\x61xis0\x18\x01 \x01(\x0b\x32\x1f.goldo.nucleo.odrive.AxisState_\x12.\n\x05\x61xis1\x18\x02 \x01(\x0b\x32\x1f.goldo.nucleo.odrive.AxisState_\"w\n\x10\x43lientStatistics\x12\x19\n\x0bmax_latency\x18\x01 \x01(\rB\x04\x80\xb5\x18\x05\x12\x1c\n\x0etimeout_errors\x18\x02 \x01(\rB\x04\x80\xb5\x18\x05\x12\x14\n\x06uptime\x18\x03 \x01(\rB\x04\x80\xb5\x18\x07\x12\x14\n\x0csynchronized\x18\x04 \x01(\x08\"\xe9\x01\n\nAxisStatus\x12\x35\n\rcurrent_state\x18\x01 \x01(\x0e\x32\x1e.goldo.nucleo.odrive.AxisState\x12\x37\n\x0frequested_state\x18\x02 \x01(\x0e\x32\x1e.goldo.nucleo.odrive.AxisState\x12\x36\n\x0c\x63ontrol_mode\x18\x03 \x01(\x0e\x32 .goldo.nucleo.odrive.ControlMode\x12\x33\n\x06\x65rrors\x18\x04 \x01(\x0b\x32#.goldo.nucleo.odrive.AxisErrorState\"`\n\tTelemetry\x12\x17\n\ttimestamp\x18\x01 \x01(\rB\x04\x80\xb5\x18\x07\x12:\n\x04\x61xis\x18\x02 \x03(\x0b\x32\".goldo.nucleo.odrive.AxisTelemetryB\x08\x88\xb5\x18\x02\x90\xb5\x18\x01\"\xc6\x01\n\x0cODriveStatus\x12\x14\n\x0csynchronized\x18\x01 \x01(\x08\x12.\n\x05\x61xis0\x18\x02 \x01(\x0b\x32\x1f.goldo.nucleo.odrive.AxisStatus\x12.\n\x05\x61xis1\x18\x03 \x01(\x0b\x32\x1f.goldo.nucleo.odrive.AxisStatus\x12@\n\x11\x63lient_statistics\x18\x04 \x01(\x0b\x32%.goldo.nucleo.odrive.ClientStatistics*\x8e\x02\n\tAxisState\x12\r\n\tUNDEFINED\x10\x00\x12\x08\n\x04IDLE\x10\x01\x12\x14\n\x10STARTUP_SEQUENCE\x10\x02\x12\x1d\n\x19\x46ULL_CALIBRATION_SEQUENCE\x10\x03\x12\x15\n\x11MOTOR_CALIBRATION\x10\x04\x12\x16\n\x12SENSORLESS_CONTROL\x10\x05\x12\x18\n\x14\x45NCODER_INDEX_SEARCH\x10\x06\x12\x1e\n\x1a\x45NCODER_OFFSET_CALIBRATION\x10\x07\x12\x17\n\x13\x43LOSED_LOOP_CONTROL\x10\x08\x12\x0f\n\x0bLOCKIN_SPIN\x10\t\x12\x14\n\x10\x45NCODER_DIR_FIND\x10\n\x12\n\n\x06HOMING\x10\x0b*b\n\x0b\x43ontrolMode\x12\x13\n\x0fVOLTAGE_CONTROL\x10\x00\x12\x12\n\x0eTORQUE_CONTROL\x10\x01\x12\x14\n\x10VELOCITY_CONTROL\x10\x02\x12\x14\n\x10POSITION_CONTROL\x10\x03\x62\x06proto3')
  ,
  dependencies=[goldo_dot_pb2__options__pb2.DESCRIPTOR,])

_AXISSTATE = _descriptor.EnumDescriptor(
  name='AxisState',
  full_name='goldo.nucleo.odrive.AxisState',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNDEFINED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='IDLE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STARTUP_SEQUENCE', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FULL_CALIBRATION_SEQUENCE', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MOTOR_CALIBRATION', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SENSORLESS_CONTROL', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ENCODER_INDEX_SEARCH', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ENCODER_OFFSET_CALIBRATION', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CLOSED_LOOP_CONTROL', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LOCKIN_SPIN', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ENCODER_DIR_FIND', index=10, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HOMING', index=11, number=11,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1630,
  serialized_end=1900,
)
_sym_db.RegisterEnumDescriptor(_AXISSTATE)

AxisState = enum_type_wrapper.EnumTypeWrapper(_AXISSTATE)
_CONTROLMODE = _descriptor.EnumDescriptor(
  name='ControlMode',
  full_name='goldo.nucleo.odrive.ControlMode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='VOLTAGE_CONTROL', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TORQUE_CONTROL', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VELOCITY_CONTROL', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='POSITION_CONTROL', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1902,
  serialized_end=2000,
)
_sym_db.RegisterEnumDescriptor(_CONTROLMODE)

ControlMode = enum_type_wrapper.EnumTypeWrapper(_CONTROLMODE)
UNDEFINED = 0
IDLE = 1
STARTUP_SEQUENCE = 2
FULL_CALIBRATION_SEQUENCE = 3
MOTOR_CALIBRATION = 4
SENSORLESS_CONTROL = 5
ENCODER_INDEX_SEARCH = 6
ENCODER_OFFSET_CALIBRATION = 7
CLOSED_LOOP_CONTROL = 8
LOCKIN_SPIN = 9
ENCODER_DIR_FIND = 10
HOMING = 11
VOLTAGE_CONTROL = 0
TORQUE_CONTROL = 1
VELOCITY_CONTROL = 2
POSITION_CONTROL = 3



_REQUESTPACKET = _descriptor.Descriptor(
  name='RequestPacket',
  full_name='goldo.nucleo.odrive.RequestPacket',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sequence_number', full_name='goldo.nucleo.odrive.RequestPacket.sequence_number', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\200\265\030\005'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='endpoint_id', full_name='goldo.nucleo.odrive.RequestPacket.endpoint_id', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\200\265\030\005'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='expected_response_size', full_name='goldo.nucleo.odrive.RequestPacket.expected_response_size', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\200\265\030\005'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='payload', full_name='goldo.nucleo.odrive.RequestPacket.payload', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='protocol_version', full_name='goldo.nucleo.odrive.RequestPacket.protocol_version', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\200\265\030\005'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=76,
  serialized_end=236,
)


_RESPONSEPACKET = _descriptor.Descriptor(
  name='ResponsePacket',
  full_name='goldo.nucleo.odrive.ResponsePacket',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sequence_number', full_name='goldo.nucleo.odrive.ResponsePacket.sequence_number', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\200\265\030\005'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='payload', full_name='goldo.nucleo.odrive.ResponsePacket.payload', index=1,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=238,
  serialized_end=302,
)


_AXISTELEMETRY = _descriptor.Descriptor(
  name='AxisTelemetry',
  full_name='goldo.nucleo.odrive.AxisTelemetry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pos_estimate', full_name='goldo.nucleo.odrive.AxisTelemetry.pos_estimate', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='vel_estimate', full_name='goldo.nucleo.odrive.AxisTelemetry.vel_estimate', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='current_iq_setpoint', full_name='goldo.nucleo.odrive.AxisTelemetry.current_iq_setpoint', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=304,
  serialized_end=392,
)


_AXISERRORSTATE = _descriptor.Descriptor(
  name='AxisErrorState',
  full_name='goldo.nucleo.odrive.AxisErrorState',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='axis', full_name='goldo.nucleo.odrive.AxisErrorState.axis', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\200\265\030\007'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='motor', full_name='goldo.nucleo.odrive.AxisErrorState.motor', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\200\265\030\007'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='controller', full_name='goldo.nucleo.odrive.AxisErrorState.controller', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\200\265\030\007'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='encoder', full_name='goldo.nucleo.odrive.AxisErrorState.encoder', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\200\265\030\007'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sensorless_estimator', full_name='goldo.nucleo.odrive.AxisErrorState.sensorless_estimator', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\200\265\030\007'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=395,
  serialized_end=537,
)


_AXISSTATE_ = _descriptor.Descriptor(
  name='AxisState_',
  full_name='goldo.nucleo.odrive.AxisState_',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='current_state', full_name='goldo.nucleo.odrive.AxisState_.current_state', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\200\265\030\007'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='requested_state', full_name='goldo.nucleo.odrive.AxisState_.requested_state', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\200\265\030\007'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='control_mode', full_name='goldo.nucleo.odrive.AxisState_.control_mode', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\200\265\030\007'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=540,
  serialized_end=738,
)


_AXISERRORSTATES = _descriptor.Descriptor(
  name='AxisErrorStates',
  full_name='goldo.nucleo.odrive.AxisErrorStates',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='axis0', full_name='goldo.nucleo.odrive.AxisErrorStates.axis0', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='axis1', full_name='goldo.nucleo.odrive.AxisErrorStates.axis1', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=740,
  serialized_end=861,
)


_AXISSTATES = _descriptor.Descriptor(
  name='AxisStates',
  full_name='goldo.nucleo.odrive.AxisStates',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='axis0', full_name='goldo.nucleo.odrive.AxisStates.axis0', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='axis1', full_name='goldo.nucleo.odrive.AxisStates.axis1', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=863,
  serialized_end=971,
)


_CLIENTSTATISTICS = _descriptor.Descriptor(
  name='ClientStatistics',
  full_name='goldo.nucleo.odrive.ClientStatistics',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='max_latency', full_name='goldo.nucleo.odrive.ClientStatistics.max_latency', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\200\265\030\005'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timeout_errors', full_name='goldo.nucleo.odrive.ClientStatistics.timeout_errors', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\200\265\030\005'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='uptime', full_name='goldo.nucleo.odrive.ClientStatistics.uptime', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\200\265\030\007'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='synchronized', full_name='goldo.nucleo.odrive.ClientStatistics.synchronized', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=973,
  serialized_end=1092,
)


_AXISSTATUS = _descriptor.Descriptor(
  name='AxisStatus',
  full_name='goldo.nucleo.odrive.AxisStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='current_state', full_name='goldo.nucleo.odrive.AxisStatus.current_state', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='requested_state', full_name='goldo.nucleo.odrive.AxisStatus.requested_state', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='control_mode', full_name='goldo.nucleo.odrive.AxisStatus.control_mode', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='errors', full_name='goldo.nucleo.odrive.AxisStatus.errors', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1095,
  serialized_end=1328,
)


_TELEMETRY = _descriptor.Descriptor(
  name='Telemetry',
  full_name='goldo.nucleo.odrive.Telemetry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='goldo.nucleo.odrive.Telemetry.timestamp', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\200\265\030\007'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='axis', full_name='goldo.nucleo.odrive.Telemetry.axis', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\210\265\030\002\220\265\030\001'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1330,
  serialized_end=1426,
)


_ODRIVESTATUS = _descriptor.Descriptor(
  name='ODriveStatus',
  full_name='goldo.nucleo.odrive.ODriveStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='synchronized', full_name='goldo.nucleo.odrive.ODriveStatus.synchronized', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='axis0', full_name='goldo.nucleo.odrive.ODriveStatus.axis0', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='axis1', full_name='goldo.nucleo.odrive.ODriveStatus.axis1', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='client_statistics', full_name='goldo.nucleo.odrive.ODriveStatus.client_statistics', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1429,
  serialized_end=1627,
)

_AXISSTATE_.fields_by_name['current_state'].enum_type = _AXISSTATE
_AXISSTATE_.fields_by_name['requested_state'].enum_type = _AXISSTATE
_AXISSTATE_.fields_by_name['control_mode'].enum_type = _CONTROLMODE
_AXISERRORSTATES.fields_by_name['axis0'].message_type = _AXISERRORSTATE
_AXISERRORSTATES.fields_by_name['axis1'].message_type = _AXISERRORSTATE
_AXISSTATES.fields_by_name['axis0'].message_type = _AXISSTATE_
_AXISSTATES.fields_by_name['axis1'].message_type = _AXISSTATE_
_AXISSTATUS.fields_by_name['current_state'].enum_type = _AXISSTATE
_AXISSTATUS.fields_by_name['requested_state'].enum_type = _AXISSTATE
_AXISSTATUS.fields_by_name['control_mode'].enum_type = _CONTROLMODE
_AXISSTATUS.fields_by_name['errors'].message_type = _AXISERRORSTATE
_TELEMETRY.fields_by_name['axis'].message_type = _AXISTELEMETRY
_ODRIVESTATUS.fields_by_name['axis0'].message_type = _AXISSTATUS
_ODRIVESTATUS.fields_by_name['axis1'].message_type = _AXISSTATUS
_ODRIVESTATUS.fields_by_name['client_statistics'].message_type = _CLIENTSTATISTICS
DESCRIPTOR.message_types_by_name['RequestPacket'] = _REQUESTPACKET
DESCRIPTOR.message_types_by_name['ResponsePacket'] = _RESPONSEPACKET
DESCRIPTOR.message_types_by_name['AxisTelemetry'] = _AXISTELEMETRY
DESCRIPTOR.message_types_by_name['AxisErrorState'] = _AXISERRORSTATE
DESCRIPTOR.message_types_by_name['AxisState_'] = _AXISSTATE_
DESCRIPTOR.message_types_by_name['AxisErrorStates'] = _AXISERRORSTATES
DESCRIPTOR.message_types_by_name['AxisStates'] = _AXISSTATES
DESCRIPTOR.message_types_by_name['ClientStatistics'] = _CLIENTSTATISTICS
DESCRIPTOR.message_types_by_name['AxisStatus'] = _AXISSTATUS
DESCRIPTOR.message_types_by_name['Telemetry'] = _TELEMETRY
DESCRIPTOR.message_types_by_name['ODriveStatus'] = _ODRIVESTATUS
DESCRIPTOR.enum_types_by_name['AxisState'] = _AXISSTATE
DESCRIPTOR.enum_types_by_name['ControlMode'] = _CONTROLMODE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RequestPacket = _reflection.GeneratedProtocolMessageType('RequestPacket', (_message.Message,), dict(
  DESCRIPTOR = _REQUESTPACKET,
  __module__ = 'goldo.nucleo.odrive_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.odrive.RequestPacket)
  ))
_sym_db.RegisterMessage(RequestPacket)

ResponsePacket = _reflection.GeneratedProtocolMessageType('ResponsePacket', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSEPACKET,
  __module__ = 'goldo.nucleo.odrive_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.odrive.ResponsePacket)
  ))
_sym_db.RegisterMessage(ResponsePacket)

AxisTelemetry = _reflection.GeneratedProtocolMessageType('AxisTelemetry', (_message.Message,), dict(
  DESCRIPTOR = _AXISTELEMETRY,
  __module__ = 'goldo.nucleo.odrive_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.odrive.AxisTelemetry)
  ))
_sym_db.RegisterMessage(AxisTelemetry)

AxisErrorState = _reflection.GeneratedProtocolMessageType('AxisErrorState', (_message.Message,), dict(
  DESCRIPTOR = _AXISERRORSTATE,
  __module__ = 'goldo.nucleo.odrive_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.odrive.AxisErrorState)
  ))
_sym_db.RegisterMessage(AxisErrorState)

AxisState_ = _reflection.GeneratedProtocolMessageType('AxisState_', (_message.Message,), dict(
  DESCRIPTOR = _AXISSTATE_,
  __module__ = 'goldo.nucleo.odrive_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.odrive.AxisState_)
  ))
_sym_db.RegisterMessage(AxisState_)

AxisErrorStates = _reflection.GeneratedProtocolMessageType('AxisErrorStates', (_message.Message,), dict(
  DESCRIPTOR = _AXISERRORSTATES,
  __module__ = 'goldo.nucleo.odrive_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.odrive.AxisErrorStates)
  ))
_sym_db.RegisterMessage(AxisErrorStates)

AxisStates = _reflection.GeneratedProtocolMessageType('AxisStates', (_message.Message,), dict(
  DESCRIPTOR = _AXISSTATES,
  __module__ = 'goldo.nucleo.odrive_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.odrive.AxisStates)
  ))
_sym_db.RegisterMessage(AxisStates)

ClientStatistics = _reflection.GeneratedProtocolMessageType('ClientStatistics', (_message.Message,), dict(
  DESCRIPTOR = _CLIENTSTATISTICS,
  __module__ = 'goldo.nucleo.odrive_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.odrive.ClientStatistics)
  ))
_sym_db.RegisterMessage(ClientStatistics)

AxisStatus = _reflection.GeneratedProtocolMessageType('AxisStatus', (_message.Message,), dict(
  DESCRIPTOR = _AXISSTATUS,
  __module__ = 'goldo.nucleo.odrive_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.odrive.AxisStatus)
  ))
_sym_db.RegisterMessage(AxisStatus)

Telemetry = _reflection.GeneratedProtocolMessageType('Telemetry', (_message.Message,), dict(
  DESCRIPTOR = _TELEMETRY,
  __module__ = 'goldo.nucleo.odrive_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.odrive.Telemetry)
  ))
_sym_db.RegisterMessage(Telemetry)

ODriveStatus = _reflection.GeneratedProtocolMessageType('ODriveStatus', (_message.Message,), dict(
  DESCRIPTOR = _ODRIVESTATUS,
  __module__ = 'goldo.nucleo.odrive_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.odrive.ODriveStatus)
  ))
_sym_db.RegisterMessage(ODriveStatus)


_REQUESTPACKET.fields_by_name['sequence_number']._options = None
_REQUESTPACKET.fields_by_name['endpoint_id']._options = None
_REQUESTPACKET.fields_by_name['expected_response_size']._options = None
_REQUESTPACKET.fields_by_name['protocol_version']._options = None
_RESPONSEPACKET.fields_by_name['sequence_number']._options = None
_AXISERRORSTATE.fields_by_name['axis']._options = None
_AXISERRORSTATE.fields_by_name['motor']._options = None
_AXISERRORSTATE.fields_by_name['controller']._options = None
_AXISERRORSTATE.fields_by_name['encoder']._options = None
_AXISERRORSTATE.fields_by_name['sensorless_estimator']._options = None
_AXISSTATE_.fields_by_name['current_state']._options = None
_AXISSTATE_.fields_by_name['requested_state']._options = None
_AXISSTATE_.fields_by_name['control_mode']._options = None
_CLIENTSTATISTICS.fields_by_name['max_latency']._options = None
_CLIENTSTATISTICS.fields_by_name['timeout_errors']._options = None
_CLIENTSTATISTICS.fields_by_name['uptime']._options = None
_TELEMETRY.fields_by_name['timestamp']._options = None
_TELEMETRY.fields_by_name['axis']._options = None
# @@protoc_insertion_point(module_scope)