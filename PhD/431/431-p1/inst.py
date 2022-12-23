import re

class Instruction:
    def __init__(self, s):
        self.s = s  # for future refs
        self.op = s.strip().split(' ')[0]
        self.rd, self.rs, self.rt, self.imm, self.label = None, None, None, None, None
        if self.op in ['add', 'sub']:
            self.ty = 'R'
            m = re.search('(?P<op>[a-z]+) \$(?P<rd>[0-9]+), \$(?P<rs>[0-9]+), \$(?P<rt>[0-9]+)', s)
            self.rd = int(m.group('rd'))
            self.rs = int(m.group('rs'))
            self.rt = int(m.group('rt'))
        elif self.op in ['lw', 'sw']:
            self.ty = 'I'
            m = re.search('(?P<op>[a-z]+) \$(?P<rt>[0-9]+), (?P<imm>(\-|)[0-9]+)\(\$(?P<rs>[0-9]+)\)', s)
            self.rs = int(m.group('rs'))
            self.rt = int(m.group('rt'))
            self.imm = int(m.group('imm'))
            if self.imm % 4 != 0:
                raise AssertionError(f'In inst {s}, you are using an offset that does not align with 4 bytes for lw/sw. I do not think you want this')
        elif self.op in ['beq', 'bne']:
            self.ty = 'I'
            m = re.search('(?P<op>[a-z]+) \$(?P<rs>[0-9]+), \$(?P<rt>[0-9]+), (?P<label>[a-zA-Z0-9]+)', s)
            self.rs = int(m.group('rs'))
            self.rt = int(m.group('rt'))
            self.label = m.group('label')
        elif self.op in ['addi']:
            self.ty = 'I'
            m = re.search('(?P<op>[a-z]+) \$(?P<rt>[0-9]+), \$(?P<rs>[0-9]+), (?P<imm>(\-|)[0-9]+)', s)
            self.rs = int(m.group('rs'))
            self.rt = int(m.group('rt'))
            self.imm = int(m.group('imm'))
        elif self.op in ['sll', 'srl']:
            self.ty = 'R'
            m = re.search('(?P<op>[a-z]+) \$(?P<rd>[0-9]+), \$(?P<rt>[0-9]+), (?P<imm>(\-|)[0-9]+)', s)
            self.rd = int(m.group('rd'))
            self.rt = int(m.group('rt'))
            self.imm = int(m.group('imm'))  # This is not imm, but shamt actually, but I will just reuse the field for simplicity
        elif self.op in ['nop']:
            self.ty = 'nop'
        else:
            raise AssertionError('Unsupported opcode!')
        #print(self.op, self.rd, self.rs, self.rt, self.imm, self.label)

    def get_srcs(self):
        if self.ty == 'R':
            return [self.rs, self.rt]
        elif self.ty == 'I':
            if self.op in ['lw', 'addi']:
                return [self.rs]
            else:
                return [self.rs, self.rt]
        else:
            return []

    def get_dst(self):
        if self.ty == 'R':
            return self.rd
        elif self.ty == 'I':
            if self.op in ['lw', 'addi']:
                return self.rt
        return None

    def constraint_check(self, constraint):
        constraint = constraint.split(',')
        return self.ty in constraint or self.op in constraint or self.op == 'nop'

    def __repr__(self):
        return self.s

    def run(self, regs, dm):
        b_dst = None
        reg_writes = []
        mem_writes = []
        if self.op == 'add':
            reg_writes.append((self.rd, regs[self.rs] + regs[self.rt]))
        elif self.op == 'addi':
            reg_writes.append((self.rt, regs[self.rs] + self.imm))
        elif self.op == 'sub':
            reg_writes.append((self.rd, regs[self.rs] - regs[self.rt]))
        elif self.op == 'lw':
            #print((regs[self.rs] + self.imm)//4)
            #print(len(dm))
            reg_writes.append((self.rt, dm[(regs[self.rs] + self.imm) // 4]))
        elif self.op == 'sll':
            reg_writes.append((self.rd, regs[self.rt] << self.imm))
        elif self.op == 'srl':
            reg_writes.append((self.rd, regs[self.rt] >> self.imm))
        elif self.op == 'sw':
            mem_writes.append(((regs[self.rs] + self.imm) // 4, regs[self.rt]))
        elif self.op == 'beq':
            if regs[self.rs] == regs[self.rt]:
                b_dst = self.label
        elif self.op == 'bne':
            if regs[self.rs] != regs[self.rt]:
                b_dst = self.label

        for rd, val in reg_writes:
            if rd == 0:
                raise AssertionError(f'You are writing to zero register ($0). Is this really what you want (it should not be)?')
        
        return reg_writes, mem_writes, b_dst
