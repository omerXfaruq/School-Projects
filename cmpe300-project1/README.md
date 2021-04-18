# mpi4py-gameOfLife

_By FarukOzderim_  

OpenMpi Project implemented in python3, mpi4py. Details about the project are in the description.  
Program is run with the following command,  
mpiexec --oversubscribe -np [M] python3 test.py [input] [output] [T]  
    
Example:  
mpiexec --oversubscribe -np 17 python3 test.py rand.txt output3.txt 19  
[M] is number of processors, [input] is input, [output] is output, [T] is number of rounds.  
[M] needs to be equal to c^2+1 for some c, where c divides 360 and a multiple of 2.  

User gives an input as initial state of the 360x360 map. Though my code is implemented dynamically, user can change the map size with changing BIGEDGE global variable in my code.  

OpenMpi environment should be installed and mpi4py pip package should be installed with

*pip3 install mpi4py*
