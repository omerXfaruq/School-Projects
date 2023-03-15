#include <algorithm>
#include <array>
#include <cstdint>
#include <cstring>
#include <memory>
#include <vector>
#include <omp.h>
#include <cmath>
#include <time.h>

constexpr uint32_t kAll = 0x1ff;
constexpr uint32_t B = 3;
constexpr uint32_t R = 9;
constexpr uint32_t RC = 9 * 9;
bool FOUND_ONE = false;

struct LocalMem
{
  char m_map[RC];
  std::array<uint32_t, R> rows;
  std::array<uint32_t, R> cols;
  std::array<uint32_t, R> boxes;
};


LocalMem THREAD_MEM;
#pragma omp threadprivate(THREAD_MEM)

struct SolverImpl
{
  std::vector<uint32_t> cells_todo;
  uint32_t num_todo = 0;
  char *m_solution;

  bool Initialize(const char *input, char *solution)
  {
    omp_set_nested(3);
    omp_set_dynamic(0);
    THREAD_MEM.rows.fill(kAll);
    THREAD_MEM.cols.fill(kAll);
    THREAD_MEM.boxes.fill(kAll);
    memcpy(THREAD_MEM.m_map, input, RC);
    cells_todo.clear();
    FOUND_ONE = false;
    m_solution = solution;

    for (int row = 0; row < R; ++row)
    {
      for (int col = 0; col < R; ++col)
      {
        int box = int(row / B) * B + int(col / B);
        if (input[row * R + col] == '.')
        {
          uint32_t repr = row | (col << R) | (box << 2 * R);
          cells_todo.emplace_back(repr);
        }
        else
        {
          uint32_t value = 1u << (uint32_t)(input[row * R + col] - '1');
          if (THREAD_MEM.rows[row] & value && THREAD_MEM.cols[col] & value && THREAD_MEM.boxes[box] & value)
          {
            THREAD_MEM.rows[row] ^= value;
            THREAD_MEM.cols[col] ^= value;
            THREAD_MEM.boxes[box] ^= value;
          }
          else
          {
            return false;
          }
        }
      }
    }
    num_todo = cells_todo.size() - 1;

    return true;
  }

  void P_Solve(size_t todo_index)
  {
    if(todo_index==5){
      Solve(todo_index);
      return;
    }
    uint32_t row_col_box = cells_todo[todo_index];
    uint32_t row = row_col_box & kAll;
    uint32_t col = (row_col_box >> R) & kAll;
    uint32_t box = (row_col_box >> 2 * R) & kAll;
    uint32_t candidates = THREAD_MEM.rows[row] & THREAD_MEM.cols[col] & THREAD_MEM.boxes[box];

    uint32_t candidate_list[R];
    uint32_t count = 0;
    for (uint32_t i = 0; i < R; i++)
    {
      if (candidates & (1u << i))
      {
        candidate_list[count] = 1u << i;
        count++;
      }
    }

#pragma omp parallel for copyin(THREAD_MEM) 
    for (uint32_t i = 0; i < count; i++)
      {
        uint32_t candidate = candidate_list[i];
        THREAD_MEM.m_map[row * R + col] = (char)('0' + __builtin_ffs(candidate));
        THREAD_MEM.rows[row] ^= candidate;
        THREAD_MEM.cols[col] ^= candidate;
        THREAD_MEM.boxes[box] ^= candidate;
        P_Solve(todo_index + 1);
        THREAD_MEM.rows[row] ^= candidate;
        THREAD_MEM.cols[col] ^= candidate;
        THREAD_MEM.boxes[box] ^= candidate;
    }
  }

  void Solve(size_t todo_index)
  {
    /*
    Solves the problem sequentially.
    */
    if (FOUND_ONE)
      return;

    if (todo_index > num_todo)
    {
      bool found_now = false;
#pragma omp critical
      {
      found_now = FOUND_ONE == false;
      FOUND_ONE = true;
    }
    if(found_now){
      memcpy(m_solution, THREAD_MEM.m_map, RC);      
    }
      return;
    }

    uint32_t row_col_box = cells_todo[todo_index];
    uint32_t row = row_col_box & kAll;
    uint32_t col = (row_col_box >> R) & kAll;
    uint32_t box = (row_col_box >> 2 * R) & kAll;
    uint32_t candidates = THREAD_MEM.rows[row] & THREAD_MEM.cols[col] & THREAD_MEM.boxes[box];

    while (candidates)
    {
      uint32_t candidate = candidates & -candidates;
      THREAD_MEM.m_map[row * R + col] = (char)('0' + __builtin_ffs(candidate));
      THREAD_MEM.rows[row] ^= candidate;
      THREAD_MEM.cols[col] ^= candidate;
      THREAD_MEM.boxes[box] ^= candidate;
      Solve(todo_index + 1);
      THREAD_MEM.rows[row] ^= candidate;
      THREAD_MEM.cols[col] ^= candidate;
      THREAD_MEM.boxes[box] ^= candidate;
      candidates = candidates & (candidates - 1);
    }
  }
};

extern "C" size_t Solver(const char *input, char *solution)
{
  static SolverImpl solver;
  if (solver.Initialize(input, solution))
  {
    solver.P_Solve(0);
    return FOUND_ONE;
  }
  return 0;
}
