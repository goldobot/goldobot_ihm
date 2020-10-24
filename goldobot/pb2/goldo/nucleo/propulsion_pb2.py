# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: goldo/nucleo/propulsion.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from goldo.common import geometry_pb2 as goldo_dot_common_dot_geometry__pb2
from goldo import pb2_options_pb2 as goldo_dot_pb2__options__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='goldo/nucleo/propulsion.proto',
  package='goldo.nucleo.propulsion',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1dgoldo/nucleo/propulsion.proto\x12\x17goldo.nucleo.propulsion\x1a\x1bgoldo/common/geometry.proto\x1a\x17goldo/pb2_options.proto\"\xda\x01\n\tTelemetry\x12)\n\x04pose\x18\x01 \x01(\x0b\x32\x1b.goldo.common.geometry.Pose\x12\x14\n\x0cleft_encoder\x18\x02 \x01(\r\x12\x15\n\rright_encoder\x18\x03 \x01(\r\x12\x10\n\x08left_pwm\x18\x04 \x01(\x02\x12\x11\n\tright_pwm\x18\x05 \x01(\x02\x12\x41\n\x05state\x18\x06 \x01(\x0e\x32\x32.goldo.nucleo.propulsion.PropulsionControllerState\x12\r\n\x05\x65rror\x18\x07 \x01(\r\"\x83\x01\n\x17MotorsVelocitySetpoints\x12\x10\n\x08left_vel\x18\x01 \x01(\x02\x12\x11\n\tright_vel\x18\x02 \x01(\x02\x12 \n\x18left_current_feedforward\x18\x03 \x01(\x02\x12!\n\x19right_current_feedforward\x18\x04 \x01(\x02\"\xc6\x01\n\x0eOdometryConfig\x12\x1b\n\x13\x64ist_per_count_left\x18\x01 \x01(\x02\x12\x1c\n\x14\x64ist_per_count_right\x18\x02 \x01(\x02\x12\x1b\n\x13wheel_distance_left\x18\x03 \x01(\x02\x12\x1c\n\x14wheel_distance_right\x18\x04 \x01(\x02\x12\x1e\n\x16speed_filter_frequency\x18\x05 \x01(\x02\x12\x1e\n\x16\x61\x63\x63\x65l_filter_frequency\x18\x06 \x01(\x02\"\x8b\x01\n\tPIDConfig\x12\n\n\x02kp\x18\x01 \x01(\x02\x12\n\n\x02ki\x18\x02 \x01(\x02\x12\n\n\x02kd\x18\x03 \x01(\x02\x12\r\n\x05lim_i\x18\x04 \x01(\x02\x12\r\n\x05lim_d\x18\x05 \x01(\x02\x12\x1a\n\x12\x64_filter_frequency\x18\x06 \x01(\x02\x12\x0f\n\x07out_min\x18\x07 \x01(\x02\x12\x0f\n\x07out_max\x18\x08 \x01(\x02\"\xea\x01\n\x1bPropulsionLowLevelPIDConfig\x12\x31\n\x05speed\x18\x01 \x01(\x0b\x32\".goldo.nucleo.propulsion.PIDConfig\x12\x31\n\x05longi\x18\x02 \x01(\x0b\x32\".goldo.nucleo.propulsion.PIDConfig\x12\x34\n\x08yaw_rate\x18\x03 \x01(\x0b\x32\".goldo.nucleo.propulsion.PIDConfig\x12/\n\x03yaw\x18\x04 \x01(\x0b\x32\".goldo.nucleo.propulsion.PIDConfig\"Z\n\"PropulsionLowLevelControllerConfig\x12\x17\n\x0fwheels_distance\x18\x01 \x01(\x02\x12\x1b\n\x13motors_speed_factor\x18\x02 \x01(\x02\"\xce\x02\n\x1aPropulsionControllerConfig\x12U\n\x10low_level_config\x18\x01 \x01(\x0b\x32;.goldo.nucleo.propulsion.PropulsionLowLevelControllerConfig\x12S\n\x0bpid_configs\x18\x02 \x03(\x0b\x32\x34.goldo.nucleo.propulsion.PropulsionLowLevelPIDConfigB\x08\x88\xb5\x18\x04\x90\xb5\x18\x01\x12\x1a\n\x12lookahead_distance\x18\x03 \x01(\x02\x12\x16\n\x0elookahead_time\x18\x04 \x01(\x02\x12\x18\n\x10static_pwm_limit\x18\x05 \x01(\x02\x12\x18\n\x10\x63ruise_pwm_limit\x18\x06 \x01(\x02\x12\x1c\n\x14reposition_pwm_limit\x18\x07 \x01(\x02\"P\n\x11\x45xecuteTrajectory\x12\r\n\x05speed\x18\x01 \x01(\x02\x12,\n\x06points\x18\x02 \x03(\x0b\x32\x1c.goldo.common.geometry.Point\"6\n\x0f\x45xecuteRotation\x12\x11\n\tyaw_delta\x18\x01 \x01(\x02\x12\x10\n\x08yaw_rate\x18\x02 \x01(\x02\"5\n\x12\x45xecuteTranslation\x12\x10\n\x08\x64istance\x18\x01 \x01(\x02\x12\r\n\x05speed\x18\x02 \x01(\x02*\x9c\x01\n\x19PropulsionControllerState\x12\x0c\n\x08INACTIVE\x10\x00\x12\x0b\n\x07STOPPED\x10\x01\x12\x15\n\x11\x46OLLOW_TRAJECTORY\x10\x02\x12\n\n\x06ROTATE\x10\x03\x12\x0e\n\nREPOSITION\x10\x04\x12\x12\n\x0eMANUAL_CONTROL\x10\x05\x12\x12\n\x0e\x45MERGENCY_STOP\x10\x06\x12\t\n\x05\x45RROR\x10\x07\x62\x06proto3'
  ,
  dependencies=[goldo_dot_common_dot_geometry__pb2.DESCRIPTOR,goldo_dot_pb2__options__pb2.DESCRIPTOR,])

