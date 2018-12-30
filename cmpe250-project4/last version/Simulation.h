//
// Created by student on 24.11.2018.
//

#ifndef PROJECT3_SIMULATION_H
#define PROJECT3_SIMULATION_H

#include <iostream>
#include <stack>
#include "Node.h"
#include <unordered_set>
#include <fstream>
#include <vector>
#include <queue>
#include "Node.h"

using namespace std;

class Simulation {
public:
    int numberOfRows, numberOfColumns;
    Node ***nodeArr;

    //int ****distanceArr;
    int start(int r1, int c1, int r2, int c2);

    Simulation(Node ***_nodeArr, int row, int column );


};

#endif //PROJECT3_SIMULATION_H
