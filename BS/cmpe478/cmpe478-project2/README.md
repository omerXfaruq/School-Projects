# cmpe478-hw2-OpenMPI-partial-differential-equation

_By FarukOzderim_  

This is a OpenMPI project, implemented in python, mpi4py.  
Poission differential equation is solved on a cubic shape with Jacobian Iteration approximation.  
Parallelization is done by dividing the cube into subcubes.  
There is a timeTesting.sh script for testing runtime in different scenarios, its output is in test.csv


# Dependencies
-openmpi  
-mpi4py  
-numpy

# run
-mpiexec --oversubscribe -np [x^3] python3 try.py [N-1]  
Example:  
mpiexec --oversubscribe -np 8 python3 try.py 5  
Here x needs to divide N.

-time bash timeTesting.sh output.csv  

# Visualization Of Partitioning


![Visualization](https://github.com/FarukOzderim/School-Projects/blob/master/cmpe478-project2/visualization.png)
