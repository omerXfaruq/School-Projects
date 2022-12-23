//
// Created by student on 24.11.2018.
//

#include "Simulation.h"

class Node;

Simulation::Simulation(Node ***_nodeArr, int _row, int _column) {
    nodeArr = _nodeArr;
    numberOfRows = _row;
    numberOfColumns = _column;

}



int operator-(Node const &a, Node const &b) {
    return abs((a.height) - (b.height));
}


int Simulation::start(int r1, int c1, int r2, int c2) {

    Node *arrival = nodeArr[r2][c2];
    arrival->distance = 0;

    priority_queue<Node> priorityQueue;
    Node &node = *arrival;
    priorityQueue.push(node);
    while (!priorityQueue.empty()) {
        node = priorityQueue.top();
        priorityQueue.pop();
        int row = node.row;
        int column = node.column;
        if (nodeArr[row][column]->finished)
            continue;           //This is an old value, this node is finished in djskstra., pass.

        nodeArr[row][column]->finished = true;

        if (row == r1 && column == c1) return node.distance;        //Found the distance

        if (row < numberOfRows) {
            Node &childNode = *nodeArr[row + 1][column];
            if (!childNode.finished) {          
                int maxDist = max(node.distance, node - childNode);

                if (!childNode.onStack) {

                    childNode.distance = maxDist; // change infinity to distance
                    
                }


                if (!childNode.onStack) {        //first discovery of the node
                    childNode.onStack = true;
                    priorityQueue.push(childNode);
                } else if (childNode.distance > maxDist) {
                    childNode.distance = maxDist;
                    priorityQueue.push(childNode);
                }
            }
        }
        if (row > 1) {
            Node &childNode = *nodeArr[row - 1][column];
            if (!childNode.finished) {          
                int maxDist = max(node.distance, node - childNode);

                if (!childNode.onStack) {

                    childNode.distance = maxDist; // change infinity to distance
                }


                if (!childNode.onStack) {        //İt was not seen before not pushed to prQueue before, and
                                                //its childNodesitance<=maxDist
                    childNode.onStack = true;
                    priorityQueue.push(childNode);
                } else if (childNode.distance > maxDist) {
                    childNode.distance = maxDist;
                    priorityQueue.push(childNode);
                }
            }
        }
        if (column < numberOfColumns) {
            Node &childNode = *nodeArr[row][column + 1];
            if (!childNode.finished) {       
                int maxDist = max(node.distance, node - childNode);

                if (!childNode.onStack) {

                    childNode.distance = maxDist; // change infinity to distance
                }


                if (!childNode.onStack) {

                    childNode.onStack = true;
                    priorityQueue.push(childNode);
                } else if (childNode.distance > maxDist) {
                    childNode.distance = maxDist;
                    priorityQueue.push(childNode);
                }
            }
        }
        if (column > 1) {
            Node &childNode = *nodeArr[row][column - 1];
            if (!childNode.finished) {          
                int maxDist = max(node.distance, node - childNode);

                if (!childNode.onStack) {

                    childNode.distance = maxDist; // change infinity to distance
                    
                }


                if (!childNode.onStack) {        //İt was not seen before not pushed to prQueue before, and
                    
                    childNode.onStack = true;
                    priorityQueue.push(childNode);
                } else if (childNode.distance > maxDist) {
                    childNode.distance = maxDist;
                    priorityQueue.push(childNode);
                }
            }
        }


    }
    return nodeArr[r1][c1]->distance;
}