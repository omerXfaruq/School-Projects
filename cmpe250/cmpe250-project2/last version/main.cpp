#include <iostream>
#include <fstream>
#include <list>
#include "Person.h"
#include "Simulation.h"

using namespace std;

int main(int argc, char *argv[]) {

    // below reads the input file
    // in your next projects, you will implement that part as well
    if (argc != 3) {
        cout << "Run the code with the following command: ./project1 [input_file] [output_file]" << endl;
        return 1;
    }


    cout << "input file: " << argv[1] << endl;
    cout << "output file: " << argv[2] << endl;

    list<Person> arrivalList;
    string input = argv[1];
    string output = argv[2];
    // here, perform the input operation. in other words,


    ifstream infile(input);

    // process first line
    int passengerNumber;
    int luggageTableSize;
    int securityTableSize;
    infile >> passengerNumber;
    infile >> luggageTableSize;
    infile >> securityTableSize;

    //Read all passengers one by one and add them to the Person list
    for (int i = 0; i < passengerNumber; i++) {
        int arrivalTime, planeTime, luggageTime, securityTime;
        char luggage, vip;
        infile >> arrivalTime;
        infile >> planeTime;
        infile >> luggageTime;
        infile >> securityTime;
        infile >> vip;
        infile >> luggage;
        Person addingPerson(arrivalTime, planeTime, luggageTime, securityTime, vip == 'V', luggage == 'L');

        arrivalList.push_back(addingPerson);
    }
    infile.close();
    cout << "input file has been read" << endl;


    //Create and start the simulation, outputing is done there.

    Simulation simulation(arrivalList, output, passengerNumber, luggageTableSize, securityTableSize);
    simulation.start();

    return 0;
}
