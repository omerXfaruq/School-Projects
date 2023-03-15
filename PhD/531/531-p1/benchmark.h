#include <algorithm>
#include <array>
#include <chrono>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iostream>
#include <random>
#include <vector>

namespace Options {
extern int benchmark_sec;
extern size_t dataset_size;
extern bool randomize;
extern uint64_t random_seed;
}; // namespace Options

class Util {
private:
  std::random_device rd_{};
  std::mt19937_64 rng_{rd_()};
  std::uniform_int_distribution<uint32_t> random_uint_{};
  std::uniform_real_distribution<> random_double_{0.0, 1.0};

public:
  void RandomSeed(uint64_t seed) {
    if (seed > 0) {
      rng_.seed(seed);
    }
  }
  uint32_t RandomUInt() { return random_uint_(rng_); }
  double RandomDouble() { return random_double_(rng_); }

  std::vector<int> Permutation(size_t size) {
    std::vector<int> ret;
    ret.reserve(size);
    for (size_t i = 0; i < size; ++i) {
      ret.push_back(i);
    }
    std::shuffle(ret.begin(), ret.end(), rng_);
    return ret;
  }

  void BlockShuffle(std::array<int, 9> *vec) {
    std::array<int, 3> blocks{0, 1, 2};
    std::shuffle(blocks.begin(), blocks.end(), rng_);
    for (size_t i = 0; i < 3; ++i) {
      std::array<int, 3> block{0, 1, 2};
      std::shuffle(block.begin(), block.end(), rng_);
      for (size_t j = 0; j < 3; ++j) {
        (*vec)[i * 3 + j] = blocks[i] * 3 + block[j];
      }
    }
  }

  void PermuteSudoku(char *board) {
    std::array<int, 9> digit_perm{0, 1, 2, 3, 4, 5, 6, 7, 8};
    std::shuffle(digit_perm.begin(), digit_perm.end(), rng_);
    std::array<int, 9> row_perm{0, 1, 2, 3, 4, 5, 6, 7, 8};
    std::array<int, 9> col_perm{0, 1, 2, 3, 4, 5, 6, 7, 8};
    BlockShuffle(&col_perm);
    BlockShuffle(&row_perm);

    size_t row_size = 9;
    size_t board_size = row_size * 9;

    std::vector<char> out_board;
    out_board.resize(board_size);

    for (size_t row = 0; row < 9; ++row) {
      for (size_t col = 0; col < 9; ++col) {
        char digit = board[row * 9 + col];
        if (digit != '.') {
          digit = (char)('1' + digit_perm[digit - '1']);
        }
        out_board[row_perm[row] * 9 + col_perm[col]] = digit;
      }
    }
    strncpy(board, &out_board[0], board_size);
  }
};

typedef size_t SolverFn(const char *input, char *solution);

struct Benchmark {
  const size_t board_size_ = 81;
  const size_t board_buf_size_ = 128; // board_size_ rounded up for alignment
  std::vector<char> dataset_;

  Util util;

  static bool ValidateSolution(const char *board) {
    std::array<uint32_t, 9 * 3> covered{};
    for (size_t i = 0; i < 9; ++i) {
      for (size_t j = 0; j < 9; ++j) {
        auto bit = 1u << (uint32_t)(board[i * 9 + j] - '1');
        covered[i] ^= bit;
        covered[9 + j] ^= bit;
        covered[18 + 3 * (i / 3) + (j / 3)] ^= bit;
      }
    }
    return std::all_of(covered.begin(), covered.end(),
                       [](uint32_t x) { return x == 0x1ff; });
  }

  static void PrintSudoku(const char *board, std::ostream &stream = std::cout) {
    for (size_t row = 0; row < 9; ++row) {
      for (size_t col = 0; col < 9; ++col) {
        stream << board[row * 9 + col];
      }
      stream << std::endl;
    }
  }

  static void ExitError(const char *board, const char *context) {
    std::cerr << "Error during " << context << std::endl;
    PrintSudoku(board, std::cerr);
    exit(1);
  }

