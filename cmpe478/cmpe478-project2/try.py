from mpi4py import MPI
import numpy as np
import sys

# Author: Ömer Faruk Özdemir
# Date: 16.05.2020
# mpiexec --oversubscribe -np [x^3] python3 test.py [N]
# example:
# mpiexec --oversubscribe -np 8 python3 test.py 7
# Note that x needs to divide N+1


step=0
edgeOfCube = int(sys.argv[1])+1    # N+1
convergenceDifference=0.0001    #Tested for convergence 

comm = MPI.COMM_WORLD
processerNo = MPI.COMM_WORLD.Get_size()
rank = int(comm.Get_rank())


noOfProcesserOnAEdge=int(round(processerNo**(1/3)))

if edgeOfCube%noOfProcesserOnAEdge!=0 or edgeOfCube/noOfProcesserOnAEdge<=0:
	if rank==0:
		print("x needs to divide N, pls read README")
	sys.exit()

lengthOfProcessersEdge = round((edgeOfCube/processerNo**(1/3))) 
row=-1
column=-1
depth=-1

miniMapOfProcessor=np.zeros(lengthOfProcessersEdge**3).reshape(lengthOfProcessersEdge,lengthOfProcessersEdge,lengthOfProcessersEdge)
updatedMiniMapOfProcessor=np.zeros(lengthOfProcessersEdge**3).reshape(lengthOfProcessersEdge,lengthOfProcessersEdge,lengthOfProcessersEdge)

row=int(rank/noOfProcesserOnAEdge**2)
column=int((int(rank/noOfProcesserOnAEdge)) %noOfProcesserOnAEdge)
height=int(rank%noOfProcesserOnAEdge)

leftNeighboursData=None
rightNeighboursData=None
aboveNeighboursData=None
belowNeighboursData=None
insideNeighboursData=None
outsideNeighboursData=None


#f=uxx+uyy+uzz=0+0+0=0
fValue=0
constantPartWithF=-1/6/np.pi/np.pi*fValue

#ui;j;k =1/6[u i+1;j;k+u i-1; j;k +u i; j+1;k +u i; j-1;k +u i; j;k+1+u i; j;k-1]-1/6n2 f i;j;k

#inside is -1 for 3d
#outside is +1 for 3d


#positions [row][column][height]
#u=x*y*z
def exacFunction(positions):
	return (positions[0]*positions[1]*positions[2])/edgeOfCube/edgeOfCube/edgeOfCube


def calculatePointBySurroundings(i,j,k):
	return 1/6*(miniMapOfProcessor[i-1][j][k]+miniMapOfProcessor[i+1][j][k]\
				+miniMapOfProcessor[i][j-1][k]+miniMapOfProcessor[i][j+1][k]\
				+miniMapOfProcessor[i][j][k-1]+miniMapOfProcessor[i][j][k+1])\
				+constantPartWithF

#Boundary planes	
def aboveBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(aboveNeighboursData[j][k]+miniMapOfProcessor[i+1][j][k]\
					+miniMapOfProcessor[i][j-1][k]+miniMapOfProcessor[i][j+1][k]\
				+miniMapOfProcessor[i][j][k-1]+miniMapOfProcessor[i][j][k+1])\
				+constantPartWithF

def belowBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(miniMapOfProcessor[i-1][j][k]+belowNeighboursData[j][k]\
		+miniMapOfProcessor[i][j-1][k]+miniMapOfProcessor[i][j+1][k]\
		+miniMapOfProcessor[i][j][k-1]+miniMapOfProcessor[i][j][k+1])\
		+constantPartWithF			

def leftBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(miniMapOfProcessor[i-1][j][k]+miniMapOfProcessor[i+1][j][k]\
		+leftNeighboursData[i][k]+miniMapOfProcessor[i][j+1][k]\
		+miniMapOfProcessor[i][j][k-1]+miniMapOfProcessor[i][j][k+1])\
		+constantPartWithF
	
def rightBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(miniMapOfProcessor[i-1][j][k]+miniMapOfProcessor[i+1][j][k]\
		+miniMapOfProcessor[i][j-1][k]+rightNeighboursData[i][k]\
		+miniMapOfProcessor[i][j][k-1]+miniMapOfProcessor[i][j][k+1])\
		+constantPartWithF

def insideBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(miniMapOfProcessor[i-1][j][k]+miniMapOfProcessor[i+1][j][k]\
		+miniMapOfProcessor[i][j-1][k]+miniMapOfProcessor[i][j+1][k]\
		+insideNeighboursData[i][j]+miniMapOfProcessor[i][j][k+1])\
		+constantPartWithF

def outsideBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(miniMapOfProcessor[i-1][j][k]+miniMapOfProcessor[i+1][j][k]\
		+miniMapOfProcessor[i][j-1][k]+miniMapOfProcessor[i][j+1][k]\
		+miniMapOfProcessor[i][j][k-1]+outsideNeighboursData[i][j])\
		+constantPartWithF

#Edges
def aboveLeftBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(aboveNeighboursData[j][k]+miniMapOfProcessor[i+1][j][k]\
					+leftNeighboursData[i][k]+miniMapOfProcessor[i][j+1][k]\
				+miniMapOfProcessor[i][j][k-1]+miniMapOfProcessor[i][j][k+1])\
				+constantPartWithF

def aboveRightBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(aboveNeighboursData[j][k]+miniMapOfProcessor[i+1][j][k]\
					+miniMapOfProcessor[i][j-1][k]+rightNeighboursData[i][k]\
				+miniMapOfProcessor[i][j][k-1]+miniMapOfProcessor[i][j][k+1])\
				+constantPartWithF

def aboveInsideBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(aboveNeighboursData[j][k]+miniMapOfProcessor[i+1][j][k]\
					+miniMapOfProcessor[i][j-1][k]+miniMapOfProcessor[i][j+1][k]\
				+insideNeighboursData[i][j]+miniMapOfProcessor[i][j][k+1])\
				+constantPartWithF

def aboveOutsideBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(aboveNeighboursData[j][k]+miniMapOfProcessor[i+1][j][k]\
					+miniMapOfProcessor[i][j-1][k]+miniMapOfProcessor[i][j+1][k]\
				+miniMapOfProcessor[i][j][k-1]+outsideNeighboursData[i][j])\
				+constantPartWithF

def belowLeftBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(belowNeighboursData[j][k]+miniMapOfProcessor[i-1][j][k]\
					+leftNeighboursData[i][k]+miniMapOfProcessor[i][j+1][k]\
				+miniMapOfProcessor[i][j][k-1]+miniMapOfProcessor[i][j][k+1])\
				+constantPartWithF

def belowRightBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(belowNeighboursData[j][k]+miniMapOfProcessor[i-1][j][k]\
					+miniMapOfProcessor[i][j-1][k]+rightNeighboursData[i][k]\
				+miniMapOfProcessor[i][j][k-1]+miniMapOfProcessor[i][j][k+1])\
				+constantPartWithF

def belowInsideBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(belowNeighboursData[j][k]+miniMapOfProcessor[i-1][j][k]\
					+miniMapOfProcessor[i][j-1][k]+miniMapOfProcessor[i][j+1][k]\
				+insideNeighboursData[i][j]+miniMapOfProcessor[i][j][k+1])\
				+constantPartWithF

def belowOutsideBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(belowNeighboursData[j][k]+miniMapOfProcessor[i-1][j][k]\
					+miniMapOfProcessor[i][j-1][k]+miniMapOfProcessor[i][j+1][k]\
				+miniMapOfProcessor[i][j][k-1]+outsideNeighboursData[i][j])\
				+constantPartWithF

def leftInsideBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(miniMapOfProcessor[i-1][j][k]+miniMapOfProcessor[i+1][j][k]\
		+leftNeighboursData[i][k]+miniMapOfProcessor[i][j+1][k]\
		+insideNeighboursData[i][j]+miniMapOfProcessor[i][j][k+1])\
		+constantPartWithF

def leftOutsideBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(miniMapOfProcessor[i-1][j][k]+miniMapOfProcessor[i+1][j][k]\
		+leftNeighboursData[i][k]+miniMapOfProcessor[i][j+1][k]\
		+miniMapOfProcessor[i][j][k-1]+outsideNeighboursData[i][j])\
		+constantPartWithF
	
def rightInsideBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(miniMapOfProcessor[i-1][j][k]+miniMapOfProcessor[i+1][j][k]\
		+rightNeighboursData[i][k]+miniMapOfProcessor[i][j-1][k]\
		+insideNeighboursData[i][j]+miniMapOfProcessor[i][j][k+1])\
		+constantPartWithF

def rightOutsideBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(miniMapOfProcessor[i-1][j][k]+miniMapOfProcessor[i+1][j][k]\
		+rightNeighboursData[i][k]+miniMapOfProcessor[i][j-1][k]\
		+miniMapOfProcessor[i][j][k-1]+outsideNeighboursData[i][j])\
		+constantPartWithF

#Corners
def aboveLeftInsideBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(aboveNeighboursData[j][k]+miniMapOfProcessor[i+1][j][k]\
					+leftNeighboursData[i][k]+miniMapOfProcessor[i][j+1][k]\
				+insideNeighboursData[i][j]+miniMapOfProcessor[i][j][k+1])\
				+constantPartWithF

def aboveLeftOutsideBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(aboveNeighboursData[j][k]+miniMapOfProcessor[i+1][j][k]\
					+leftNeighboursData[i][k]+miniMapOfProcessor[i][j+1][k]\
				+miniMapOfProcessor[i][j][k-1]+outsideNeighboursData[i][j])\
				+constantPartWithF

def aboveRightInsideBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(aboveNeighboursData[j][k]+miniMapOfProcessor[i+1][j][k]\
					+miniMapOfProcessor[i][j-1][k]+rightNeighboursData[i][k]\
				+insideNeighboursData[i][j]+miniMapOfProcessor[i][j][k+1])\
				+constantPartWithF

def aboveRightOutsideBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(aboveNeighboursData[j][k]+miniMapOfProcessor[i+1][j][k]\
					+miniMapOfProcessor[i][j-1][k]+rightNeighboursData[i][k]\
				+miniMapOfProcessor[i][j][k-1]+outsideNeighboursData[i][j])\
				+constantPartWithF

def belowLeftInsideBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(belowNeighboursData[j][k]+miniMapOfProcessor[i-1][j][k]\
					+leftNeighboursData[i][k]+miniMapOfProcessor[i][j+1][k]\
				+insideNeighboursData[i][j]+miniMapOfProcessor[i][j][k+1])\
				+constantPartWithF

def belowLeftOutsideBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(belowNeighboursData[j][k]+miniMapOfProcessor[i-1][j][k]\
					+leftNeighboursData[i][k]+miniMapOfProcessor[i][j+1][k]\
				+miniMapOfProcessor[i][j][k-1]+outsideNeighboursData[i][j])\
				+constantPartWithF

def belowRightInsideBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(belowNeighboursData[j][k]+miniMapOfProcessor[i-1][j][k]\
					+miniMapOfProcessor[i][j-1][k]+rightNeighboursData[i][k]\
				+insideNeighboursData[i][j]+miniMapOfProcessor[i][j][k+1])\
				+constantPartWithF

def belowRightOutsideBoundaryCalculatePointBySurroundings(i,j,k):
	return 1/6*(belowNeighboursData[j][k]+miniMapOfProcessor[i-1][j][k]\
					+miniMapOfProcessor[i][j-1][k]+rightNeighboursData[i][k]\
				+miniMapOfProcessor[i][j][k-1]+outsideNeighboursData[i][j])\
				+constantPartWithF


def getProcesserNo(row,column,height):
	return row*noOfProcesserOnAEdge**2 + column*noOfProcesserOnAEdge + height

#Converts convertMiniProcesserMapPositions To Real Positions
def convertPosition(relativeVector,row,column,height):
	return (relativeVector[0]+row*lengthOfProcessersEdge,relativeVector[1]+column*lengthOfProcessersEdge,relativeVector[2]+height*lengthOfProcessersEdge)

