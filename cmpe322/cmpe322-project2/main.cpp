#include <iostream>
#include <cstdlib>
#include <pthread.h>
#include <fstream>
#include <string>
#include <unistd.h>
#include <mutex>
#include <queue>

using namespace std;

int paymentsLogged = 0;
mutex paymentNoMutex;
mutex billMutexes[5];
mutex ATMMutexes[11];
bool ATMcancel[11] = {false, false, false, false, false, false, false, false, false, false};
queue<int> ATMQueues[11];
int billAmounts[5] = {0, 0, 0, 0, 0};
mutex logMutex;
string outputName;

//Returns index according to bill type
int billIndex(string bill) {
    if (!bill.compare("cableTV"))
        return 0;
    else if (!bill.compare("electricity"))
        return 1;
    else if (!bill.compare("gas"))
        return 2;
    else if (!bill.compare("telecommunication"))
        return 3;
    else if (!bill.compare("water"))
        return 4;
    else
        return -1;
}

//Returns bill name according to bill index
string billName(int index) {
    if (index == 0)
        return "cableTV";
    else if (index == 1)
        return "electricity";
    else if (index == 2)
        return "gas";
    else if (index == 3)
        return "telecommunication";
    else if (index == 4)
        return "water";
    else
        return "-1";
}


//Creates customer thread, extracts delimiters, sends payment to ATM thread
void *CreateCustomerThread(void *ptr) {
    string customer = *reinterpret_cast<std::string *>(ptr);

    int position1 = customer.find(",");
    int position2 = customer.substr(position1 + 1).find(",") + position1 + 1;
    int position3 = customer.substr(position2 + 1).find(",") + position2 + 1;
    int position4 = customer.substr(position3 + 1).find(",") + position3 + 1;

    string word1 = customer.substr(0, position1);
    string word2 = customer.substr(position1 + 1, position2 - position1 - 1);
    string word3 = customer.substr(position2 + 1, position3 - position2 - 1);
    string word4 = customer.substr(position3 + 1, position4 - position3 - 1);
    string word5 = customer.substr(position4 + 1);

    int sleepTime = stoi(word1);
    int atmNo = stoi(word2);
    string billType = word3;
    int amount = stoi(word4);
    int customerNo = stoi(word5);

    sleep(sleepTime/1000);

    ATMMutexes[atmNo].lock();
    ATMQueues[atmNo].push(billIndex(word3));
    ATMQueues[atmNo].push(amount);
    ATMQueues[atmNo].push(customerNo);
    ATMMutexes[atmNo].unlock();
}

//Checks its awaiting payments, and does the payment if there is a awaiting one
void *CreateATMThread(void *ptr) {
    int AtmNo = *((int *) ptr);

    int billType, amount, customerNo;
    bool flag = false;
    while (1) {
        ATMMutexes[AtmNo].lock();
        if (ATMcancel[AtmNo])
            break;
        if (!ATMQueues[AtmNo].empty()) {
            billType = ATMQueues[AtmNo].front();
            ATMQueues[AtmNo].pop();
            amount = ATMQueues[AtmNo].front();
            ATMQueues[AtmNo].pop();
            customerNo = ATMQueues[AtmNo].front();
            ATMQueues[AtmNo].pop();
            flag = true;
        }
        ATMMutexes[AtmNo].unlock();

        if (flag) {
            //Payment
            billMutexes[billType].lock();
            billAmounts[billType] += amount;
            billMutexes[billType].unlock();

            //For logging
            string logOutput = "Customer";
            logOutput += to_string(customerNo + 1);
            logOutput += ",";
            logOutput += to_string(amount);
            logOutput += "TL,";
            logOutput += billName(billType);
            logOutput += "\n";
            logMutex.lock();

            ofstream output(outputName, std::ios_base::app);
            //Writing Log
            output << logOutput;
            paymentNoMutex.lock();
            paymentsLogged++;
            paymentNoMutex.unlock();
            output.close();
            logMutex.unlock();

            flag = false;
        }
    }
}

int main(int argc, char **argv) {
    int rc;
    int i;

    pthread_t ATMthreads[11];
    int argumentsForATMs[11];
    string inputName(argv[1]);
    outputName = inputName + "_log.txt";
    ofstream outputClear(outputName);       //Clear the output
    outputClear.close();
    //Create ATM threads
    for (int i = 0; i < 11; i++) {
        argumentsForATMs[i] = i;
        if (pthread_create(&ATMthreads[i], NULL, CreateATMThread, &argumentsForATMs[i])) {
            cout << "Unable to create ATM thread" << endl;
            exit(-1);
        }
    }


    //Read input and create customer threads
    ifstream input(argv[1]);

    int customerNumber;
    input >> customerNumber;
    pthread_t customerThreads[customerNumber];
    string argumentsForCustomers[customerNumber];
    string customerInfo;
    for (int i = 0; i < customerNumber; i++) {
        input >> customerInfo;
        customerInfo += ",";
        customerInfo += to_string(i);
        argumentsForCustomers[i] = customerInfo;
        if (pthread_create(&customerThreads[i], NULL, CreateCustomerThread, &argumentsForCustomers[i])) {
            cout << "Unable to create customer thread" << endl;
            exit(-1);
        }
    }
    input.close();


    for (int i = 0; i < customerNumber; i++) {
        pthread_join(customerThreads[i], NULL);
    }
    cout << "All customer threads has finished" << endl;

    //Wait until all payments are completed.
    while (1) {
        sleep(0.1);
        paymentNoMutex.lock();
        if (paymentsLogged == customerNumber) {
            paymentNoMutex.unlock();
            break;
        }
        paymentNoMutex.unlock();
    }
    //Cancel ATM threads
    for (int i = 0; i < 11; i++) {
        ATMMutexes[i].lock();
        ATMcancel[i] = true;
        ATMMutexes[i].unlock();
    }


    //Do last part of logging
    ofstream output(outputName, std::ios_base::app);
    output << "All payments are completed.\n";
    output << "CableTV: ";
    output << billAmounts[0];
    output << "TL\n";

    output << "Electricity: ";
    output << billAmounts[1];
    output << "TL\n";

    output << "Gas: ";
    output << billAmounts[2];
    output << "TL\n";

    output << "Telecommunication: ";
    output << billAmounts[3];
    output << "TL\n";

    output << "Water: ";
    output << billAmounts[4];
    output << "TL\n";


    output.close();


    cout << "Program is finished" << endl;
    cout << "Log location: " << outputName << endl;
}