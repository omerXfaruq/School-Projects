//
// Created by student on 24.11.2018.
//

#ifndef PROJECT3_SIMULATION_H
#define PROJECT3_SIMULATION_H

#include <stack>
#include "Bank.h"
#include <unordered_set>

using namespace std;

class Simulation {
public:
    stack<int> stacked;
    //int i;
    int id = 1;
//int sccCount = 0;
    int arrSize;
    Bank **bankArr;
    string output;
    unordered_set<int> sccRoots;


    void scc(int bankNumber);

    void dfs(int number);

    void scc();

    Simulation(int _arrSize, Bank *_bankArr[], string _output);

};

#endif //PROJECT3_SIMULATION_H
