#include <iostream>
#include <fstream>
#include <list>
#include <queue>
#include <stack>
#include "Bank.h"
#include "Simulation.h"
#include <unordered_set>

using namespace std;


//int sccCount = 0;
//Bank **bankArr = new Bank *[1];
//unordered_set<int> *keyArr = new unordered_set[1];


int main(int argc, char *argv[]) {
    ios_base::sync_with_stdio(false);

    // below reads the input file
    // in your next projects, you will implement that part as well
      if (argc != 3) {
        cout << "Run the code with the following command: ./project1 [input_file] [output_file]" << endl;
      return 1;
     }


    cout << "input file: " << argv[1] << endl;
    cout << "output file: " << argv[2] << endl;

    string input = argv[1];
    string output = argv[2];
   // string input = "/home/student/Desktop/code/input14.txt";
   // string output = "/home/student/Desktop/code/myoutput14.txt";
    // here, perform the input operation. in other words,


    ifstream infile(input);

    // process first line
    int bankNumber;


    infile >> bankNumber;

    Bank *bankArr[bankNumber + 1];


    //Create banks and hold keys inside it
    for (int i = 1; i <= bankNumber; i++) {
        int keyNumber;
        infile >> keyNumber;
        Bank *bank = new Bank(i);
        bankArr[i] = bank;

        for (int k = 1; k <= keyNumber; k++) {
            int key;
            infile >> key;
            bank->keyArr.insert(key);
        }
    }
    infile.close();
    cout << "input file has been read" << endl;


    Simulation simulation = Simulation(bankNumber, bankArr, output);
    simulation.scc();

    //Create and start the simulation, outputing is done there.


    return 0;
}
