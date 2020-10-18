# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: goldo/camera/detections.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='goldo/camera/detections.proto',
  package='goldo.camera',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1dgoldo/camera/detections.proto\x12\x0cgoldo.camera\"\xbd\x01\n\nDetections\x12\x36\n\ndetections\x18\x01 \x03(\x0b\x32\".goldo.camera.Detections.Detection\x1aw\n\tDetection\x12\x0e\n\x06tag_id\x18\x01 \x01(\x05\x12:\n\x07\x63orners\x18\x02 \x03(\x0b\x32).goldo.camera.Detections.Detection.Corner\x1a\x1e\n\x06\x43orner\x12\t\n\x01x\x18\x01 \x01(\x05\x12\t\n\x01y\x18\x02 \x01(\x05\x62\x06proto3'
)




_DETECTIONS_DETECTION_CORNER = _descriptor.Descriptor(
  name='Corner',
  full_name='goldo.camera.Detections.Detection.Corner',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='goldo.camera.Detections.Detection.Corner.x', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='y', full_name='goldo.camera.Detections.Detection.Corner.y', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  serialized_start=207,
  serialized_end=237,
)

_DETECTIONS_DETECTION = _descriptor.Descriptor(
  name='Detection',
  full_name='goldo.camera.Detections.Detection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='tag_id', full_name='goldo.camera.Detections.Detection.tag_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='corners', full_name='goldo.camera.Detections.Detection.corners', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_DETECTIONS_DETECTION_CORNER, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=118,
  serialized_end=237,
)

_DETECTIONS = _descriptor.Descriptor(
  name='Detections',
  full_name='goldo.camera.Detections',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='detections', full_name='goldo.camera.Detections.detections', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_DETECTIONS_DETECTION, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=48,
  serialized_end=237,
)

_DETECTIONS_DETECTION_CORNER.containing_type = _DETECTIONS_DETECTION
_DETECTIONS_DETECTION.fields_by_name['corners'].message_type = _DETECTIONS_DETECTION_CORNER
_DETECTIONS_DETECTION.containing_type = _DETECTIONS
_DETECTIONS.fields_by_name['detections'].message_type = _DETECTIONS_DETECTION
DESCRIPTOR.message_types_by_name['Detections'] = _DETECTIONS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Detections = _reflection.GeneratedProtocolMessageType('Detections', (_message.Message,), {

  'Detection' : _reflection.GeneratedProtocolMessageType('Detection', (_message.Message,), {

    'Corner' : _reflection.GeneratedProtocolMessageType('Corner', (_message.Message,), {
      'DESCRIPTOR' : _DETECTIONS_DETECTION_CORNER,
      '__module__' : 'goldo.camera.detections_pb2'
      # @@protoc_insertion_point(class_scope:goldo.camera.Detections.Detection.Corner)
      })
    ,
    'DESCRIPTOR' : _DETECTIONS_DETECTION,
    '__module__' : 'goldo.camera.detections_pb2'
    # @@protoc_insertion_point(class_scope:goldo.camera.Detections.Detection)
    })
  ,
  'DESCRIPTOR' : _DETECTIONS,
  '__module__' : 'goldo.camera.detections_pb2'
  # @@protoc_insertion_point(class_scope:goldo.camera.Detections)
  })
_sym_db.RegisterMessage(Detections)
_sym_db.RegisterMessage(Detections.Detection)
_sym_db.RegisterMessage(Detections.Detection.Corner)


# @@protoc_insertion_point(module_scope)
