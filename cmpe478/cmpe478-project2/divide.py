from mpi4py import MPI
import numpy as np
import sys

edgeOfCube = int(sys.argv[1])+1    # N+1

x=(float(sys.argv[1])/float(sys.argv[2]))
print(round(x, 2))