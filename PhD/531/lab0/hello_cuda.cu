#include <stdio.h>
#include <cuda.h>
#include <cuda_runtime.h>

#define check(err) __check(err, __LINE__)
__host__ void __check(cudaError err, int line) {
    if (err) {
        fprintf(stderr, "%d:%s\n", line, cudaGetErrorString(err));
        abort();
    }
}

__global__ void hello_kernel() {
    int dev;
    cudaGetDevice(&dev);
    printf("Hello from cuda device %d\n", dev);
}

void hello_cuda(int rank) {
    int count;
    check(cudaGetDeviceCount(&count));
    check(cudaSetDevice(rank % count));
    hello_kernel<<<1, 1>>>();
    cudaDeviceSynchronize();
}
