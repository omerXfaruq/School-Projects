import sys
import random

if __name__ == "__main__":
    # Initial setup and getting command line arguments
    file_name = "hard_test"
    num_graphs = 5
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]
    if len(sys.argv) >= 3:
        num_graphs = int(sys.argv[2])
    file_path = "../inputs_outputs/{}.in".format(file_name)

    # Some additional configuration
    verts_min = 5
    verts_max = 100

    # Storage for output
    all_data = []

    # Generate all the graphs
    for graph in range(num_graphs):
        # Generate number of edges and vertices
        num_verts = random.randrange(verts_min, verts_max + 1)
        edges_min = num_verts - 1
        edges_max = min(2000, num_verts * (num_verts - 1) // 2)
        num_edges = random.randrange(edges_min, edges_max + 1)
        all_data.append((num_verts, num_edges))

        # Create list of all possible edges
        all_edges = []
        for i in range(num_verts - 1):
            for j in range(i + 1, num_verts):
                all_edges.append((i, j))

        # Generate edges to ensure connected component
        vert_list = list(range(num_verts))
        random.shuffle(vert_list)
        for edge_idx in range(len(vert_list) - 1):
            if vert_list[edge_idx] < vert_list[edge_idx + 1]:
                temp_edge = (vert_list[edge_idx], vert_list[edge_idx + 1])
            else:
                temp_edge = (vert_list[edge_idx + 1], vert_list[edge_idx])
            all_data.append(temp_edge)
            all_edges.remove(temp_edge)

        # Generate remaining edges
        edge_list = random.sample(all_edges, num_edges - num_verts + 1)
        for edge in edge_list:
            all_data.append(edge)

    # Format output as strings
    all_lines = []
    all_lines.append("{}\n".format(num_graphs))
    for line in all_data:
        all_lines.append("{} {}\n".format(line[0], line[1]))
    all_lines[-1] = all_lines[-1].strip()

    # Write output
    out_file = open(file_path, "w")
    out_file.writelines(all_lines)
    out_file.close()
