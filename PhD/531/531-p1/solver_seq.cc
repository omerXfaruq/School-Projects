#include <algorithm>
#include <array>
#include <cstdint>
#include <cstring>
#include <memory>
#include <vector>
constexpr uint32_t kAll = 0x1ff;

struct SolverImpl {
  std::array<uint32_t, 9> rows{}, cols{}, boxes{};
  std::vector<uint32_t> cells_todo;
  size_t num_todo = 0, num_solutions = 0;

  void Solve(size_t todo_index, char *solution) {
    uint32_t row_col_box = cells_todo[todo_index];
    auto row = row_col_box & kAll;
    auto col = (row_col_box >> 9) & kAll;
    auto box = (row_col_box >> 18) & kAll;
    auto candidates = rows[row] & cols[col] & boxes[box];
    while (candidates) {
      uint32_t candidate = candidates & -candidates;
      rows[row] ^= candidate;
      cols[col] ^= candidate;
      boxes[box] ^= candidate;
      solution[row * 9 + col] = (char)('0' + __builtin_ffs(candidate));
      if (todo_index < num_todo) {
        Solve(todo_index + 1, solution);
      } else {
        ++num_solutions;
      }
      if (num_solutions > 0) {
        return;
      }
      rows[row] ^= candidate;
      cols[col] ^= candidate;
      boxes[box] ^= candidate;
      candidates = candidates & (candidates - 1);
    }
  }

  bool Initialize(const char *input, char *solution) {
    rows.fill(kAll);
    cols.fill(kAll);
    boxes.fill(kAll);
    cells_todo.clear();
    num_solutions = 0;
    memcpy(solution, input, 81);

    for (int row = 0; row < 9; ++row) {
      for (int col = 0; col < 9; ++col) {
        int box = int(row / 3) * 3 + int(col / 3);
        if (input[row * 9 + col] == '.') {
          cells_todo.emplace_back(row | (col << 9) | (box << 18));
        } else {
          uint32_t value = 1u << (uint32_t)(input[row * 9 + col] - '1');
          if (rows[row] & value && cols[col] & value && boxes[box] & value) {
            rows[row] ^= value;
            cols[col] ^= value;
            boxes[box] ^= value;
          } else {
            return false;
          }
        }
      }
    }
    num_todo = cells_todo.size() - 1;
    return true;
  }
};

extern "C" size_t Solver(const char *input, char *solution) {
  static SolverImpl solver;
  if (solver.Initialize(input, solution)) {
    solver.Solve(0, solution);
    return solver.num_solutions;
  }
  return 0;
}
