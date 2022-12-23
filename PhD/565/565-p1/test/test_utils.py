from src.utils import (
    convert_adjacency_list_to_matrix,
    convert_adjacency_matrix_to_list,
    read_input,
    create_graph_from_matrix,
    get_adjacency_matrix_from_graph,
)
import pytest

adjacency_list = read_input("inputs_outputs/hard.in")[0]
adjacency_matrix = [[0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0]]


def test_convert_adjacency_list_to_matrix():
    print(adjacency_list)
    matrix = convert_adjacency_list_to_matrix(adjacency_list)
    print(matrix)
    assert matrix == adjacency_matrix


def test_convert_adjacency_matrix_to_list():
    print(adjacency_matrix)
    lis = convert_adjacency_matrix_to_list(adjacency_matrix)
    print(lis)
    assert lis == adjacency_list


def test_graph():
    graph = create_graph_from_matrix(convert_adjacency_list_to_matrix(adjacency_list))
    assert (get_adjacency_matrix_from_graph(graph) == adjacency_matrix).all()
