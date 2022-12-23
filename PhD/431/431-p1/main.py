from vliw import VLIW
from single_cycle import SingleCycle

import argparse
import fileinput

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cpu-type', type=str, default='singlecycle')  # singlecycle, vliw
    parser.add_argument('--num-regs', type=int, default=32)
    parser.add_argument('--dm-size', type=int, default=65)
    parser.add_argument('--mips-code', type=str, default='./code.txt')
    parser.add_argument('--issue-width', type=int, default=2)
    args = parser.parse_args()

    insts = []
    for line in fileinput.input(args.mips_code):
        line = line.split('#')[0].strip()
        if len(line) > 0:
            insts.append(line)
    print(insts)

    if args.cpu_type == 'singlecycle':
        cpu = SingleCycle(insts, num_regs=args.num_regs, dm_size=args.dm_size)
    elif args.cpu_type == 'vliw':
        constraints = ['R,beq,bne,addi'] * (args.issue_width // 2) + ['lw,sw'] * (args.issue_width - args.issue_width // 2)
        cpu = VLIW(insts, num_regs=args.num_regs, dm_size=args.dm_size, issue_width=args.issue_width, constraints=constraints)

    print('# cycles: ', cpu.run())
    print('Final register state: ', cpu.regs)
    print('Final memory state:', cpu.dm)