  void Load(const std::string &filename) {
    std::ifstream file;
    file.open(filename);
    if (file.fail()) {
      std::cerr << "Error opening " << filename << std::endl;
      exit(1);
    }
    dataset_.resize(Options::dataset_size * board_buf_size_);
    fill(dataset_.begin(), dataset_.end(), 0);

    std::string line;
    size_t num_loaded = 0, num_processed = 0;
    while (std::getline(file, line)) {
      if (line.length() > 0 && line[0] != '#') {
        if (line[line.size() - 1] == '\r') {
          line.erase(line.size() - 1);
        }
        if (line.length() >= board_size_) {
          ++num_processed;
          bool is_full = num_loaded == Options::dataset_size;
          bool is_replace = util.RandomDouble() <
                            (double)Options::dataset_size / num_processed;
          if (is_full && !is_replace) {
            continue;
          }
          size_t idx =
              is_full ? util.RandomUInt() % Options::dataset_size : num_loaded;
          char *dest = &dataset_[board_buf_size_ * idx];
          strncpy(dest, line.c_str(), board_size_);
          if (Options::randomize) {
            util.PermuteSudoku(dest);
          }
          if (!is_full) {
            ++num_loaded;
          }
        }
      } else if (line.find("ALLOWZERO") != std::string::npos) {
        std::cerr << "ALLOWZERO is not supported." << std::endl;
        exit(1);
      }
    }
    file.close();
    // fill up to dataset_size
    if (num_loaded == num_processed) {
      while (num_loaded + num_processed < Options::dataset_size) {
        memcpy(&dataset_[board_buf_size_ * num_loaded], &dataset_[0],
               board_buf_size_ * num_processed);
        if (Options::randomize) {
          for (size_t j = 0; j < num_processed; j++) {
            util.PermuteSudoku(&dataset_[board_buf_size_ * (num_loaded + j)]);
          }
        }
        num_loaded += num_processed;
      }
    }
    for (size_t i = num_loaded; i < Options::dataset_size; i++) {
      auto which = util.RandomUInt() % num_loaded;
      strncpy(&dataset_[board_buf_size_ * i],
              &dataset_[board_buf_size_ * which], board_size_);
      if (Options::randomize) {
        util.PermuteSudoku(&dataset_[board_buf_size_ * i]);
      }
    }
  }

  void Warmup(SolverFn &solver) {
    char output[81]{0};
    for (size_t i = 0; i < Options::dataset_size; i++) {
      const char *board = &dataset_[board_buf_size_ * i];
      output[0] = '.';
      size_t count = solver(board, output);
      if (!count) {
        ExitError(board, "warmup: no solution found by solver");
      }
      if (!ValidateSolution(output)) {
        ExitError(board, "validation");
      }
    }
  }

  void Run(const std::string &filename, SolverFn &solver) {
    using std::chrono::duration_cast;
    using std::chrono::microseconds;
    using std::chrono::steady_clock;
    util.RandomSeed(Options::random_seed);
    Load(filename);
    auto perm = util.Permutation(Options::dataset_size);
    std::cout << "Benchmark of " << filename << std::endl;

    microseconds start =
        duration_cast<microseconds>(steady_clock::now().time_since_epoch());
    Warmup(solver);
    microseconds end =
        duration_cast<microseconds>(steady_clock::now().time_since_epoch());
    std::cout << "Validation walltime (usec): " << (end - start).count()
              << std::endl;

    char board_output[81]{0};
    size_t total_solved = 0;

    start = duration_cast<microseconds>(steady_clock::now().time_since_epoch());
    end = start;
    char output[81]{0};
    bool has_sol = true;
    while ((end - start).count() < Options::benchmark_sec * 1000000) {
      for (int i = 0; i < Options::dataset_size; i++) {
        const char *board = &dataset_[board_buf_size_ * i];
        has_sol &= solver(board, output) > 0;
      }
      total_solved += Options::dataset_size;
      end = duration_cast<microseconds>(steady_clock::now().time_since_epoch());
    }
    if (!has_sol) {
      std::cerr << "[Run] no solution found by solver" << std::endl;
      exit(1);
    }
    auto total_usec = (end - start).count();
    double board_per_second = 1000000 * total_solved / total_usec;
    double usec_per_board = total_usec / (double)total_solved;
    std::cout << "Benchmark walltime (usec): " << total_usec << std::endl
              << board_per_second << " board/sec" << std::endl
              << usec_per_board << " usec/board" << std::endl;
  }
};
