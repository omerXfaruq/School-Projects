#include <algorithm>
#include <array>
#include <cstdint>
#include <cstring>
#include <memory>
#include <vector>
#include <omp.h>
#include <cmath>
#include <time.h>

constexpr uint32_t
    kAll = 0x1ff;
constexpr uint32_t
    B = 3;
constexpr uint32_t
    R = 9;
constexpr uint32_t
    RC = 9 * 9;
bool FOUND_ONE = false;

struct Threadmem
{
    std::array<uint32_t, R> rows;
    std::array<uint32_t, R> cols;
    std::array<uint32_t, R> boxes;
    char m_map[RC];
} __attribute__((__aligned__(8)));

constexpr uint32_t
    THREAD_COUNT = 2;
Threadmem Local_Mem[THREAD_COUNT];

struct SolverImpl
{
    std::vector<uint32_t> cells_todo;
    uint32_t num_todo = 0;
    char *m_solution;

    bool Initialize(const char *input, char *solution)
    {
        FOUND_ONE = false;
        Local_Mem[0].rows.fill(kAll);
        Local_Mem[0].cols.fill(kAll);
        Local_Mem[0].boxes.fill(kAll);
        memcpy(Local_Mem[0].m_map, input, RC);
        cells_todo.clear();
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
                    if (Local_Mem[0].rows[row] & value && Local_Mem[0].cols[col] & value &&
                        Local_Mem[0].boxes[box] & value)
                    {
                        Local_Mem[0].rows[row] ^= value;
                        Local_Mem[0].cols[col] ^= value;
                        Local_Mem[0].boxes[box] ^= value;
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

    void P_Solve(size_t todo_index, Threadmem &data)
    {

        for (int i = 1; i < THREAD_COUNT; i++)
        {
            memcpy(&Local_Mem[i], &Local_Mem[0], sizeof(Threadmem));
        }
        uint32_t row_col_box = cells_todo[todo_index];
        uint32_t row = row_col_box & kAll;
        uint32_t col = (row_col_box >> R) & kAll;
        uint32_t box = (row_col_box >> 2 * R) & kAll;
        uint32_t candidates = data.rows[row] & data.cols[col] & data.boxes[box];

        uint32_t candidate_list[R];
        uint32_t count = 0;
        for (uint32_t i = 0; i < R; i++)
        {
            if (candidates & (1u << i))
            {
                candidate_list[count] = i;
                count++;
            }
        }
#pragma omp parallel for schedule(dynamic, 1) num_threads(THREAD_COUNT)
        for (uint32_t i = 0; i < count; i++)
        {
            int tid = omp_get_thread_num();
            uint32_t candidate = 1u << candidate_list[i];
            Local_Mem[tid].m_map[row * R + col] = (char)('0' + __builtin_ffs(candidate));
            Local_Mem[tid].rows[row] ^= candidate;
            Local_Mem[tid].cols[col] ^= candidate;
            Local_Mem[tid].boxes[box] ^= candidate;
            Solve(todo_index + 1, Local_Mem[tid]);
            Local_Mem[tid].rows[row] ^= candidate;
            Local_Mem[tid].cols[col] ^= candidate;
            Local_Mem[tid].boxes[box] ^= candidate;
        }
    }

    void Solve(size_t todo_index, Threadmem &data)
    {
        /*
        Solves the problem sequentially.
        */

        if (FOUND_ONE)
            return;

        if (todo_index > num_todo)
        {
#pragma omp critical
            FOUND_ONE = true;
            memcpy(m_solution, data.m_map, RC);
            return;
        }

        uint32_t row_col_box = cells_todo[todo_index];
        uint32_t row = row_col_box & kAll;
        uint32_t col = (row_col_box >> R) & kAll;
        uint32_t box = (row_col_box >> 2 * R) & kAll;
        uint32_t candidates = data.rows[row] & data.cols[col] & data.boxes[box];

        while (candidates)
        {
            uint32_t candidate = candidates & -candidates;
            data.m_map[row * R + col] = (char)('0' + __builtin_ffs(candidate));
            data.rows[row] ^= candidate;
            data.cols[col] ^= candidate;
            data.boxes[box] ^= candidate;
            Solve(todo_index + 1, data);
            data.rows[row] ^= candidate;
            data.cols[col] ^= candidate;
            data.boxes[box] ^= candidate;
            candidates = candidates & (candidates - 1);
        }
    }
};

extern "C" size_t Solver(const char *input, char *solution)
{
    static SolverImpl solver;
    if (solver.Initialize(input, solution))
    {
        solver.P_Solve(0, Local_Mem[0]);
        return FOUND_ONE;
    }
    return 0;
}