#Assign boundary Values with exacFunction
def assignBoundaryValues():
	if row==0:
		for i in range(lengthOfProcessersEdge):
			for j in range(lengthOfProcessersEdge):
				miniMapOfProcessor[0,i,j]=exacFunction(convertPosition((0,i,j),row,column,height))

	if row==noOfProcesserOnAEdge-1:
		for i in range(lengthOfProcessersEdge):
			for j in range(lengthOfProcessersEdge):
				miniMapOfProcessor[lengthOfProcessersEdge-1,i,j]=exacFunction(convertPosition((lengthOfProcessersEdge-1,i,j),row,column,height))

	if column==0:
		for i in range(lengthOfProcessersEdge):
			for j in range(lengthOfProcessersEdge):
				miniMapOfProcessor[i,0,j]=exacFunction(convertPosition((i,0,j),row,column,height))

	if column==noOfProcesserOnAEdge-1:
		for i in range(lengthOfProcessersEdge):
			for j in range(lengthOfProcessersEdge):
				miniMapOfProcessor[i,lengthOfProcessersEdge-1,j]=exacFunction(convertPosition((i,lengthOfProcessersEdge-1,j),row,column,height))

	if height==0:
		for i in range(lengthOfProcessersEdge):
			for j in range(lengthOfProcessersEdge):
				miniMapOfProcessor[i,j,0]=exacFunction(convertPosition((i,j,0),row,column,height))

	if height==noOfProcesserOnAEdge-1:
		for i in range(lengthOfProcessersEdge):
			for j in range(lengthOfProcessersEdge):
				miniMapOfProcessor[i,j,lengthOfProcessersEdge-1]=exacFunction(convertPosition((i,j,lengthOfProcessersEdge-1),row,column,height))

#Starts communication with neighbour subcubs 
def startCommunicationWithNeighbours():
	
	global req1 				
	global req2
	global req3
	global req4
	global req5
	global req6
	global reqFromOutside
	global reqFromInside
	global reqFromRight
	global reqFromLeft	
	global reqFromBelow
	global reqFromAbove

	if row!=0:
		req1=comm.isend(miniMapOfProcessor[0,:,:],dest=getProcesserNo(row-1,column,height),tag=1)
		reqFromAbove=comm.irecv(source=getProcesserNo(row-1,column,height),tag=2)			
	
	if row!=noOfProcesserOnAEdge-1:
		req2=comm.isend(miniMapOfProcessor[lengthOfProcessersEdge-1,:,:],dest=getProcesserNo(row+1,column,height),tag=2)
		reqFromBelow=comm.irecv(source=getProcesserNo(row+1,column,height),tag=1)			
	
	if column!=0:
		req3=comm.isend(miniMapOfProcessor[:,0,:],dest=getProcesserNo(row,column-1,height),tag=3)
		reqFromLeft=comm.irecv(source=getProcesserNo(row,column-1,height),tag=4)			
	
	if column!=noOfProcesserOnAEdge-1:
		req4=comm.isend(miniMapOfProcessor[:,lengthOfProcessersEdge-1,:],dest=getProcesserNo(row,column+1,height),tag=4)
		reqFromRight=comm.irecv(source=getProcesserNo(row,column+1,height),tag=3)			
	
	if height!=0:
		req5=comm.isend(miniMapOfProcessor[:,:,0],dest=getProcesserNo(row,column,height-1),tag=5)
		reqFromInside=comm.irecv(source=getProcesserNo(row,column,height-1),tag=6)			
	
	if height!=noOfProcesserOnAEdge-1:
		req6=comm.isend(miniMapOfProcessor[:,:,lengthOfProcessersEdge-1],dest=getProcesserNo(row,column,height+1),tag=6)
		reqFromOutside=comm.irecv(source=getProcesserNo(row,column,height+1),tag=5)	

