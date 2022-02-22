from mpi4py import MPI
import numpy as np
import sys

# Author: Ömer Faruk Özdemir
# Date: 13.12.2019
# Compiling and Working
# can run with
# mpiexec --oversubscribe -np [M] python3 test.py [input] [output] [T]
# example:
# mpiexec --oversubscribe -np 17 python3 test.py rand.txt output3.txt 19
input = sys.argv[1]
output = sys.argv[2]
roundNo = int(sys.argv[3])  # Get Inputs, and assign initial global variables
comm = MPI.COMM_WORLD
totalWorkerNumber = MPI.COMM_WORLD.Get_size()
rank = comm.Get_rank()
BIGEDGE = 360
WorkerNoOnAEdge = int((totalWorkerNumber - 1) ** (1 / 2))


def readInput(input):
    print("Reading the input")
    map = np.full((BIGEDGE, BIGEDGE), 0)
    inputFile = open(input, 'r')
    lineNo = 0
    for line in inputFile:
        if (len(line) == 0):
            continue
        row = line.split(" ", BIGEDGE - 1)
        map[lineNo] = row
        lineNo += 1
    return map


#    for line in inputFile


if rank == 0:  # Main Worker
    mainMap = readInput(input)
    print("Worker Number Is: ", totalWorkerNumber)
    position = np.arange(int(BIGEDGE / int(WorkerNoOnAEdge)))
    position2 = np.arange(int(BIGEDGE / int(WorkerNoOnAEdge)))
    # print(position)

    # Distribute the data
    print("Distributing the data")
    for row in range(0, WorkerNoOnAEdge):
        for column in range(0, WorkerNoOnAEdge):
            #print(str(row) + "  -  " + str(column))
            # print(mainMap[np.ix_(position2, position + column * int(BIGEDGE / WorkerNoOnAEdge))])
            comm.send(mainMap[np.ix_(position2, position + column * int(BIGEDGE / WorkerNoOnAEdge))],
                      dest=row * WorkerNoOnAEdge + +column + 1, tag=1)
        position2 += int(BIGEDGE / WorkerNoOnAEdge)

    # Collect the data
    print("Collecting the data")
    position = np.arange(int(BIGEDGE / int(WorkerNoOnAEdge)))
    position2 = np.arange(int(BIGEDGE / int(WorkerNoOnAEdge)))
    for row in range(0, WorkerNoOnAEdge):
        for column in range(0, WorkerNoOnAEdge):
            #print(str(row) + "  -  " + str(column))
            mainMap[np.ix_(position2, position + column * int(BIGEDGE / WorkerNoOnAEdge))] = comm.recv(
                source=row * WorkerNoOnAEdge + column + 1, tag=2)
        position2 += int(BIGEDGE / WorkerNoOnAEdge)

    # Write the output
    print("Writing the output")
    outputFile = open(output, "w")
    for i in range(0, BIGEDGE):
        line = ""
        row = mainMap[i]
        # print ("Row " + str(i) + " :" + str(row))
        for j in range(0, row.shape[0]):
            # print(row[j])
            line += str(row[j])
            line += " "
        outputFile.write(line + "\n")
    outputFile.close()

