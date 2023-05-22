#include <cstdio>
#include <cstdlib>
#include <stdint.h>

#define INF 200
__device__ inline int calc_loc_index(int tid)
{
    return 4 * tid;
}
__device__ inline int calc_kth_index(int tid)
{
    return 4 * tid + 1;
}

__device__ inline int calc_block_addr(uint x, int y, int r, int b)
{
    if (x <= y)
        return (x * b * r + y) * b;

    return (y * b * r + x) * b;
}

__device__ inline uint8_t calc_loc_val(int x, int y, uint8_t *data, int b)
{
    return data[4 * (x * b + y)];
}

__device__ inline uint8_t calc_kth_val(uint x, int y, uint8_t *data, int b)
{
    if (x < y)
        return data[4 * (x * b + y) + 1];

    return data[4 * (y * b + x) + 1];
}

__device__ inline uint8_t calc_neigh_val1(uint x, int y, uint8_t *data, int b)
{
    return data[4 * (x * b + y) + 1];
}

__device__ inline uint8_t calc_neigh_val2(uint x, int y, uint8_t *data, int b)
{
    return data[4 * (x * b + y) + 2];
}

uint8_t host_calc_val(int x, int y, uint8_t *data, int b)
{
    if (x == y)
        return 0;
    if (x < y)
        return data[x * b + y];

    return data[y * b + x];
}

__global__ void gloyd1(uint8_t *gdata, int N, int B, int R, int mrank)
{
    extern __shared__ uint8_t sdata[];
    int tid = threadIdx.x;
    int block_start_address = mrank * B * (R * B + 1);
    int loc_x = tid / B;
    int loc_y = tid % B;
    int gi = block_start_address + loc_x * R * B + loc_y;
    int gi_x = gi / R / B;
    int gi_y = gi % (R * B);

    if (gi_x < gi_y)
        sdata[calc_kth_index(tid)] = gdata[gi];

    for (int k = 0; k < B; k++) // TODO; reduce number of steps for edge blocks
    {
        __syncthreads();
        uint16_t w;
        if (gi_x < gi_y)
            w = calc_kth_val(loc_x, k, sdata, B) + calc_kth_val(k, loc_y, sdata, B);
        
        __syncthreads();
        
        if (gi_x < gi_y)
            if (w < sdata[calc_kth_index(tid)])
                sdata[calc_kth_index(tid)] = w;

            
    }
    if (gi_x < gi_y)
        gdata[gi] = sdata[calc_kth_index(tid)];
}

__global__ void gloyd2(uint8_t *gdata, int N, int B, int R, int cur_rank)
{
    extern __shared__ uint8_t sdata[];
    int tid = threadIdx.x;
    int pivot_block_start_address = cur_rank * B * (R * B + 1);
    int loc_x = tid / B;
    int loc_y = tid % B;
    int my_block_start_address, gi, p_gi, p_gi_x, p_gi_y;
    bool upside = (int)blockIdx.x < cur_rank;
    if (upside) // Up side of the pivot
        my_block_start_address = pivot_block_start_address - (cur_rank - blockIdx.x) * R * B * B;
    else // Right side of the pivot
        my_block_start_address = pivot_block_start_address + (blockIdx.x - cur_rank + 1) * B;

    gi = my_block_start_address + loc_x * R * B + loc_y;

    p_gi = pivot_block_start_address + loc_x * R * B + loc_y;
    p_gi_x = p_gi / R / B;
    p_gi_y = p_gi % (R * B);

    sdata[calc_loc_index(tid)] = gdata[gi];

    if (p_gi_x < p_gi_y)
        sdata[calc_kth_index(tid)] = gdata[p_gi];

    for (int k = 0; k < B; k++) // TODO; reduce number of steps for edge blocks
    {
        __syncthreads();
        uint16_t w;
        if (upside)
            w = calc_loc_val(loc_x, k, sdata, B) + calc_kth_val(k, loc_y, sdata, B);
        else
            w = calc_kth_val(loc_x, k, sdata, B) + calc_loc_val(k, loc_y, sdata, B);

        __syncthreads();

        if (w < sdata[calc_loc_index(tid)])
            sdata[calc_loc_index(tid)] = w;
    }

    gdata[gi] = sdata[calc_loc_index(tid)];
}

