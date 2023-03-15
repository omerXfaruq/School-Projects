#include "benchmark.h"

namespace Options {
int benchmark_sec = 10;
size_t dataset_size = 10000;
bool randomize = true;
uint64_t random_seed = 0;
}; // namespace Options

extern "C" SolverFn Solver;

int main(int argc, char **argv) {
  Benchmark benchmark;
  for (size_t i = 1; i < argc; ++i) {
    benchmark.Run(argv[i], Solver);
  }
}
