from collections import OrderedDict
import re
import math

units = {'': 1, 'mm' : 1e-3, 'deg' : math.pi/180 }


def parse_literal(val):
    #try int with unit
    m = re.match('(-?[\d]+)([a-z]*)', val)
    if m:
        return int(m.group(1)) * units[m.group(2)]
    #try vec2
    m = re.match('\(([\w]+),([\w]+)\)', val)
    if m:
        return (parse_literal(m.group(1)), parse_literal(m.group(2)))
    m = re.match('\(([\w]+),([\w]+),([\w]+)\)', val)
    if m:
        return (parse_literal(m.group(1)), parse_literal(m.group(2)), parse_literal(m.group(2)))
    return int(val)
    
    
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
        self.args = [Arg(a) for a in args.split(',')]
        
    def encode(self, parser):
        pass

class Sequence:
    def __init__(self, name):
        self.name = name
        self.start_index = 0
        self.variables = OrderedDict()
        self.labels = {}
        self.instructions = []
        
class SequenceParser:
    def __init__(self):
        self.constants = {}
        self.variables = OrderedDict()
        self.sequences = OrderedDict()
        self.current_block = None
        self.current_sequence = None
        self.current_index = 0
        
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
                print(op.__dict__)
                self.current_index += 1

                

                
parser = SequenceParser()
parser.parse_file('sequence.txt')