__global__ void gloyd3(uint8_t *gdata, int N, int B, int R, int cur_rank)
{
    extern __shared__ uint8_t sdata[];
    int tid = threadIdx.x;

    int block_row = blockIdx.x / R;
    int block_col = blockIdx.x % R;

    if (block_row > block_col || block_row == cur_rank || block_col == cur_rank)
        return;

    int kth_block_start_address_1 = calc_block_addr(block_row, cur_rank, R, B);
    int kth_block_start_address_2 = calc_block_addr(cur_rank, block_col, R, B);
    int my_block_start_address = calc_block_addr(block_row, block_col, R, B);

    int loc_x = tid / B;
    int loc_y = tid % B;

    int gi = my_block_start_address + loc_x * R * B + loc_y;
    int gi_x = gi / R / B;
    int gi_y = gi % (R * B);

    int p_gi1 = kth_block_start_address_1 + loc_x * R * B + loc_y;
    int p_gix1 = p_gi1 / R / B;
    int p_giy1 = p_gi1 % (R * B);

    int p_gi2 = kth_block_start_address_2 + loc_x * R * B + loc_y;
    int p_gix2 = p_gi2 / R / B;
    int p_giy2 = p_gi2 % (R * B);

    if (gi_x < gi_y)
        sdata[calc_loc_index(tid)] = gdata[gi];

    if (p_gix1 < p_giy1)
        sdata[calc_kth_index(tid)] = gdata[p_gi1];

    if (p_gix2 < p_giy2)
        sdata[calc_kth_index(tid) + 1] = gdata[p_gi2];

    for (int k = 0; k < B; k++) // TODO; reduce number of steps for edge blocks
    {
        __syncthreads();
        uint16_t w;
        uint8_t n1, n2;
        if (gi_x < gi_y)
        {
            if (block_row > cur_rank)
                n1 = calc_neigh_val1(k, loc_x, sdata, B); // Transpose to upper triangle
            else
                n1 = calc_neigh_val1(loc_x, k, sdata, B);

            if (cur_rank > block_col)
                n2 = calc_neigh_val2(loc_y, k, sdata, B); // Transpose to upper triangle
            else
                n2 = calc_neigh_val2(k, loc_y, sdata, B);

            w = n1 + n2;
        }

        __syncthreads();

        if (gi_x < gi_y)
            if (w < sdata[calc_loc_index(tid)])
                sdata[calc_loc_index(tid)] = w;


    }

    if (gi_x < gi_y)
        gdata[gi] = sdata[calc_loc_index(tid)];
}

int main(int argc, char **argv)
{
    int B = atoi(argv[3]);
    int n, m;
    uint8_t *d, *dd;
    // input
    FILE *infile = fopen(argv[1], "r");
    fscanf(infile, "%d %d", &n, &m);
    int R = n / B + (n % B != 0);
    int memsize = sizeof(uint8_t) * R * B * R * B;
    d = (uint8_t *)malloc(memsize);
    for (int i = 0; i < R * B * R * B; ++i)
        d[i] = INF;
    int a, b, w;
    for (int i = 0; i < m; ++i)
    {
        fscanf(infile, "%d %d %d", &a, &b, &w);
        d[a * R * B + b] = w;
    }
    fclose(infile);

    cudaMalloc(&dd, memsize);
    cudaMemcpy(dd, d, memsize, cudaMemcpyHostToDevice);

    printf("R: %d N: %d B: %d\n", R, n, B);

    for (int r = 0; r < R; r++)
    {
        gloyd1<<<1, B * B, B * B * 4>>>(dd, n, B, R, r);
        gloyd2<<<R - 1, B * B, B * B * 4>>>(dd, n, B, R, r);
        gloyd3<<<R * R, B * B, B * B * 4>>>(dd, n, B, R, r);
    }

    cudaDeviceSynchronize();
    cudaMemcpy(d, dd, memsize, cudaMemcpyDeviceToHost);

    // output
    FILE *outfile = fopen(argv[2], "w");
    for (int i = 0; i < n; ++i)
    {
        for (int j = 0; j < n; ++j)
        {
            fprintf(outfile, "%d%s",
                    (i == j ? 0 : host_calc_val(i, j, d, R * B)),
                    (j == n - 1 ? " \n" : " "));
        }
    }
    free(d);
    cudaFree(dd);
}
