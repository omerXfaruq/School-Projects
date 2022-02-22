//
// Created by student on 032.11.20132.
//

#include "Simulation.h"

Simulation::Simulation(list<Person> &arrivalList, string output, int passengerNumber, int luggageTableSize,
                       int securityTableSize) {
    this->passengerNumber = passengerNumber;
    this->securityTableSize = securityTableSize;
    this->luggageTableSize = luggageTableSize;
    this->arrivalList = arrivalList;
    this->output = output;
    out1 = 0;
    out2 = 0;
}

void Simulation::start() {
    ofstream out;
    out.open(output);

    workForCase(0, 0, 0);
    out << out1 << " " << out2 << endl;

    workForCase(1, 0, 0);
    out << out1 << " " << out2 << endl;

    workForCase(0, 1, 0);
    out << out1 << " " << out2 << endl;

    workForCase(1, 1, 0);
    out << out1 << " " << out2 << endl;

    workForCase(0, 0, 1);
    out << out1 << " " << out2 << endl;

    workForCase(1, 0, 1);
    out << out1 << " " << out2 << endl;


    workForCase(0, 1, 1);
    out << out1 << " " << out2 << endl;


    workForCase(1, 1, 1);
    out << out1 << " " << out2 << endl;


}

void Simulation::workForCase(bool firstFlyFirstOut, bool vip, bool onlineTicketing) {
    //return;
    int totalTimePassengersSpentAtAirport = 0;
    int flightsMiss = 0;
    int t = 0;
    int arrived = 0;
    int luggageCounterEmptyAt = INT32_MAX;
    int securityCounterEmptyAt = INT32_MAX;
    list<Person>::iterator arrivalListEnd = arrivalList.end();      //Used for looking if iterator finished or not
    bool iteratorCheck = true;   //Used for finishing iterator
    int nextPersonArriving = 0;

    if (firstFlyFirstOut) {
        priority_queue<Person> luggageQueue, securityQueue, luggageCounters, securityCounters;
        list<Person>::iterator it = arrivalList.begin();
        Person nextPerson = *it;
        nextPersonArriving = nextPerson.arrivalTime;
        while (arrived < passengerNumber) {

            //Finish people who are finished at security counters
            while (!securityCounters.empty() && securityCounters.top().comparable == t) {
                Person person = securityCounters.top();
                securityCounters.pop();

                totalTimePassengersSpentAtAirport += t - person.arrivalTime;
                arrived++;
                if (t > person.planeTime)
                    flightsMiss++;
            }
            //Add people from securityQueue to securityCounters
            while (securityCounters.size() < securityTableSize && !securityQueue.empty()) {
                Person person = securityQueue.top();
                securityQueue.pop();
                person.comparable = t + person.securityTime;
                securityCounters.push(person);
            }
            //Discharge people from luggageCounters if they are finished there
            while (!luggageCounters.empty() && luggageCounters.top().comparable == t) {
                Person person = luggageCounters.top();
                luggageCounters.pop();

                if (person.vip && vip) {
                    totalTimePassengersSpentAtAirport += t - person.arrivalTime;


                    arrived++;
                    if (t > person.planeTime)
                        flightsMiss++;
                } else {
                    if (securityCounters.size() < securityTableSize) {
                        person.comparable = t + person.securityTime;
                        securityCounters.push(person);

                    } else {
                        person.comparable = person.planeTime;
                        securityQueue.push(person);
                    }

                }
            }

            //Add people to luggageCounters from luggageQueue

            while (luggageCounters.size() < luggageTableSize && !luggageQueue.empty()) {

                Person person = luggageQueue.top();
                luggageQueue.pop();
                person.comparable = t + person.luggageTime;
                luggageCounters.push(person);
            }

            //While nextPerson is entering to airport at that time
            if (nextPerson.arrivalTime == t) {
                if (!onlineTicketing || nextPerson.luggage) { //İf onlineTicketing is offline or person has luggage

                    if (luggageCounters.size() < luggageTableSize) {
                        nextPerson.comparable = t + nextPerson.luggageTime;
                        luggageCounters.push(nextPerson);

                    } else {
                        luggageQueue.push(nextPerson);
                    }
                } else if (nextPerson.vip && vip) {  //İf Vip feature is online and person is vip finish his simulation

                    arrived++;


                    if (t > nextPerson.planeTime)
                        flightsMiss++;
                } else {
                    if (securityCounters.size() < securityTableSize) {
                        nextPerson.comparable = t + nextPerson.securityTime;
                        securityCounters.push(nextPerson);
                    } else {
                        securityQueue.push(nextPerson);
                    }

                }
                if (iteratorCheck) {

                    if (++it != arrivalListEnd) {     //Gotta check if nextPerson gets null at .end()
                        nextPerson = *it;


                        nextPersonArriving = nextPerson.arrivalTime;
                    } else {
                        iteratorCheck = false;
                        nextPersonArriving = INT32_MAX;    //Dont pick next arrival time as minimum, because there is no person coming anymore.
                    }
                }
            }




            //İf luggageCounters are empty there is no future event for that
            if (!luggageCounters.empty()) luggageCounterEmptyAt = luggageCounters.top().comparable;
            else luggageCounterEmptyAt = INT32_MAX;

            //İf securityCounters are empty there is no future event for that
            if (!securityCounters.empty()) securityCounterEmptyAt = securityCounters.top().comparable;
            else securityCounterEmptyAt = INT32_MAX;


            t = min((min(luggageCounterEmptyAt, securityCounterEmptyAt)), nextPersonArriving);


        }


        this->out1 = (double) totalTimePassengersSpentAtAirport / (double) arrived;
        this->out2 = flightsMiss;


    } else {
        priority_queue<Person> luggageCounters, securityCounters;
        list<Person> luggageQueue, securityQueue;
        list<Person>::iterator it = arrivalList.begin();
        Person nextPerson = *it;
        nextPersonArriving = nextPerson.arrivalTime;

        while (arrived < passengerNumber) {


            //Finish people who are finished at security counters

            while (!securityCounters.empty() && securityCounters.top().comparable == t) {
                Person person = securityCounters.top();
                securityCounters.pop();
                totalTimePassengersSpentAtAirport += t - person.arrivalTime;
                arrived++;

                if (t > person.planeTime)
                    flightsMiss++;
            }

            //Add people from securityQueue to securityCounters
            while (securityCounters.size() < securityTableSize && !securityQueue.empty()) {
                Person person = securityQueue.front();
                securityQueue.pop_front();
                person.comparable = t + person.securityTime;
                securityCounters.push(person);
            }

            //Discharge people from luggageCounters if they are finished there wrt their arrivalTimes and add to
            //securityCounters or securityQueue
            while (!luggageCounters.empty() && luggageCounters.top().comparable == t) {
                Person person = luggageCounters.top();
                luggageCounters.pop();
                if (person.vip && vip) {
                    totalTimePassengersSpentAtAirport += t - person.arrivalTime;
                    arrived++;
                    if (t > person.planeTime)
                        flightsMiss++;
                } else {
                    if (securityCounters.size() < securityTableSize) {
                        person.comparable = t + person.securityTime;
                        securityCounters.push(person);
                    } else {
                        person.comparable = person.planeTime;
                        securityQueue.push_back(person);
                    }

                }
            }

            //Add people to luggageCounters from luggageQueue
            while (luggageCounters.size() < luggageTableSize && !luggageQueue.empty()) {
                Person person = luggageQueue.front();
                luggageQueue.pop_front();
                person.comparable = t + person.luggageTime;
                luggageCounters.push(person);
            }

            //While nextPerson is entering to airport at that time
            if (nextPerson.arrivalTime == t) {
                if (!onlineTicketing || nextPerson.luggage) { //İf onlineTicketing is offline or person has luggage

                    if (luggageCounters.size() < luggageTableSize) {
                        nextPerson.comparable = t + nextPerson.luggageTime;
                        luggageCounters.push(nextPerson);
                    } else {
                        luggageQueue.push_back(nextPerson);
                    }
                } else if (nextPerson.vip && vip) {  //İf Vip feature is online and person is vip finish his simulation

                    arrived++;
                    if (t > nextPerson.planeTime)
                        flightsMiss++;
                } else {
                    if (securityCounters.size() < securityTableSize) {
                        nextPerson.comparable = t + nextPerson.securityTime;
                        securityCounters.push(nextPerson);
                    } else {
                        securityQueue.push_back(nextPerson);
                    }

                }
                if (iteratorCheck) {

                    if (++it != arrivalListEnd) {     //Gotta check if nextPerson gets null at .end()
                        nextPerson = *it;

                        nextPersonArriving = nextPerson.arrivalTime;

                    } else {
                        iteratorCheck = false;
                        nextPersonArriving = INT32_MAX;    //Dont pick next arrival time as minimum, because there is no person coming anymore.
                    }
                }
            }


            if (!luggageCounters.empty()) luggageCounterEmptyAt = luggageCounters.top().comparable;
            else luggageCounterEmptyAt = INT32_MAX;

            if (!securityCounters.empty()) securityCounterEmptyAt = securityCounters.top().comparable;
            else securityCounterEmptyAt = INT32_MAX;


            t = min((min(luggageCounterEmptyAt, securityCounterEmptyAt)), nextPersonArriving);


        }


        this->out1 = (double) totalTimePassengersSpentAtAirport / (double) arrived;
        this->out2 = flightsMiss;
    }

}
