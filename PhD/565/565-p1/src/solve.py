from utils import (
    read_input,
    write_output,
    plot_graph_from_adjacency_list,
    calculate_vertex_and_leaf_count,
)
from algorithms import ALGO_CLASS_LIST
import sys

if __name__ == "__main__":
    # Debug flags
    DEBUG_PLOT_BEST_SOLUTION = False
    DEBUG_PLOT_ALL_SOLUTIONS = False
    DEBUG_PRINT_INPUTS_AND_OUTPUT_GRAPHS = False
    DEBUG_PRINT_LEAF_COUNTS = False

    file_in = "../inputs_outputs/hard.in"
    file_out = "../inputs_outputs/hard.out"

    if len(sys.argv) >= 3:
        file_in = sys.argv[1]
        file_out = sys.argv[2]
    if len(sys.argv) >= 4:
        DEBUG_PLOT_BEST_SOLUTION = sys.argv[3].lower() == "true"
    if len(sys.argv) >= 5:
        DEBUG_PLOT_ALL_SOLUTIONS = sys.argv[4].lower() == "true"
    if len(sys.argv) >= 6:
        DEBUG_PRINT_INPUTS_AND_OUTPUT_GRAPHS = sys.argv[5].lower() == "true"
    if len(sys.argv) >= 7:
        DEBUG_PRINT_LEAF_COUNTS = sys.argv[6].lower() == "true"

    problem_list = read_input(file_in)

    # Run our algorithm on all problems
    solution_list = []

    for index, prob in enumerate(problem_list):
        best_solution_pack = (-1, {}, "", 0)
        for algo in ALGO_CLASS_LIST:
            solution_adjacency_list = algo.solve(prob)
            vertex_count, leaf_count = calculate_vertex_and_leaf_count(
                solution_adjacency_list
            )
            if leaf_count > best_solution_pack[0]:
                best_solution_pack = (
                    leaf_count,
                    solution_adjacency_list,
                    algo.__name__,
                    vertex_count,
                )

            if DEBUG_PLOT_ALL_SOLUTIONS:
                plot_graph_from_adjacency_list(
                    prob,
                    solution_adjacency_list,
                    title=f"{algo.__name__} Solution {index}, leaf_count: {leaf_count}",
                )

            if DEBUG_PRINT_LEAF_COUNTS:
                print(
                    f"Problem: {index:>03} - Method: {algo.__name__:>12} - Leaves: {leaf_count:>2}, Ratio: %{round(leaf_count/vertex_count*100)}"
                )

        solution_list.append(best_solution_pack)
        if DEBUG_PLOT_BEST_SOLUTION:
            plot_graph_from_adjacency_list(
                prob,
                best_solution_pack[1],
                title=f"Best Solution {index}: {best_solution_pack[2]}, leaf_count: {best_solution_pack[0]}",
            )

        if DEBUG_PRINT_INPUTS_AND_OUTPUT_GRAPHS:
            print(f"Problem {index}: {prob}")
            print(f"Best Solution {index}: {best_solution_pack[1]}")

    # Write our algorithm's output to a file
    write_output(solution_list, file_out)
