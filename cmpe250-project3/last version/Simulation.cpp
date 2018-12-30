//
// Created by student on 24.11.2018.
//

#include <fstream>
#include <iostream>
#include <vector>
#include <queue>
#include "Simulation.h"


Simulation::Simulation(int _arrSize, Bank **_bankArr, string _output) {
    //int i = 0;
    bankArr = _bankArr;

    arrSize = _arrSize;

    output = _output;


}

//Create scc s, in scc make all banks an alias of root
//Give all keys in banks to root
void Simulation::scc(int bankNumber) {
//    i++;
//    cout<<i<<endl;
    Bank *bank = bankArr[bankNumber];
    bank->index = bank->low = id;
    id++;
    stacked.push(bankNumber);
    bank->onStack = true;
    unordered_set<int>::iterator it = bank->keyArr.begin();
    unordered_set<int>::iterator end = bank->keyArr.end();


    while (it != end) {
        Bank *child = bankArr[*it];
        it++;
        if (child->index == -1) {
            scc(child->number);
            bank->low = min(bank->low, child->low);
        } else if (child->onStack) {
            bank->low = min(bank->low,
                            child->index);     //Can do low?????      asistant's psuedo code says child->index?
        }
    }

    if (bank->low == bank->index) {
        while (true) {
            int top = stacked.top();
            Bank *popped = bankArr[top];
            popped->index = bank->index;      //Sure????
            stacked.pop();
            popped->onStack = false;

            if (top == bankNumber) {
                sccRoots.insert(bankNumber);
                break;
            }


            unordered_set<int>::iterator it2 = popped->keyArr.begin();
            unordered_set<int>::iterator end2 = popped->keyArr.end();
            while (it2 != end2) {
                bank->keyArr.insert(*it2);          //We can delete this line if we do use low values and delete them from sccRoots<int>
                it2++;
            }

            bankArr[top] = bankArr[bankNumber];    //Name banks as an alias of root in the scc.

            //Maybe i can use just low values and no need for alias
        }

    }
    //i--;

}

void Simulation::dfs(int number) {

    Bank *bank = bankArr[number];
    if (number != bank->number || bank->hasKey)
        return;
    unordered_set<int>::iterator it = bank->keyArr.begin();
    unordered_set<int>::iterator end = bank->keyArr.end();


    while (it != end) {
        Bank *child = bankArr[*it];

        if (child->number != number) {       // İf it is an alias of *bank dont dfs
            dfs(child->number);       //Dfs to all neighbours
            child->hasKey = true;
        }
        it++;
    }
}


void Simulation::scc() {

    for (int i = 1; i <= arrSize; i++) {        //Scc all banks
        if (bankArr[i]->index == -1) {
            scc(i);

        }
    }
    for (int i = 1; i <= arrSize; i++) {        //Dfs from all
        //Only dfs from scc's roots
        dfs(i);
    }
    string s = "";
    queue<string> stringVector;
    int willCrack = 0;
    for (int i = 1; i <= arrSize; i++) {        //Find and print scc roots which has no key
        Bank *bank = bankArr[i];
        if (i == bank->number && !bank->hasKey) {
            stringVector.push(to_string(i));
            willCrack++;

            //   if (i ==70000) {
            //         cout << "hi" << endl;
            //    }
        }
    }
    ofstream out(output);
    out << willCrack << " ";
    while (!stringVector.empty()) {
        out << stringVector.front() << " ";
        stringVector.pop();
    }
    out.close();

}