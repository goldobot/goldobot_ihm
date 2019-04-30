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

opcodes = {
    'wait_movement_finished': 126,
    'propulsion.set_pose':127,
    'propulsion.point_to':128,
    'propulsion.move_to': 129,
    'pump.set_pwm': 140,
    'arm.go_to_position': 141,
    'set_servo': 142,
    'ret':30,
    'call': 31,
    'delay': 32    
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
    def __repr__(self):
        return '<Arg {}>'.format(self.__dict__)
        
class Op:
    def __init__(self, op, args):        
        self.op = op
        self.args = [Arg(a) for a in args.split(',')] if args != '' else []
        
    def encode(self, parser):
        if self.op == 'call':
            seq_index = list(parser.sequences.keys()).index(self.args[0].name)
            return struct.pack('BBBB', opcodes[self.op], seq_index,0,0)
        if self.op == 'arm.go_to_position':
            pos_index = list(config.dynamixels_positions.keys()).index(self.args[0].name)
            return struct.pack('BBBB', opcodes[self.op], pos_index,0, 0)
            
        if self.op == 'set_servo':
            pos_index = config.servos[self.args[0].name]
            return struct.pack('BBBB', opcodes[self.op], pos_index,parser.variable_index(self.args[1].name),0)
        if len(self.args) == 0:
            return struct.pack('BBBB', opcodes[self.op], 0,0,0)
        if len(self.args) == 1:
            return struct.pack('BBBB', opcodes[self.op], parser.variable_index(self.args[0].name),0,0)
        
    def __repr__(self):
        return '<Op {} {}>'.format(self.op, self.args)

class Sequence:
    def __init__(self, name):
        self.name = name
        self.start_index = 0
        self.variables = OrderedDict()
        self.labels = {}
        self.ops = []
        
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
            
            op, args = line.split(' ', 1)
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
                self.current_sequence.labels[args] = self.current_index
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
        return buff
            
        
        
        

                

                
parser = SequenceParser()
parser.parse_file('sequence.txt')
