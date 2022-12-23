#include "LinkedList.h"

LinkedList::LinkedList() {
    this->length;
    // pointer to the first element of LinkedList
    this->head = 0;
    // pointer to the last element of LinkedList
    this->tail = 0;
}

LinkedList::LinkedList(const LinkedList &list) {
    if (head)
        this->head = new Node(*(list.head));
    if (tail)
        this->tail = new Node(*(list.tail));
    this->length = list.length;
}

LinkedList &LinkedList::operator=(const LinkedList &list) {
    this->length = list.length;
    if (list.head) {
        delete this->head;
        this->head = new Node(*(list.head));
    }
    if (list.tail) {
        delete this->tail;
        this->tail = new Node(*(list.tail));
    }
    return *this;
}

LinkedList &LinkedList::operator=(LinkedList &&list) {
    this->length = move(list.length);
    delete this->head;
    delete this->tail;
    this->head = move(list.head);
    this->tail = move(list.tail);

    list.length = 0;
    list.head = NULL;
    list.tail = NULL;
    return *this;
}

LinkedList::LinkedList(LinkedList &&list) {
    this->length = move(list.length);
    this->head = move(list.head);
    this->tail = move(list.tail);

    list.length = 0;
    list.head = NULL;
    list.tail = NULL;
}

// add a new element to the back of LinkedList
void LinkedList::pushTail(string _name, float _amount) {
    if (!head) {                            //List is empty

        head = new Node(_name, _amount);
        tail = head;
        length = 1;
    } else {                                //There are some elements in the list
        tail = head;                        //traverse in the list and add element to end.
        while (tail->next != NULL) {
            tail = tail->next;
        }
        tail->next = new Node(_name, _amount);
        length++;
        tail = tail->next;
    }
}

// update an existing element
void LinkedList::updateNode(string _name, float _amount) {          //Traverse in the list and update the amount
    Node *current = head;
    while (current->name.compare(_name) && current->next != NULL) {

        current = current->next;
    }
    current->amount = _amount;

}

LinkedList::~LinkedList() {
    if (head)
        delete head;

};