else:  # All other Workers
    myGrid = comm.recv(source=0, tag=1)  # Receive miniGrid from central worker
    myEdge = myGrid.shape[0]  # Edge length of the miniGrid
    # print("I am rank:" + str(rank) + "\n" + str(myGrid))
    rowNo = int((rank - 1) / WorkerNoOnAEdge)  # 0 to s/c -1
    columnNo = (rank - 1) % WorkerNoOnAEdge + 1  # 1 to s/c

    while roundNo > 0:  # Do the communication and round processing
        roundNo += -1

        ###Communication Part
        downLeftNeighbour = None
        downRightNeighbour = None
        upLeftNeighbour = None
        upRightNeighbour = None

        upRightCorner = myGrid[0][myEdge - 1]
        upLeftCorner = myGrid[0][0]
        downLeftCorner = myGrid[myEdge - 1][0]
        downRightCorner = myGrid[myEdge - 1][myEdge - 1]

        rightNeighboursColumn = None
        leftNeighboursColumn = None
        upNeighboursRow = None
        downNeighboursRow = None

        rightColumn = myGrid[:, myEdge - 1]
        leftColumn = myGrid[:, 0]
        upRow = myGrid[0]
        downRow = myGrid[myEdge - 1]

        c = WorkerNoOnAEdge

        # Odd columns send to right neighbour
        if columnNo % 2 == 1:
            comm.send(rightColumn, dest=rank + 1, tag=21)
        else:
            leftNeighboursColumn = comm.recv(source=rank - 1, tag=21)

        # Odd columns send to left neighbour
        if columnNo % 2 == 1:
            if columnNo == 1:
                comm.send(leftColumn, dest=rank + c - 1, tag=22)  # Toroid exception
            else:
                comm.send(leftColumn, dest=rank - 1, tag=22)
        else:
            if columnNo == WorkerNoOnAEdge:
                rightNeighboursColumn = comm.recv(source=rank - c + 1, tag=22)  # Toroid exception
            else:
                rightNeighboursColumn = comm.recv(source=rank + 1, tag=22)

        # Even columns send to right neighbour
        if columnNo % 2 == 0:
            if columnNo == WorkerNoOnAEdge:
                comm.send(rightColumn, dest=rank - c + 1, tag=23)  # Toroid exception
            else:
                comm.send(rightColumn, dest=rank + 1, tag=23)
        else:
            if columnNo == 1:
                leftNeighboursColumn = comm.recv(source=rank - 1 + c, tag=23)  # Toroid exception
            else:
                leftNeighboursColumn = comm.recv(source=rank - 1, tag=23)

        # Even columns send to left neighbour
        if columnNo % 2 == 0:
            comm.send(leftColumn, dest=rank - 1, tag=24)
        else:
            rightNeighboursColumn = comm.recv(source=rank + 1, tag=24)

        #####

        # Odd rows send to  above neighbour
        if rowNo % 2 == 1:
            comm.send(upRow, dest=rank - c, tag=31)
        else:
            downNeighboursRow = comm.recv(source=rank + c, tag=31)

        # Odd rows send to below neighbour
        if rowNo % 2 == 1:
            if rowNo == WorkerNoOnAEdge - 1:
                comm.send(downRow, dest=rank + c - c ** 2, tag=32)  # Toroid exception
            else:
                comm.send(downRow, dest=rank + c, tag=32)
        else:
            if rowNo == 0:
                upNeighboursRow = comm.recv(source=rank - c + c ** 2, tag=32)  # Toroid exception
            else:
                upNeighboursRow = comm.recv(source=rank - c, tag=32)

        # Even rows send to above neighbour
        if rowNo % 2 == 0:
            if rowNo == 0:
                comm.send(upRow, dest=rank - c + c ** 2, tag=33)
            else:
                comm.send(upRow, dest=rank - c, tag=33)
        else:
            if rowNo == WorkerNoOnAEdge - 1:
                downNeighboursRow = comm.recv(source=rank + c - c ** 2, tag=33)
            else:
                downNeighboursRow = comm.recv(source=rank + c, tag=33)

        # Even rows send to below neighbour
        if rowNo % 2 == 0:
            comm.send(downRow, dest=rank + c, tag=34)
        else:
            upNeighboursRow = comm.recv(source=rank - c, tag=34)

        ###CORNERS###

        # Odd rows send to cross neighbours
        if rowNo % 2 == 1:
            if columnNo == WorkerNoOnAEdge:
                comm.send(upRightCorner, dest=rank - c + 1 - c, tag=41)  # Toroid exception
            else:
                comm.send(upRightCorner, dest=rank - c + 1, tag=41)

            if columnNo == 1:
                comm.send(upLeftCorner, dest=rank - c - 1 + c, tag=42)  # Toroid exception
            else:
                comm.send(upLeftCorner, dest=rank - c - 1, tag=42)

            if columnNo == 1:
                if rowNo == WorkerNoOnAEdge - 1:  # Toroid Exceptions
                    comm.send(downLeftCorner, dest=rank + c - 1 + c - c ** 2, tag=43)
                else:
                    comm.send(downLeftCorner, dest=rank + c - 1 + c, tag=43)
            else:
                if rowNo == WorkerNoOnAEdge - 1:
                    comm.send(downLeftCorner, dest=rank + c - 1 - c ** 2, tag=43)
                else:
                    comm.send(downLeftCorner, dest=rank + c - 1, tag=43)

            if columnNo == WorkerNoOnAEdge:
                if rowNo == WorkerNoOnAEdge - 1:  # Toroid Exceptions
                    comm.send(downRightCorner, dest=rank + c + 1 - c - c ** 2, tag=44)
                else:
                    comm.send(downRightCorner, dest=rank + c + 1 - c, tag=44)
            else:
                if rowNo == WorkerNoOnAEdge - 1:
                    comm.send(downRightCorner, dest=rank + c + 1 - c ** 2, tag=44)
                else:
                    comm.send(downRightCorner, dest=rank + c + 1, tag=44)


        else:

            if columnNo == 1:
                downLeftNeighbour = comm.recv(source=rank + c - 1 + c, tag=41)
            else:
                downLeftNeighbour = comm.recv(source=rank + c - 1, tag=41)

            if columnNo == WorkerNoOnAEdge:
                downRightNeighbour = comm.recv(source=rank + c + 1 - c, tag=42)
            else:
                downRightNeighbour = comm.recv(source=rank + c + 1, tag=42)

            if columnNo == WorkerNoOnAEdge:
                if rowNo == 0:  # Toroid Exceptions
                    upRightNeighbour = comm.recv(source=rank - c + 1 - c + c ** 2, tag=43)
                else:
                    upRightNeighbour = comm.recv(source=rank - c + 1 - c, tag=43)
            else:
                if rowNo == 0:
                    upRightNeighbour = comm.recv(source=rank - c + 1 + c ** 2, tag=43)
                else:
                    upRightNeighbour = comm.recv(source=rank - c + 1, tag=43)

            if columnNo == 1:
                if rowNo == 0:  # Toroid Exceptions
                    upLeftNeighbour = comm.recv(source=rank - c - 1 + c + c ** 2, tag=44)
                else:
                    upLeftNeighbour = comm.recv(source=rank - c - 1 + c, tag=44)
            else:
                if rowNo == 0:
                    upLeftNeighbour = comm.recv(source=rank - c - 1 + c ** 2, tag=44)
                else:
                    upLeftNeighbour = comm.recv(source=rank - c - 1, tag=44)

        # Even rows send to cross neighbours
        if rowNo % 2 == 0:

            if columnNo == WorkerNoOnAEdge:
                comm.send(downRightCorner, dest=rank + c + 1 - c, tag=51)  # Toroid exception
            else:
                comm.send(downRightCorner, dest=rank + c + 1, tag=51)

            if columnNo == 1:
                comm.send(downLeftCorner, dest=rank + c - 1 + c, tag=52)  # Toroid exception
            else:
                comm.send(downLeftCorner, dest=rank + c - 1, tag=52)

            if columnNo == 1:
                if rowNo == 0:  # Toroid Exceptions
                    comm.send(upLeftCorner, dest=rank - c - 1 + c + c ** 2, tag=53)  # Toroid exceptions
                else:
                    comm.send(upLeftCorner, dest=rank - c - 1 + c, tag=53)
            else:
                if rowNo == 0:
                    comm.send(upLeftCorner, dest=rank - c - 1 + c ** 2, tag=53)
                else:
                    comm.send(upLeftCorner, dest=rank - c - 1, tag=53)

            if columnNo == WorkerNoOnAEdge:
                if rowNo == 0:  # Toroid Exceptions
                    comm.send(upRightCorner, dest=rank - c + 1 - c + c ** 2, tag=54)  # Toroid exceptions
                else:
                    comm.send(upRightCorner, dest=rank - c + 1 - c, tag=54)
            else:
                if rowNo == 0:
                    comm.send(upRightCorner, dest=rank - c + 1 + c ** 2, tag=54)
                else:
                    comm.send(upRightCorner, dest=rank - c + 1, tag=54)
        else:
            if columnNo == 1:
                upLeftNeighbour = comm.recv(source=rank - c - 1 + c, tag=51)
            else:
                upLeftNeighbour = comm.recv(source=rank - c - 1, tag=51)

            if columnNo == WorkerNoOnAEdge:
                upRightNeighbour = comm.recv(source=rank - c + 1 - c, tag=52)
            else:
                upRightNeighbour = comm.recv(source=rank - c + 1, tag=52)

            if columnNo == WorkerNoOnAEdge:
                if rowNo == WorkerNoOnAEdge - 1:  # Toroid Exceptions
                    downRightNeighbour = comm.recv(source=rank + c + 1 - c - c ** 2, tag=53)
                else:
                    downRightNeighbour = comm.recv(source=rank + c + 1 - c, tag=53)
            else:
                if rowNo == WorkerNoOnAEdge - 1:
                    downRightNeighbour = comm.recv(source=rank + c + 1 - c ** 2, tag=53)
                else:
                    downRightNeighbour = comm.recv(source=rank + c + 1, tag=53)

            if columnNo == 1:
                if rowNo == WorkerNoOnAEdge - 1:  # Toroid Exceptions
                    downLeftNeighbour = comm.recv(source=rank + c - 1 + c - c ** 2, tag=54)
                else:
                    downLeftNeighbour = comm.recv(source=rank + c - 1 + c, tag=54)
            else:
                if rowNo == WorkerNoOnAEdge - 1:
                    downLeftNeighbour = comm.recv(source=rank + c - 1 - c ** 2, tag=54)
                else:
                    downLeftNeighbour = comm.recv(source=rank + c - 1, tag=54)

        ### Process The Turn
        # Add neighboour information, make the grid size grid+2 with neighbour points added, then do the processing
        withNeighbourGrids = np.full((myEdge + 2, myEdge + 2), 0)
        withNeighbourGrids[0][0] = upLeftNeighbour
        withNeighbourGrids[0][1:myEdge + 1] = upNeighboursRow
        withNeighbourGrids[0][myEdge + 1] = upRightNeighbour

        withNeighbourGrids[myEdge + 1][0] = downLeftNeighbour
        withNeighbourGrids[myEdge + 1][1:myEdge + 1] = downNeighboursRow
        withNeighbourGrids[myEdge + 1][myEdge + 1] = downRightNeighbour
        withNeighbourGrids[np.ix_(np.arange(1, myEdge + 1), [0])] = leftNeighboursColumn.reshape(myEdge, 1)
        withNeighbourGrids[np.ix_(np.arange(1, myEdge + 1), [myEdge + 1])] = rightNeighboursColumn.reshape(myEdge, 1)

        position = np.arange(myEdge)
        position += 1
        withNeighbourGrids[np.ix_(position, position)] = myGrid

        # Processing for each point
        for i in range(1, myEdge + 1):
            for j in range(1, myEdge + 1):
                neighboursResult = withNeighbourGrids[i - 1][j - 1] + withNeighbourGrids[i - 1][j] + \
                                   withNeighbourGrids[i - 1][j + 1] + withNeighbourGrids[i][j - 1] + \
                                   withNeighbourGrids[i][j + 1] + \
                                   withNeighbourGrids[i + 1][j - 1] + withNeighbourGrids[i + 1][j] + \
                                   withNeighbourGrids[i + 1][j + 1]
                if withNeighbourGrids[i][j] == 1:
                    if neighboursResult < 2 or neighboursResult > 3:
                        myGrid[i - 1][j - 1] = 0
                else:
                    if neighboursResult == 3:
                        myGrid[i - 1][j - 1] = 1
        ### Round finished  ###

    # Send subMatrix to Central Worker
    data = comm.send(myGrid, dest=0, tag=2)
