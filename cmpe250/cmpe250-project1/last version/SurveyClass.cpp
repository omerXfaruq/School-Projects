#include "SurveyClass.h"

SurveyClass::SurveyClass() {
    members = NULL;
}


SurveyClass::SurveyClass(const SurveyClass &other) {
    if (other.members)
        this->members = new LinkedList(*(other.members));
}

SurveyClass &SurveyClass::operator=(const SurveyClass &list) {
    if (list.members) {
        delete this->members;
        this->members = new LinkedList(*(list.members));
    }
    return *this;
}

SurveyClass::SurveyClass(SurveyClass &&other) {

    this->members = move(other.members);
    other.members = NULL;

}

SurveyClass &SurveyClass::operator=(SurveyClass &&list) {
    delete this->members;
    this->members = move(list.members);

    list.members = NULL;
    return *this;
}

SurveyClass::~SurveyClass() {
    if (members)
        delete members;
}

// Adds a new Node to the linked list or updates the corresponding Node in the linked list
void SurveyClass::handleNewRecord(string _name, float _amount) {
    if (members == NULL)            //create a linkedlist if it is not initialized
        members = new LinkedList();

    bool check = false;
    if (members->head) {
        Node *node = members->head;
        while (node->next != NULL) {            //Check if person exists in the list.
            if (!node->name.compare(_name)) {
                check = true;
            }
            node = node->next;
        }
        if (!node->name.compare(_name)) {
            check = true;
        }
        if (!check)
            members->pushTail(_name, _amount);      //Person does not exist in the list
        else
            members->updateNode(_name, _amount);    //Person does exist in the list
    } else {
        members->pushTail(_name, _amount);          //List is empty
    }
}

// Calculates and returns the minimum amount of expense.
// The minimum amount can have up to two decimal points.
float SurveyClass::calculateMinimumExpense() {
    float min = 100000;
    if (members->head) {                //Move along the list
        Node *node = members->head;
        while (node->next != NULL) {
            if (node->amount < min) {
                min = node->amount;
            }
            node = node->next;
        }
        if (node->amount < min)
            min = node->amount;


    }
    min = (int) (min * 100) / 100.f;        //Keep 2 digits after decimal

    return min;

}

// Calculates and returns the maximum amount of expense.
// The maximum amount can have up to two decimal points.
float SurveyClass::calculateMaximumExpense() {
    float max = 0.00;
    if (members->head) {
        Node *node = members->head;     //Move along the list
        while (node->next != NULL) {
            if (node->amount > max) {
                max = node->amount;
            }
            node = node->next;
        }
        if (node->amount > max) {
            max = node->amount;
        }


    }
    max = (int) (max * 100) / 100.f;    //Keep 2 digits after decimal

    return max;

}

// Calculates and returns the average amount of expense.
// The average amount can have up to two decimal points.
float SurveyClass::calculateAverageExpense() {
    float av = 0.00;
    if (members->head) {
        Node *node = members->head;     //Move along the list
        while (node->next != NULL) {
            av = av + node->amount;
            node = node->next;

        }
        av = av + node->amount;
        av = av / members->length;
        av = (int) (av * 100) / 100.f;  //Keep 2 digits after decimal
    }

    return av;
};