//
// Created by student on 22.11.2018.
//

#ifndef PROJECT3_BANK_H
#define PROJECT3_BANK_H

#include <list>
#include <unordered_set>

using namespace std;

class Node {
public:
    int height;
    int distance=INT32_MAX;
    int row,column;

    bool operator<(const Node  &rhs)const;

    bool onStack=false;
    bool finished=false;

    //int **distance;

    Node(int _number, int row, int column);


};


#endif //PROJECT3_BANK_H
