#include <iostream>
#include <fstream>
#include <list>
#include <queue>
#include <stack>
#include "Node.h"
#include "Simulation.h"
#include <unordered_set>
#include <random>
#include <memory>

using namespace std;

int main(int argc, char *argv[]) {
    ios_base::sync_with_stdio(false);
    clock_t start;
    start = clock();

    // below reads the input file
    // in your next projects, you will implement that part as well
    if (argc != 3) {
        cout << "Run the code with the following command: ./project1 [input_file] [output_file]" << endl;
        return 1;
    }
    cout << "input file: " << argv[1] << endl;
    cout << "output file: " << argv[2] << endl;

    string input = argv[1];
    string output = argv[2];
    ifstream infile(input);

    // process first line
    int numberOfRows, numberOfColumns;

    infile >> numberOfRows;
    infile >> numberOfColumns;


    Node **nodeArr[numberOfRows + 1];


    //Create banks and hold keys inside it
    for (int i = 1; i <= numberOfRows; i++) {
        nodeArr[i] = new Node *[numberOfColumns + 1];
        for (int j = 1; j <= numberOfColumns; j++) {
            int stair;
            infile >> stair;
            nodeArr[i][j] = new Node(stair, i, j);
        }
    }
    cout << (clock() - start) / (double) CLOCKS_PER_SEC << ": finished reading input" << endl;


    Simulation simulation(nodeArr, numberOfRows, numberOfColumns);




    ofstream out(output);


    int questionSize;
    infile >> questionSize;
    int arr[4];
    //for (int i = 0; i < questionSize; i++) {
    infile >> arr[0];
    infile >> arr[1];
    infile >> arr[2];
    infile >> arr[3];
    int distance = simulation.start(arr[0], arr[1], arr[2], arr[3]);

    cout << "distance between " << arr[0] << " " << arr[1] << " " << arr[2] << " " << arr[3] << endl;

    cout << distance << endl;

    out << distance << endl;
    // }
    infile.close();

    cout << (clock() - start) / (double) CLOCKS_PER_SEC << ": finished finding the distance" << endl;

    return 0;
}