#Subcube Boundary points calculation
def subcubeBoundaryPointsCalculation():
	global aboveNeighboursData
	global belowNeighboursData
	global rightNeighboursData
	global leftNeighboursData
	global insideNeighboursData
	global outsideNeighboursData


	#Calculate inner points in boundary planes
	if row!=0:
		req1.wait()
		aboveNeighboursData=reqFromAbove.wait()
		for j in range(1,lengthOfProcessersEdge-1):
			for k in range(1,lengthOfProcessersEdge-1):
				updatedMiniMapOfProcessor[0,j,k]=aboveBoundaryCalculatePointBySurroundings(0,j,k)

	if row!=noOfProcesserOnAEdge-1:
		req2.wait()
		belowNeighboursData=reqFromBelow.wait()
		for j in range(1,lengthOfProcessersEdge-1):
			for k in range(1,lengthOfProcessersEdge-1):
				updatedMiniMapOfProcessor[lengthOfProcessersEdge-1,j,k]=belowBoundaryCalculatePointBySurroundings(lengthOfProcessersEdge-1,j,k)

	if column!=0:
		req3.wait()
		leftNeighboursData=reqFromLeft.wait()
		for i in range(1,lengthOfProcessersEdge-1):
			for k in range(1,lengthOfProcessersEdge-1):
				updatedMiniMapOfProcessor[i,0,k]=leftBoundaryCalculatePointBySurroundings(i,0,k)

	if column!=noOfProcesserOnAEdge-1:
		req4.wait()
		rightNeighboursData=reqFromRight.wait()
		for i in range(1,lengthOfProcessersEdge-1):
			for k in range(1,lengthOfProcessersEdge-1):
				updatedMiniMapOfProcessor[i,lengthOfProcessersEdge-1,k]=rightBoundaryCalculatePointBySurroundings(i,lengthOfProcessersEdge-1,k)
	
	if height!=0:
		req5.wait()
		insideNeighboursData=reqFromInside.wait()
		for i in range(1,lengthOfProcessersEdge-1):
			for j in range(1,lengthOfProcessersEdge-1):
				updatedMiniMapOfProcessor[i,j,0]=insideBoundaryCalculatePointBySurroundings(i,j,0)

	if height!=noOfProcesserOnAEdge-1:
		req6.wait()
		outsideNeighboursData=reqFromOutside.wait()
		for i in range(1,lengthOfProcessersEdge-1):
			for j in range(1,lengthOfProcessersEdge-1):
				updatedMiniMapOfProcessor[i,j,lengthOfProcessersEdge-1]=outsideBoundaryCalculatePointBySurroundings(i,j,lengthOfProcessersEdge-1)

	#Calculate edges and corners on boundary planes
	#Note that edge points have 2 subcube neighbour ponints, and corner points have 3 subcube corner points.

	#Edges
	if row!=0 and column !=0:
		for k in range(1,lengthOfProcessersEdge-1):
			updatedMiniMapOfProcessor[0,0,k]=aboveLeftBoundaryCalculatePointBySurroundings(0,0,k)

	if row!=noOfProcesserOnAEdge-1 and column!=0:
		for k in range(1,lengthOfProcessersEdge-1):
			updatedMiniMapOfProcessor[lengthOfProcessersEdge-1,0,k]=belowLeftBoundaryCalculatePointBySurroundings(lengthOfProcessersEdge-1,0,k)

	if row!=0 and column!=noOfProcesserOnAEdge-1:
		for k in range(1,lengthOfProcessersEdge-1):
			updatedMiniMapOfProcessor[0,lengthOfProcessersEdge-1,k]=aboveRightBoundaryCalculatePointBySurroundings(0,lengthOfProcessersEdge-1,k)

	if row!=noOfProcesserOnAEdge-1 and column!=noOfProcesserOnAEdge-1:
		for k in range(1,lengthOfProcessersEdge-1):
			updatedMiniMapOfProcessor[lengthOfProcessersEdge-1,lengthOfProcessersEdge-1,k]=belowRightBoundaryCalculatePointBySurroundings(lengthOfProcessersEdge-1,lengthOfProcessersEdge-1,k)


	if row!=0 and height !=0:
		for j in range(1,lengthOfProcessersEdge-1):
			updatedMiniMapOfProcessor[0,j,0]=aboveInsideBoundaryCalculatePointBySurroundings(0,j,0)

	if row!=noOfProcesserOnAEdge-1 and height!=0:
		for j in range(1,lengthOfProcessersEdge-1):
			updatedMiniMapOfProcessor[lengthOfProcessersEdge-1,j,0]=belowInsideBoundaryCalculatePointBySurroundings(lengthOfProcessersEdge-1,j,0)

	if row!=0 and height!=noOfProcesserOnAEdge-1:
		for j in range(1,lengthOfProcessersEdge-1):
			updatedMiniMapOfProcessor[0,j,lengthOfProcessersEdge-1]=aboveOutsideBoundaryCalculatePointBySurroundings(0,j,lengthOfProcessersEdge-1)

	if row!=noOfProcesserOnAEdge-1 and height!=noOfProcesserOnAEdge-1:
		for j in range(1,lengthOfProcessersEdge-1):
			updatedMiniMapOfProcessor[lengthOfProcessersEdge-1,j,lengthOfProcessersEdge-1]=belowOutsideBoundaryCalculatePointBySurroundings(lengthOfProcessersEdge-1,j,lengthOfProcessersEdge-1)


	
	if height!=0 and column !=0:
		for i in range(1,lengthOfProcessersEdge-1):
			updatedMiniMapOfProcessor[i,0,0]=leftInsideBoundaryCalculatePointBySurroundings(i,0,0)

	if height!=noOfProcesserOnAEdge-1 and column!=0:
		for i in range(1,lengthOfProcessersEdge-1):
			updatedMiniMapOfProcessor[i,0,lengthOfProcessersEdge-1]=leftOutsideBoundaryCalculatePointBySurroundings(i,0,lengthOfProcessersEdge-1)

	if height!=0 and column!=noOfProcesserOnAEdge-1:
		for i in range(1,lengthOfProcessersEdge-1):
			updatedMiniMapOfProcessor[i,lengthOfProcessersEdge-1,0]=rightInsideBoundaryCalculatePointBySurroundings(i,lengthOfProcessersEdge-1,0)

	if height!=noOfProcesserOnAEdge-1 and column!=noOfProcesserOnAEdge-1:
		for i in range(1,lengthOfProcessersEdge-1):
			updatedMiniMapOfProcessor[i,lengthOfProcessersEdge-1,lengthOfProcessersEdge-1]=rightOutsideBoundaryCalculatePointBySurroundings(i,lengthOfProcessersEdge-1,lengthOfProcessersEdge-1)


	#Corners
	if row!=0 and column !=0:
		if height!=0:
			updatedMiniMapOfProcessor[0,0,0]=aboveLeftInsideBoundaryCalculatePointBySurroundings(0,0,0)
		
		if height!=noOfProcesserOnAEdge-1:
			updatedMiniMapOfProcessor[0,0,lengthOfProcessersEdge-1]=aboveLeftOutsideBoundaryCalculatePointBySurroundings(0,0,lengthOfProcessersEdge-1)

	if row!=noOfProcesserOnAEdge-1 and column!=0:
		if height!=0:
			updatedMiniMapOfProcessor[lengthOfProcessersEdge-1,0,0]=belowLeftInsideBoundaryCalculatePointBySurroundings(lengthOfProcessersEdge-1,0,0)
		
		if height!=noOfProcesserOnAEdge-1:
			updatedMiniMapOfProcessor[lengthOfProcessersEdge-1,0,lengthOfProcessersEdge-1]=belowLeftOutsideBoundaryCalculatePointBySurroundings(lengthOfProcessersEdge-1,0,lengthOfProcessersEdge-1)

	if row!=0 and column!=noOfProcesserOnAEdge-1:
		if height!=0:
			updatedMiniMapOfProcessor[0,lengthOfProcessersEdge-1,0]=aboveRightInsideBoundaryCalculatePointBySurroundings(0,lengthOfProcessersEdge-1,0)
		
		if height!=noOfProcesserOnAEdge-1:
			updatedMiniMapOfProcessor[0,lengthOfProcessersEdge-1,lengthOfProcessersEdge-1]=aboveRightOutsideBoundaryCalculatePointBySurroundings(0,lengthOfProcessersEdge-1,lengthOfProcessersEdge-1)

	if row!=noOfProcesserOnAEdge-1 and column!=noOfProcesserOnAEdge-1:
		if height!=0:
			updatedMiniMapOfProcessor[lengthOfProcessersEdge-1,lengthOfProcessersEdge-1,0]=belowRightInsideBoundaryCalculatePointBySurroundings(lengthOfProcessersEdge-1,lengthOfProcessersEdge-1,0)

		if height!=noOfProcesserOnAEdge-1:
			updatedMiniMapOfProcessor[lengthOfProcessersEdge-1,lengthOfProcessersEdge-1,lengthOfProcessersEdge-1]=belowRightOutsideBoundaryCalculatePointBySurroundings(lengthOfProcessersEdge-1,lengthOfProcessersEdge-1,lengthOfProcessersEdge-1)