_PROPULSIONCONTROLLERSTATE = _descriptor.EnumDescriptor(
  name='PropulsionControllerState',
  full_name='goldo.nucleo.propulsion.PropulsionControllerState',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INACTIVE', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STOPPED', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FOLLOW_TRAJECTORY', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ROTATE', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='REPOSITION', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MANUAL_CONTROL', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EMERGENCY_STOP', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1670,
  serialized_end=1826,
)
_sym_db.RegisterEnumDescriptor(_PROPULSIONCONTROLLERSTATE)

PropulsionControllerState = enum_type_wrapper.EnumTypeWrapper(_PROPULSIONCONTROLLERSTATE)
INACTIVE = 0
STOPPED = 1
FOLLOW_TRAJECTORY = 2
ROTATE = 3
REPOSITION = 4
MANUAL_CONTROL = 5
EMERGENCY_STOP = 6
ERROR = 7



_TELEMETRY = _descriptor.Descriptor(
  name='Telemetry',
  full_name='goldo.nucleo.propulsion.Telemetry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pose', full_name='goldo.nucleo.propulsion.Telemetry.pose', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='left_encoder', full_name='goldo.nucleo.propulsion.Telemetry.left_encoder', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='right_encoder', full_name='goldo.nucleo.propulsion.Telemetry.right_encoder', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='left_pwm', full_name='goldo.nucleo.propulsion.Telemetry.left_pwm', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='right_pwm', full_name='goldo.nucleo.propulsion.Telemetry.right_pwm', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='state', full_name='goldo.nucleo.propulsion.Telemetry.state', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='error', full_name='goldo.nucleo.propulsion.Telemetry.error', index=6,
      number=7, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=113,
  serialized_end=331,
)


_MOTORSVELOCITYSETPOINTS = _descriptor.Descriptor(
  name='MotorsVelocitySetpoints',
  full_name='goldo.nucleo.propulsion.MotorsVelocitySetpoints',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='left_vel', full_name='goldo.nucleo.propulsion.MotorsVelocitySetpoints.left_vel', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='right_vel', full_name='goldo.nucleo.propulsion.MotorsVelocitySetpoints.right_vel', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='left_current_feedforward', full_name='goldo.nucleo.propulsion.MotorsVelocitySetpoints.left_current_feedforward', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='right_current_feedforward', full_name='goldo.nucleo.propulsion.MotorsVelocitySetpoints.right_current_feedforward', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=334,
  serialized_end=465,
)


