import sys

if __name__ == "__main__":
    # Require command line input
    if len(sys.argv) < 2:
        sys.exit('ERROR: Must run this file as "{} filename"'.format(sys.argv[0]))
    file_path = "../inputs_outputs/{}.out".format(sys.argv[1])

    # Read the lines from the file
    in_file = open(file_path, "r")
    lines = in_file.readlines()
    in_file.close()

    # Remove all newline characters
    lines = [item.strip() for item in lines]

    # Extract number of leaves from each output:
    leaves = []
    verts = []
    line_num = 0
    while line_num < len(lines):
        current_line = lines[line_num].split()
        leaves.append(int(current_line[0]))
        line_num += int(current_line[1]) + 1
        verts.append(int(current_line[1]) + 1)

    # Display results
    p_width = len(str(len(leaves)))
    l_width = len(str(max(leaves)))
    v_width = len(str(max(verts)))
    for prob in range(len(leaves)):
        print(
            "Graph {prob_num:>{prob_width}}: {leaf_num:>{leaf_width}} leaves --- {vert_num:>{vert_width}} total vertices)".format(
                prob_num=prob + 1,
                prob_width=p_width,
                leaf_num=leaves[prob],
                leaf_width=l_width,
                vert_num=verts[prob],
                vert_width=v_width,
            )
        )
