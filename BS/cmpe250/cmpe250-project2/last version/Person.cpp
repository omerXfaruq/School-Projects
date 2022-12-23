//
// Created by student on 02.11.2018.
//

#include "Person.h"


Person::Person(int _arrivalTime, int _planeTime, int _luggageTime, int _securityTime, bool _vip, bool _luggage)
        : arrivalTime(_arrivalTime), planeTime(_planeTime), luggageTime(_luggageTime), securityTime(_securityTime),
          vip(_vip), luggage(_luggage) {
    this->comparable = _planeTime;

}

bool Person::operator<(const Person &comparison) const {
    if (this->comparable > comparison.comparable)
        return true;
    else if (this->comparable == comparison.comparable)
        return this->arrivalTime > comparison.arrivalTime;
    else
        return false;
}
