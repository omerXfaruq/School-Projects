//
// Created by student on 22.11.2018.
//

#ifndef PROJECT3_BANK_H
#define PROJECT3_BANK_H
#include <list>
#include <unordered_set>

using namespace std;

class Bank {
public:
    int number,low,index;
    bool onStack,hasKey;
    unordered_set<int> keyArr;

    // list<Bank*> childrenList;

    Bank(int _number);
};


#endif //PROJECT3_BANK_H
