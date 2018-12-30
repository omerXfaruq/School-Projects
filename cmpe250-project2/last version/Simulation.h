//
// Created by student on 08.11.2018.
//

#ifndef CMPE250_PROJECT2_SIMULATION_H
#define CMPE250_PROJECT2_SIMULATION_H

#include <queue>
#include <list>
#include "Person.h"
#include <fstream>
#include <iostream>

using namespace std;

class Simulation {
public:
    int out2, passengerNumber, luggageTableSize, securityTableSize;
    double out1;
    list<Person> arrivalList;
    string output;

    Simulation(list<Person> &arrivalList, string output, int passengerNumber, int luggageTableSize,
               int securityTableSize);

    void start();

    void workForCase(bool firstFlyFirstOut, bool vip, bool onlineTicketing);


};


#endif //CMPE250_PROJECT2_SIMULATION_H
