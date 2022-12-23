from inst import Instruction
from cpu_base import CPU

class VLIW(CPU):
    def __init__(self, packets, issue_width=2, constraints=['R,beq,bne,addi', 'lw,sw'], num_regs=32, dm_size=10):
        super().__init__(num_regs, dm_size)
        self.issue_width = issue_width
        assert(issue_width == len(constraints))
        self.constraints = constraints

        self.im = []
        self.branch_labels = {}
        for i, p in enumerate(packets):
            if ':' in p:
                label, p = p.split(':')[0].strip(), p.split(':')[1].strip()
                self.branch_labels[label] = i
            self.im.append(Packet(p))

        # Check is something that a compiler has to make sure is the case.
        # I am providing this code to improve student's productivity.
        self.check()

    def run(self):
        # Simulate the execution of the packet stream,
        # and throw an error if anything is wrong.
        cycle = 0

        i = 0
        while i < len(self.im):
            self.regs, self.dm, b_dst = self.im[i].run(self.regs, self.dm)
            if b_dst is not None:
                i = self.branch_labels[b_dst]
            else:
                i += 1
            cycle += 1

        return cycle

    def check(self):
        # Check slot constraints
        for p in self.im:
            p.constraint_check(self.constraints)

        # Check if the instructions in the same packet are writing to the same dst
        for p in self.im:
            p.check_write_conflict()

        # Check if load-use is apart by 1 cycle.
        # Maybe it is better to just simulate what happens,
        # (as this may prohibit some ninja optimization)
        # but I will just check this and throw error for simplicity,
        # as it will make students to debug their code much easier
        # (and I don't think students will perform any ninja optimizations anyways).
        loads = {}
        for i, p in enumerate(self.im):
            for inst in p.insts:
                if inst.op == "lw":
                    loads[inst.rt] = i
                for src in inst.get_srcs():
                    if src in loads and loads[src] >= i - 1:
                        raise AssertionError('Load and use is not separated by more than one cycle!')


class Packet:
    def __init__(self, s):
        inst_strs = s.split('|')
        self.insts = [Instruction(inst_s) for inst_s in inst_strs]
        self.s = s  # for future refs

    def constraint_check(self, constraints):
        assert(len(self.insts) == len(constraints))
        for inst, const in zip(self.insts, constraints):
            if not inst.constraint_check(const):
                raise AssertionError(f'Packet slot constraint violated: {inst} violates {const} in {self.s}')

    def check_write_conflict(self):
        write_regs = set()
        for inst in self.insts:
            dst = inst.get_dst()
            if dst is not None:
                if dst in write_regs:
                    raise AssertionError(f'{self.s} writing to the same reg in multiple instructions')
                write_regs.add(dst)

    def run(self, regs, dm):
        b_dst = None
        reg_writes = []
        mem_writes = []
        for inst in self.insts:
            tmp_reg_writes, tmp_mem_writes, tmp_b_dst = inst.run(regs, dm)
            reg_writes += tmp_reg_writes
            mem_writes += tmp_mem_writes
            if tmp_b_dst is not None:
                assert(b_dst is None)
                b_dst = tmp_b_dst

        for i, val in reg_writes:
            regs[i] = val
        for i, val in mem_writes:
            try: 
                dm[i] = val
            except:
                print(f"failing: i:{i}, val: {val}")
            dm[i] = val

        return regs, dm, b_dst
