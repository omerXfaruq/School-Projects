/* MPI+OpenMP+CUDA Hello World Sample
$ source /etc/profile.d/modules.sh
$ module load mpi/openmpi-x86_64
$ /usr/local/cuda/bin/nvcc -std=c++11 -ccbin mpicxx -Xcompiler -fopenmp -Xcompiler -std=c++11 hello_w135.cc hello_cuda.cu -o hello_w135
$ mpirun -np 4 ./hello_mpi
*/

#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <omp.h>

void hello_cuda(int);

int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    hello_cuda(rank);
#pragma omp parallel for
    for (int i = 0; i < 2; ++i) {
        int tid = omp_get_thread_num();
        printf("Hello world thread %d from rank %d out of %d processors\n", tid, rank, size);
    }
    MPI_Finalize();
}
