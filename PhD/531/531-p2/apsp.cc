#include <cstdio>
#include <cstdlib>
#include <mpi.h>
#include <assert.h>
#include <cstdint>
#include <algorithm>
#include <cstring>

#define INF 200
#define ALIGNMENT 64

int main(int argc, char** argv) {
    int size, myRank, rc;
    rc = MPI_Init(&argc, &argv);
    assert(!rc);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &myRank);
    
    int n, m, k, base, myStart, myEnd;
    uint8_t *d, *local, *kth;
    MPI_Request req1;
    MPI_Request req2;
    MPI_Request requests[size];
    int starts[size];
    int ends[size];
    int lengths[size];
    bool subgraph_connections[size][size];
    uint8_t subgraph_parents[size][size];

    if(0 == myRank){
        int a,b,w;
        FILE *infile = fopen(argv[1], "r");
        fscanf(infile, "%d %d", &n, &m);

        base = (n+size-1)/size;

        d = (uint8_t *) aligned_alloc(ALIGNMENT, sizeof(uint8_t) * n * n);
        for (int i = 0; i < n * n; ++i) d[i] = INF;
        for (int i = 0; i < m; ++i) {
            fscanf(infile, "%d %d %d", &a, &b, &w);
            d[a * n + b] = d[b * n + a] = w;
            subgraph_connections[a/base][b/base] = subgraph_connections[b/base][a/base] = true;
        }
        fclose(infile);
    }
    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(subgraph_connections, sizeof(uint8_t)*size*size, MPI_UINT8_T, 0, MPI_COMM_WORLD);
    
    base = (n+size-1)/size;
    myStart = myRank*base;
    myEnd = std::min(myStart + base, n);
    
    for(int i = 0; i<size; i++){
        starts[i] = i*base * n;
        ends[i] = (std::min(starts[i] + base*n, n*n));
        lengths[i] = (ends[i] - starts[i]);
    }

    local = (uint8_t *) aligned_alloc(ALIGNMENT, sizeof(uint8_t) * base * n);
    kth = (uint8_t *) aligned_alloc(ALIGNMENT, sizeof(uint8_t) * n);

    MPI_Scatterv(d, lengths, starts, MPI_UINT8_T, local, lengths[myRank], MPI_UINT8_T, 0, MPI_COMM_WORLD);

    
    bool subgraphs_are_fully_connected = true;

    for(int i =0; i<size; i++)
        for(int j=i+1; j<size; j++)
            subgraphs_are_fully_connected &= subgraph_connections[i][j];


    if(!subgraphs_are_fully_connected){
        printf("Subgrapghs are not fully connected, using advanced communication algorithm!!\n");
        for(int i =0; i<size; i++)
            for(int j=0; j<size; j++)
                subgraph_parents[i][j] = -1;
        
        for(int i =0; i<size; i++)
            for(int j=0; j<size; j++)
                if(subgraph_connections[i][j]) subgraph_parents[i][j]=i;

        for (k=0; k<n; ++k){
            int cur_host = k/base;
            if(cur_host == myRank){
                std::memcpy(kth, local + (k - myStart)*n, n);
                for(int j=myRank+1; j!=myRank; j=(j+1)%size)
                    if(subgraph_parents[cur_host][j] == myRank)
                        MPI_Isend(kth, n, MPI_UINT8_T, j, 0, MPI_COMM_WORLD, &req2);
            }else{
                MPI_Irecv(kth, n, MPI_UINT8_T, subgraph_parents[cur_host][myRank], 0, MPI_COMM_WORLD, &req2);
                MPI_Wait(&req2,MPI_STATUS_IGNORE);
                
                for(int j=myRank+1; j!=myRank; j=(j+1)%size)
                    if(subgraph_parents[cur_host][j] == myRank)
                        MPI_Isend(kth, n, MPI_UINT8_T, j, 0, MPI_COMM_WORLD, &req2);
            }
            #pragma omp parallel for schedule(static,ALIGNMENT) collapse(2)
            for (int i = myStart; i < myEnd; ++i) {
                for (int j = 0; j < n; ++j) {
                    int w;
                    if ((w = local[(i-myStart)*n + k] + kth[j]) < local[(i-myStart)*n + j]) 
                        local[(i-myStart)*n + j] = w;
                }
            }
        }

    }else{
        if(0 == myRank){
            std::memcpy(kth, local, n);
        }

        k=0;
        MPI_Ibcast(kth, n/2, MPI_UINT8_T, (k)/base, MPI_COMM_WORLD, &req1);
        
        
        for (; k < n-1; ++k){
            if((k)/base == myRank){
                std::memcpy(kth+n/2, local + (k - myStart)*n + n/2, n-n/2);
            }
            MPI_Ibcast(kth + n/2, n-n/2, MPI_UINT8_T, k/base, MPI_COMM_WORLD, &req2);
            
            MPI_Wait(&req1, MPI_STATUS_IGNORE);
            #pragma omp parallel for schedule(static,ALIGNMENT) collapse(2)
            for (int i = myStart; i < myEnd; ++i) {
                for (int j = 0; j < n/2; ++j) {
                    int w;
                    if ((w = local[(i-myStart)*n + k] + kth[j]) < local[(i-myStart)*n + j]) 
                        local[(i-myStart)*n + j] = w;
                }
            }
            if((k+1)/base == myRank){
                std::memcpy(kth, local + (k+1 - myStart)*n, n/2);
            }
            MPI_Ibcast(kth, n/2, MPI_UINT8_T, (k+1)/base, MPI_COMM_WORLD, &req1);

            MPI_Wait(&req2, MPI_STATUS_IGNORE);
            #pragma omp parallel for schedule(static,ALIGNMENT) collapse(2)
            for (int i = myStart; i < myEnd; ++i) {
                for (int j = n/2; j < n; ++j) {
                    int w;
                    if ((w = local[(i-myStart)*n + k] + kth[j]) < local[(i-myStart)*n + j]) 
                        local[(i-myStart)*n + j] = w;
                }
            }
        }

        if((k)/base == myRank){
            std::memcpy(kth+n/2, local + (k - myStart)*n + n/2, n-n/2);
        }
        MPI_Ibcast(kth + n/2, n-n/2, MPI_UINT8_T, (k)/base, MPI_COMM_WORLD, &req2);
        
        MPI_Wait(&req1, MPI_STATUS_IGNORE);
        #pragma omp parallel for schedule(static,ALIGNMENT) collapse(2)
            for (int i = myStart; i < myEnd; ++i) {
                for (int j = 0; j < n/2; ++j) {
                    int w;
                    if ((w = local[(i-myStart)*n + k] + kth[j]) < local[(i-myStart)*n + j]) 
                        local[(i-myStart)*n + j] = w;
            }
        }
            
        MPI_Wait(&req2, MPI_STATUS_IGNORE);
        #pragma omp parallel for schedule(static,ALIGNMENT) collapse(2)
            for (int i = myStart; i < myEnd; ++i) {
                for (int j = n/2; j < n; ++j) {
                    int w;
                    if ((w = local[(i-myStart)*n + k] + kth[j]) < local[(i-myStart)*n + j]) 
                        local[(i-myStart)*n + j] = w;
            }
        }

    }
    
        
    if(0 == myRank){
        for(int rank = 1; rank<size; rank++){
            MPI_Irecv(d + (starts[rank]), (ends[rank]-starts[rank]), MPI_UINT8_T, rank, 2*n, MPI_COMM_WORLD, &requests[rank]);
        }   
    }
    //This way we won't do copy after Irecv as it will directly write it to d
    MPI_Barrier(MPI_COMM_WORLD);

    if(0 != myRank){
        MPI_Isend(local, (myEnd-myStart)*n, MPI_UINT8_T, 0, 2*n, MPI_COMM_WORLD, &req1);
        MPI_Wait(&req1, MPI_STATUS_IGNORE);
    }  
    
    if(0 == myRank){
        FILE *outfile = fopen(argv[2], "w");
        for (int i = myStart; i < myEnd; ++i) 
                for (int j = 0; j < n; ++j) 
                    fprintf(outfile, "%d%s",
                        (i == j ? 0 : local[(i-myStart)*n + j]),
                        (j == n - 1 ? " \n" : " ")
                    );

        for (int rank = 1; rank<size; rank++){
            MPI_Wait(&requests[rank], MPI_STATUS_IGNORE);
            for (int i = starts[rank]/n; i < ends[rank]/n; ++i) 
                for (int j = 0; j < n; ++j) 
                    fprintf(outfile, "%d%s",
                        (i == j ? 0 : d[i * n + j]),
                        (j == n - 1 ? " \n" : " ")
                    );


        }
        free(d);
    }
    free(local);
    free(kth);
    MPI_Finalize();
}