#############################
######### Main ##############
#############################



#Initial values assigned to boundary points on the cube
assignBoundaryValues()
updatedMiniMapOfProcessor=miniMapOfProcessor.copy()

req1=None
req2=None
req3=None
req4=None
req5=None
req6=None

reqFromOutside=None	
reqFromInside=None
reqFromRight=None	
reqFromLeft	=None
reqFromBelow=None	
reqFromAbove=None	



while(True):
	#Starts communication with neighbour subcubes
	startCommunicationWithNeighbours()
	
	#Inner points calculation
	for i in range(1,lengthOfProcessersEdge-1):
		for j in range(1,lengthOfProcessersEdge-1):
			for k in range(1,lengthOfProcessersEdge-1):
				updatedMiniMapOfProcessor[i,j,k]=calculatePointBySurroundings(i,j,k)
	
	#Boundary points calculation
	subcubeBoundaryPointsCalculation()

	#Check for convergence wrt to previous values
	maxDistance=-1
	sumDistance=0
	for i in range(1,lengthOfProcessersEdge-1):
		for j in range(1,lengthOfProcessersEdge-1):
			for k in range(1,lengthOfProcessersEdge-1):
				absValue=abs(miniMapOfProcessor[i,j,k]-updatedMiniMapOfProcessor[i,j,k])
				maxDistance=max(maxDistance,absValue)
				sumDistance+=absValue

	#Update values
	miniMapOfProcessor=updatedMiniMapOfProcessor.copy()

	myMax = np.array(maxDistance,'d')
	mySum = np.array(sumDistance,'d')
	all_max = np.array(0.0,'d')
	all_sum = np.array(0.0,'d')
	comm.Reduce(myMax, all_max, op=MPI.MAX, root=0)
	comm.Reduce(mySum, all_sum, op=MPI.SUM, root=0)
	
	step+=1
	#Check convergence
	letsFinish=-1
	if rank == 0:
		if all_sum<convergenceDifference:
			letsFinish=1
		else:
			letsFinish=0  
	
	# broadcast letsFinish
	letsFinish = comm.bcast(letsFinish, root=0)
	
	differenceToExactFunction=0
	maxDifferenceToExactFunction=0
	sumDifferenceToExactFunction=0

	if letsFinish==1:


		#Calculate difference with exact function		
		for i in range(1,lengthOfProcessersEdge-1):
			for j in range(1,lengthOfProcessersEdge-1):
				for k in range(1,lengthOfProcessersEdge-1):
					absValue=abs(miniMapOfProcessor[i,j,k]-exacFunction(convertPosition((i,j,k),row,column,height)))
					maxDifferenceToExactFunction=max(maxDifferenceToExactFunction,absValue)
					sumDifferenceToExactFunction+=absValue
		
		maxDifferenceToExactFunction = np.array(maxDifferenceToExactFunction,'d')
		sumDifferenceToExactFunction = np.array(sumDifferenceToExactFunction,'d')
		exact_all_max = np.array(0.0,'d')
		exact_all_sum = np.array(0.0,'d')
		comm.Reduce(maxDifferenceToExactFunction, exact_all_max, op=MPI.MAX, root=0)
		comm.Reduce(sumDifferenceToExactFunction, exact_all_sum, op=MPI.SUM, root=0)

		#Print out result
		if rank==0:
			print("Step:",step,"sum difference to previous step: ",all_sum)
			print("Step:",step,"max difference to previous step: ",all_max)
			print("Step:",step,"sum difference to exact function: ",exact_all_sum)
			print("Step:",step,"max difference to exact function: ",exact_all_max)

		break
	
	#Synchronize
	comm.barrier()	


if rank==0:
	print("TotalStep:",step)
