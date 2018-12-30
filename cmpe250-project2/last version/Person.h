//
// Created by student on 02.11.2018.
//

#ifndef CMPE250_PROJECT2_PERSON_H
#define CMPE250_PROJECT2_PERSON_H


class Person {
public:
    bool vip;               // true if he is vip
    bool luggage;           // true if he has luggage
    int arrivalTime;
    int planeTime;
    int luggageTime;
    int securityTime;

    int comparable;     //Used for comparing Persons with respect to different field        //When it is in counters it holds the value when will person get free

    bool operator<(const Person &comparison) const;

    Person(int arrivalTime, int planeTime, int luggageTime, int securityTime, bool vip, bool luggage);


};


#endif //CMPE250_PROJECT2_PERSON_H