_ODOMETRYCONFIG = _descriptor.Descriptor(
  name='OdometryConfig',
  full_name='goldo.nucleo.propulsion.OdometryConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='dist_per_count_left', full_name='goldo.nucleo.propulsion.OdometryConfig.dist_per_count_left', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dist_per_count_right', full_name='goldo.nucleo.propulsion.OdometryConfig.dist_per_count_right', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='wheel_distance_left', full_name='goldo.nucleo.propulsion.OdometryConfig.wheel_distance_left', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='wheel_distance_right', full_name='goldo.nucleo.propulsion.OdometryConfig.wheel_distance_right', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='speed_filter_frequency', full_name='goldo.nucleo.propulsion.OdometryConfig.speed_filter_frequency', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='accel_filter_frequency', full_name='goldo.nucleo.propulsion.OdometryConfig.accel_filter_frequency', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=468,
  serialized_end=666,
)


_PIDCONFIG = _descriptor.Descriptor(
  name='PIDConfig',
  full_name='goldo.nucleo.propulsion.PIDConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='kp', full_name='goldo.nucleo.propulsion.PIDConfig.kp', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ki', full_name='goldo.nucleo.propulsion.PIDConfig.ki', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='kd', full_name='goldo.nucleo.propulsion.PIDConfig.kd', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lim_i', full_name='goldo.nucleo.propulsion.PIDConfig.lim_i', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lim_d', full_name='goldo.nucleo.propulsion.PIDConfig.lim_d', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='d_filter_frequency', full_name='goldo.nucleo.propulsion.PIDConfig.d_filter_frequency', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='out_min', full_name='goldo.nucleo.propulsion.PIDConfig.out_min', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='out_max', full_name='goldo.nucleo.propulsion.PIDConfig.out_max', index=7,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=669,
  serialized_end=808,
)


_PROPULSIONLOWLEVELPIDCONFIG = _descriptor.Descriptor(
  name='PropulsionLowLevelPIDConfig',
  full_name='goldo.nucleo.propulsion.PropulsionLowLevelPIDConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='speed', full_name='goldo.nucleo.propulsion.PropulsionLowLevelPIDConfig.speed', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='longi', full_name='goldo.nucleo.propulsion.PropulsionLowLevelPIDConfig.longi', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='yaw_rate', full_name='goldo.nucleo.propulsion.PropulsionLowLevelPIDConfig.yaw_rate', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='yaw', full_name='goldo.nucleo.propulsion.PropulsionLowLevelPIDConfig.yaw', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=811,
  serialized_end=1045,
)


_PROPULSIONLOWLEVELCONTROLLERCONFIG = _descriptor.Descriptor(
  name='PropulsionLowLevelControllerConfig',
  full_name='goldo.nucleo.propulsion.PropulsionLowLevelControllerConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='wheels_distance', full_name='goldo.nucleo.propulsion.PropulsionLowLevelControllerConfig.wheels_distance', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='motors_speed_factor', full_name='goldo.nucleo.propulsion.PropulsionLowLevelControllerConfig.motors_speed_factor', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1047,
  serialized_end=1137,
)


_PROPULSIONCONTROLLERCONFIG = _descriptor.Descriptor(
  name='PropulsionControllerConfig',
  full_name='goldo.nucleo.propulsion.PropulsionControllerConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='low_level_config', full_name='goldo.nucleo.propulsion.PropulsionControllerConfig.low_level_config', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pid_configs', full_name='goldo.nucleo.propulsion.PropulsionControllerConfig.pid_configs', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\210\265\030\004\220\265\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lookahead_distance', full_name='goldo.nucleo.propulsion.PropulsionControllerConfig.lookahead_distance', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lookahead_time', full_name='goldo.nucleo.propulsion.PropulsionControllerConfig.lookahead_time', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='static_pwm_limit', full_name='goldo.nucleo.propulsion.PropulsionControllerConfig.static_pwm_limit', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cruise_pwm_limit', full_name='goldo.nucleo.propulsion.PropulsionControllerConfig.cruise_pwm_limit', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='reposition_pwm_limit', full_name='goldo.nucleo.propulsion.PropulsionControllerConfig.reposition_pwm_limit', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1140,
  serialized_end=1474,
)


