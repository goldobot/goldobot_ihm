from collections import OrderedDict
import re
import math
import struct
import config

units = {'': 1, 'mm' : 1e-3, 'deg' : math.pi/180 }

def parse_literal(val):
    #try int with unit
    m = re.match('(-?[\d]+)([a-z]*)', val)
    if m:
        return int(m.group(1)) * units[m.group(2)]
    #try vec2
    m = re.match('\((-?[\w]+),(-?[\w]+)\)', val)
    if m:
        return (parse_literal(m.group(1)), parse_literal(m.group(2)))
    #try vec3
    m = re.match('\((-?[\w]+),(-?[\w]+),(-?[\w]+)\)', val)
    if m:
        return (parse_literal(m.group(1)), parse_literal(m.group(2)), parse_literal(m.group(3)))
    print(val)
    return int(val)
    
sensor_shifts = {'microswitch':0}

opcodes = {
    'mov',
    'add',
    'cmp',
    'jne',
    'je',
    'jl',
    'jle',
    'jg',
    'jge',
    'call'
}
opcodes_jump = {
    'jmp' : 200,
    'jz': 201,
    'jnz': 202
   }
opcodes = {
    'nop': (0, None, None, None),
    'mov1': (1, 'var', 'var', None), #move one int32 from arg1 into arg0
    'mov2': (2, 'var', 'var', None), #move two int32 from arg1 into arg0
    'mov3': (3, 'var', 'var', None), #move three int32 from arg1 into arg0
    'propulsion.motors_enable': (64, None, None, None),
    'propulsion.enable': (65, None, None, None),
    'propulsion.motors_disable': (66, None, None, None),
    'propulsion.disable': (67, None, None, None),
    'wait_movement_finished': (126, None, None, None),
    'wait_arm_finished': (125, None, None, None),
    'propulsion.set_pose': (127, 'var', None, None),
    'propulsion.point_to': (128, 'var','var', None),
    'propulsion.move_to': (129, 'var', 'var', None),
    'propulsion.rotate': (130, 'var', 'var', None),
    'propulsion.translate': (131, 'var', 'var', None),
    'propulsion.reposition': (132, 'var', 'var', None),
    'propulsion.enter_manual': (133, None, None, None),
    'propulsion.exit_manual': (134, None, None, None),
    'propulsion.set_control_levels': (135, 'imm', 'imm', None),
    'propulsion.set_target_pose': (136, 'var', 'var', None),
    'propulsion.face_direction': (137, 'var', 'var', None),
    'pump.set_pwm': (140, 'var', None, None),
    'arm.go_to_position': (141, 'arm_position', 'imm', 'imm'),
    'set_servo': (142, 'servo_id', 'var', 'imm'),
    'arm.shutdown': (143, None, None, None,),
    'ret': (30, None, None, None,),
    'call': (31,'sequence', 0,0),
    'delay': (32, 'var', None, None),
    'yield': (33, None, None, None,),
    'check_sensor' : (150, 'imm', None, None),
    'send_event' : (34, 'imm', 'imm', None)
    }

        
#format: op,a1,a2;a3
#a1 = output address
#a2 = input_address
#a3 = 2nd input_address or index

#for 2 input operands
#has 2 forms: input or output indexed
# re.match('^-?[\d+]*$', '-1000')
# re.match('^-?[\d+]*\.[\d+]*$', '-1000.0')
class Variable:
    def __init__(self, args):
        args = args.split(' ')        
        nd = args[1].split('=')
        self.type = args[0]
        self.name = nd[0].strip()
        self.default = parse_literal(nd[1]) if len(nd) == 2 else None
        self.index = None
        
    def encode(self):
        if self.type == 'int':
            return struct.pack('<i', self.default)
        if self.type == 'float':
            return struct.pack('<f', self.default)
        if self.type == 'vec2':
            return struct.pack('<ff', self.default[0], self.default[1])
        if self.type == 'vec3':
            return struct.pack('<fff', self.default[0], self.default[1], self.default[2])
        
        
