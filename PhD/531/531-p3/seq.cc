#include <cstdio>
#include <cstdlib>
#define INF 200

int main(int argc, char** argv) {
    int n, m, *d;
    // input
    FILE *infile = fopen(argv[1], "r");
    fscanf(infile, "%d %d", &n, &m);
    d = (int *) malloc(sizeof(int *) * n * n);
    for (int i = 0; i < n * n; ++i) d[i] = INF;
    int a, b, w;
    for (int i = 0; i < m; ++i) {
        fscanf(infile, "%d %d %d", &a, &b, &w);
        d[a * n + b] = d[b * n + a] = w;
    }
    fclose(infile);
    // Floyd-Warshall
    for (int k = 0; k < n; ++k) {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j)
                if ((w = d[i * n + k] + d[k * n + j]) < d[i * n + j])
                    d[i * n + j] = w;
        }
    }
    // ouput
    FILE *outfile = fopen(argv[2], "w");
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            fprintf(outfile, "%d%s",
                (i == j ? 0 : d[i * n + j]),
                (j == n - 1 ? " \n" : " ")
            );
        }
    }
    free(d);
}