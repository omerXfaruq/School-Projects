import sys
from typing import List, Tuple
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt


def read_input(input_filename: str) -> List[dict]:
    """
    Reads graphs from the file and creates adjacency lists.

    Args:
        input_filename: file name

    Returns:
        adjacency_lists

    """

    # Read the lines from the file
    in_file = open(input_filename, "r")
    lines = in_file.readlines()
    in_file.close()

    # Remove all newline characters
    lines = [item.strip() for item in lines]

    # Split input into individual problems
    num_probs = int(lines[0])
    split_problems = []
    current_line = 1
    for i in range(num_probs):
        # Create single problem, empty to start
        temp_problem = []
        # Get and store the problem metadata from the first line
        first_line = lines[current_line].split()
        temp_problem.append((int(first_line[0]), int(first_line[1])))
        num_lines = temp_problem[0][1]
        current_line += 1
        # Read the remainder of the problem and store it
        for j in range(num_lines):
            temp_line = lines[current_line].split()
            temp_problem.append((int(temp_line[0]), int(temp_line[1])))
            current_line += 1
        # Store the problem into the list of all problems
        split_problems.append(temp_problem)

    # Store each problem as a map, create list of problems
    problem_list = []
    for prob in split_problems:
        # Get metadata
        num_verts = prob[0][0]
        num_edges = prob[0][1]
        # Create dict with vertices as keys
        graph = {}
        for i in range(num_verts):
            graph[i] = []
        # Add edges
        for i in range(num_edges):
            edge = prob[i + 1]
            graph[edge[0]].append(edge[1])
            graph[edge[1]].append(edge[0])
        # For sanity, sort each adjacency list
        for i in range(num_verts):
            graph[i].sort()

        # Store graph to list
        problem_list.append(graph)

    # Return list of problems
    return problem_list


# Helper function for writing all solutions to output
def write_output(
    best_solutions: List[Tuple[int, dict, str, int]], output_filename: str
):
    """
    Writes output to file in output convention. Check the pdf for details.

    Args:
        best_solutions: List of (leaf_count, adjacency_list, algo_name, vertex_count)
        output_filename:
    """

    # Create storage for output
    all_data = []
    # Process all problems
    for solution in best_solutions:
        leaf_count, adjacency_list, algo_name, vertex_count = solution
        edge_count = vertex_count - 1

        # Remove duplicate edges
        for vert in adjacency_list:
            for item in adjacency_list[vert]:
                adjacency_list[item].remove(vert)

        # Put everything in the list for output
        all_data.append((leaf_count, edge_count))
        for vert in adjacency_list:
            for item in adjacency_list[vert]:
                all_data.append((vert, item))

    # Format output as strings
    all_lines = []
    for line in all_data:
        all_lines.append("{} {}\n".format(line[0], line[1]))
    all_lines[-1] = all_lines[-1].strip()

    # Write output
    out_file = open(output_filename, "w")
    out_file.writelines(all_lines)
    out_file.close()


def convert_adjacency_list_to_matrix(dic: dict) -> List[List[int]]:
    vertix_count = len(dic)
    matrix = [[0] * vertix_count for _ in range(vertix_count)]
    for key, values in dic.items():
        for value in values:
            matrix[key][value] = 1
    return matrix


def convert_adjacency_matrix_to_list(matrix: List[List[int]]) -> dict:
    dic = {}
    for vertex, neighbours in enumerate(matrix):
        print(neighbours, vertex)
        dic[vertex] = []
        for index, neighbour in enumerate(neighbours):
            if neighbour == 1:
                dic[vertex].append(index)
    return dic


def create_graph_from_matrix(matrix: List[List[int]]) -> nx.Graph:
    graph = nx.from_numpy_array(np.matrix(matrix))
    return graph


def get_adjacency_matrix_from_graph(graph: nx.Graph) -> List[List[int]]:
    return nx.adjacency_matrix(graph).todense()


def plot_graph(graph_1: nx.Graph, graph_2: nx.Graph, title: str = ""):
    fig, axs = plt.subplots(1, 2)
    nx.draw_networkx(graph_1, ax=axs[0])
    nx.draw_networkx(graph_2, ax=axs[1])
    plt.title(title)
    plt.show()


def plot_graph_from_adjacency_list(dic_1: dict, dic_2: dict, title: str):
    plot_graph(
        create_graph_from_matrix(convert_adjacency_list_to_matrix(dic_1)),
        create_graph_from_matrix(convert_adjacency_list_to_matrix(dic_2)),
        title=title,
    )


def calculate_vertex_and_leaf_count(adjacency_list: dict) -> (int, int):
    """
    Args:
        adjacency_list:

    Returns:
        vertex_count, leaf_count
    """
    leaf_count = 0
    edge_count = 0
    for vertex, vertex_edges in adjacency_list.items():
        vertices_edge_count = len(vertex_edges)
        if vertices_edge_count == 1:
            leaf_count += 1
        edge_count += vertices_edge_count
    edge_count //= 2
    vertex_count = edge_count + 1

    return vertex_count, leaf_count