_EXECUTETRAJECTORY = _descriptor.Descriptor(
  name='ExecuteTrajectory',
  full_name='goldo.nucleo.propulsion.ExecuteTrajectory',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='speed', full_name='goldo.nucleo.propulsion.ExecuteTrajectory.speed', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='points', full_name='goldo.nucleo.propulsion.ExecuteTrajectory.points', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1476,
  serialized_end=1556,
)


_EXECUTEROTATION = _descriptor.Descriptor(
  name='ExecuteRotation',
  full_name='goldo.nucleo.propulsion.ExecuteRotation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='yaw_delta', full_name='goldo.nucleo.propulsion.ExecuteRotation.yaw_delta', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='yaw_rate', full_name='goldo.nucleo.propulsion.ExecuteRotation.yaw_rate', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1558,
  serialized_end=1612,
)


_EXECUTETRANSLATION = _descriptor.Descriptor(
  name='ExecuteTranslation',
  full_name='goldo.nucleo.propulsion.ExecuteTranslation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='distance', full_name='goldo.nucleo.propulsion.ExecuteTranslation.distance', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='speed', full_name='goldo.nucleo.propulsion.ExecuteTranslation.speed', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1614,
  serialized_end=1667,
)

_TELEMETRY.fields_by_name['pose'].message_type = goldo_dot_common_dot_geometry__pb2._POSE
_TELEMETRY.fields_by_name['state'].enum_type = _PROPULSIONCONTROLLERSTATE
_PROPULSIONLOWLEVELPIDCONFIG.fields_by_name['speed'].message_type = _PIDCONFIG
_PROPULSIONLOWLEVELPIDCONFIG.fields_by_name['longi'].message_type = _PIDCONFIG
_PROPULSIONLOWLEVELPIDCONFIG.fields_by_name['yaw_rate'].message_type = _PIDCONFIG
_PROPULSIONLOWLEVELPIDCONFIG.fields_by_name['yaw'].message_type = _PIDCONFIG
_PROPULSIONCONTROLLERCONFIG.fields_by_name['low_level_config'].message_type = _PROPULSIONLOWLEVELCONTROLLERCONFIG
_PROPULSIONCONTROLLERCONFIG.fields_by_name['pid_configs'].message_type = _PROPULSIONLOWLEVELPIDCONFIG
_EXECUTETRAJECTORY.fields_by_name['points'].message_type = goldo_dot_common_dot_geometry__pb2._POINT
DESCRIPTOR.message_types_by_name['Telemetry'] = _TELEMETRY
DESCRIPTOR.message_types_by_name['MotorsVelocitySetpoints'] = _MOTORSVELOCITYSETPOINTS
DESCRIPTOR.message_types_by_name['OdometryConfig'] = _ODOMETRYCONFIG
DESCRIPTOR.message_types_by_name['PIDConfig'] = _PIDCONFIG
DESCRIPTOR.message_types_by_name['PropulsionLowLevelPIDConfig'] = _PROPULSIONLOWLEVELPIDCONFIG
DESCRIPTOR.message_types_by_name['PropulsionLowLevelControllerConfig'] = _PROPULSIONLOWLEVELCONTROLLERCONFIG
DESCRIPTOR.message_types_by_name['PropulsionControllerConfig'] = _PROPULSIONCONTROLLERCONFIG
DESCRIPTOR.message_types_by_name['ExecuteTrajectory'] = _EXECUTETRAJECTORY
DESCRIPTOR.message_types_by_name['ExecuteRotation'] = _EXECUTEROTATION
DESCRIPTOR.message_types_by_name['ExecuteTranslation'] = _EXECUTETRANSLATION
DESCRIPTOR.enum_types_by_name['PropulsionControllerState'] = _PROPULSIONCONTROLLERSTATE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Telemetry = _reflection.GeneratedProtocolMessageType('Telemetry', (_message.Message,), {
  'DESCRIPTOR' : _TELEMETRY,
  '__module__' : 'goldo.nucleo.propulsion_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.propulsion.Telemetry)
  })
