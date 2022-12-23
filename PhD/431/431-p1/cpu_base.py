import random

class CPU:
    def __init__(self, num_regs, dm_size):
        self.regs = [0] * num_regs
        # dm_size in word
        #random.seed(7)
        #self.dm = [random.randint(0, 1024) for _ in range(dm_size)]
        self.dm = [i for i in range(dm_size)]

    def set_regs(self, li):
        for i, val in li:
            if i == 0:
                raise AssertionError(f'reg 0 is always zero!')
            self.regs[i] = val
