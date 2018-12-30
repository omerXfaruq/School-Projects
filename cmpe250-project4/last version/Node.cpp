//
// Created by student on 22.11.2018.
//

#include <memory>
#include "Node.h"

Node::Node(int _number, int _row, int _column) {
    height = _number;
    row = _row;
    column = _column;


}


bool Node::operator<(const Node &rhs) const {
    return this->distance > rhs.distance;
}