_sym_db.RegisterMessage(Telemetry)

MotorsVelocitySetpoints = _reflection.GeneratedProtocolMessageType('MotorsVelocitySetpoints', (_message.Message,), {
  'DESCRIPTOR' : _MOTORSVELOCITYSETPOINTS,
  '__module__' : 'goldo.nucleo.propulsion_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.propulsion.MotorsVelocitySetpoints)
  })
_sym_db.RegisterMessage(MotorsVelocitySetpoints)

OdometryConfig = _reflection.GeneratedProtocolMessageType('OdometryConfig', (_message.Message,), {
  'DESCRIPTOR' : _ODOMETRYCONFIG,
  '__module__' : 'goldo.nucleo.propulsion_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.propulsion.OdometryConfig)
  })
_sym_db.RegisterMessage(OdometryConfig)

PIDConfig = _reflection.GeneratedProtocolMessageType('PIDConfig', (_message.Message,), {
  'DESCRIPTOR' : _PIDCONFIG,
  '__module__' : 'goldo.nucleo.propulsion_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.propulsion.PIDConfig)
  })
_sym_db.RegisterMessage(PIDConfig)

PropulsionLowLevelPIDConfig = _reflection.GeneratedProtocolMessageType('PropulsionLowLevelPIDConfig', (_message.Message,), {
  'DESCRIPTOR' : _PROPULSIONLOWLEVELPIDCONFIG,
  '__module__' : 'goldo.nucleo.propulsion_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.propulsion.PropulsionLowLevelPIDConfig)
  })
_sym_db.RegisterMessage(PropulsionLowLevelPIDConfig)

PropulsionLowLevelControllerConfig = _reflection.GeneratedProtocolMessageType('PropulsionLowLevelControllerConfig', (_message.Message,), {
  'DESCRIPTOR' : _PROPULSIONLOWLEVELCONTROLLERCONFIG,
  '__module__' : 'goldo.nucleo.propulsion_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.propulsion.PropulsionLowLevelControllerConfig)
  })
_sym_db.RegisterMessage(PropulsionLowLevelControllerConfig)

PropulsionControllerConfig = _reflection.GeneratedProtocolMessageType('PropulsionControllerConfig', (_message.Message,), {
  'DESCRIPTOR' : _PROPULSIONCONTROLLERCONFIG,
  '__module__' : 'goldo.nucleo.propulsion_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.propulsion.PropulsionControllerConfig)
  })
_sym_db.RegisterMessage(PropulsionControllerConfig)

ExecuteTrajectory = _reflection.GeneratedProtocolMessageType('ExecuteTrajectory', (_message.Message,), {
  'DESCRIPTOR' : _EXECUTETRAJECTORY,
  '__module__' : 'goldo.nucleo.propulsion_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.propulsion.ExecuteTrajectory)
  })
_sym_db.RegisterMessage(ExecuteTrajectory)

ExecuteRotation = _reflection.GeneratedProtocolMessageType('ExecuteRotation', (_message.Message,), {
  'DESCRIPTOR' : _EXECUTEROTATION,
  '__module__' : 'goldo.nucleo.propulsion_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.propulsion.ExecuteRotation)
  })
_sym_db.RegisterMessage(ExecuteRotation)

ExecuteTranslation = _reflection.GeneratedProtocolMessageType('ExecuteTranslation', (_message.Message,), {
  'DESCRIPTOR' : _EXECUTETRANSLATION,
  '__module__' : 'goldo.nucleo.propulsion_pb2'
  # @@protoc_insertion_point(class_scope:goldo.nucleo.propulsion.ExecuteTranslation)
  })
_sym_db.RegisterMessage(ExecuteTranslation)


_PROPULSIONCONTROLLERCONFIG.fields_by_name['pid_configs']._options = None
# @@protoc_insertion_point(module_scope)