class Arg:
    def __init__(self, arg):
        if re.match('^[a-z][\w]+$', arg):
            self.type = 'var'# var_idx, cst
            self.name = arg
        else:
            self.type = 'cst'
            self.value = parse_literal(arg)
            
    def encode(self, typ, parser):
        if typ is None:
            return 0
        if typ == 'var':
            return parser.variable_index(self.name)
        if typ == 'imm':
            return int(self.value)
        if typ == 'arm_position':
            return parser.config.get_arm_position_index(self.name)
        if typ == 'sequence':
            return list(parser.sequences.keys()).index(self.name)
        if typ == 'servo_id':
            return parser.config.get_servo_index(self.name)     
        
    def __repr__(self):
        return '<Arg {}>'.format(self.__dict__)
        
class Op:
    def __init__(self, op, args):        
        self.op = op
        self.args = [Arg(a) for a in args.split(',')] if args != '' else []
        
    def encode(self, parser):
        if self.op in opcodes_jump:
            offset = parser.current_sequence.labels[self.args[0].name] + parser.current_sequence_offset
            return struct.pack('<BBBB', opcodes_jump[self.op], offset % 256, offset >> 8, 0)
            
        args = [0,0,0]
        opc = opcodes[self.op]
        for i in range(len(self.args)):
            args[i] = self.args[i].encode(opc[i+1], parser)
        return struct.pack('<BBBB', opc[0], args[0], args[1], args[2])
        
    def __repr__(self):
        return '<Op {} {}>'.format(self.op, self.args)

class Sequence:
    def __init__(self, name):
        self.name = name
        self.start_index = 0
        self.variables = OrderedDict()
        self.labels = {}
        self.ops = []

class CompiledSequences:
    pass
    
class SequenceParser:
    def __init__(self):
        self.constants = {}
        self.variables = OrderedDict()
        self.sequences = OrderedDict()
        self.current_block = None
        self.current_sequence = None
        self.current_index = 0
        
    def variable_index(self, name):
        return self.variables[name].index
        
    def parse_file(self, path):
        for line in open(path):
            #strip whitespace
            line = line.split('#')[0].strip()
            #comment line and empty lines
            if line == '':
                continue
            
            if ' ' in line:
                op, args = line.split(' ', 1)
            else:
                op = line
                args = ''
            if op == 'include':
                pass
            if op == 'begin' and args.split(' ')[0] == 'sequence':
                if self.current_block is None:
                    self.current_sequence = Sequence(args.split(' ')[1])
                    self.current_index = 0
                    self.sequences[self.current_sequence.name] = self.current_sequence
            elif op == 'end' and args.split(' ')[0] == 'sequence':
                self.current_sequence.ops.append(Op('ret',''))
                self.current_sequence = None
            elif op == 'var':
                var = Variable(args)
                if self.current_sequence is None:
                    self.variables[var.name] = var
                else:
                    self.current_sequence.variables[var.name] = var   
            elif op == 'label':
                self.current_sequence.labels[args] = len(self.current_sequence.ops)
            else:
                op = Op(op,args)
                self.current_sequence.ops.append(op)
                
    def compile(self):
        #allocate global variables
        vars_buffer = b''        
        for v in self.variables.values():
            v.index = len(vars_buffer)//4
            vars_buffer += v.encode()
        #allocate sequence variables
        
        #encode sequences
        seqs_table = []
        seqs_buffer = b''
        for s in self.sequences.values():
            seqs_table.append(len(seqs_buffer) // 4)
            self.current_sequence = s
            self.current_sequence_offset = len(seqs_buffer) // 4
            for op in s.ops:
                seqs_buffer+=op.encode(self)
        #encode buffer
        #header
        buff = struct.pack('HHbbbb', 0,0, len(vars_buffer)//4, len(self.sequences), 0, 0)
        #variables
        buff += vars_buffer
        for si in seqs_table:
            buff += struct.pack('<H', si)
        buff += seqs_buffer
        retval = CompiledSequences()
        retval.binary = buff
        retval.variables = self.variables
        retval.sequence_names = [s.name for s in self.sequences.values()]
        return retval

#parser = SequenceParser()
#parser.parse_file('sequence.txt')
#print(len(parser.compile()))
