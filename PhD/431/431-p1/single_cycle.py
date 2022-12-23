from inst import Instruction
from cpu_base import CPU

class SingleCycle(CPU):
    def __init__(self, insts, num_regs=32, dm_size=10):
        super().__init__(num_regs, dm_size)
        self.im = []
        self.branch_labels = {}
        for i, p in enumerate(insts):
            if ':' in p:
                label, p = p.split(':')[0].strip(), p.split(':')[1].strip()
                self.branch_labels[label] = i
            self.im.append(Instruction(p))

    def run(self):
        # Simulate the execution of the packet stream,
        # and throw an error if anything is wrong.
        cycle = 0

        i = 0
        while i < len(self.im):
            reg_writes, mem_writes, b_dst = self.im[i].run(self.regs, self.dm)
            for j, val in reg_writes:
                self.regs[j] = val
            for j, val in mem_writes:
                self.dm[j] = val
            if b_dst is not None:
                i = self.branch_labels[b_dst]
            else:
                i += 1
            cycle += 1

        return cycle


