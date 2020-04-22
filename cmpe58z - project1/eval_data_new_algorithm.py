#By FarukOzderim

import numpy as np
import matplotlib.pyplot as plt
import sys

matrixInput=sys.argv[1]
personInput=sys.argv[2]
resolution=500					#Number of threshold values for the FAR/GAR graph
EERprecision=10**-2				#Convergence for EER, difference between FAR-FFR
FARvaluePrecisionRatio=10**-2	#Convergence for finding FAR value, difference between foundValue-searchedValue=searchedValıe*Ratio

samePersonData=[]
differentPersonData=[]

numberOfPhotos=0
with open(personInput) as f:
	numberOfPhotos=(len(f.readlines()))

Similarity_Matrix=np.zeros(numberOfPhotos**2).reshape(numberOfPhotos,numberOfPhotos)
minus_infinity=10**-10
ownerClasses=np.zeros(numberOfPhotos)
with open(matrixInput, 'r') as f:	
	i=0
	for line in f:
		splited=line.split(',')
		splited[i]=minus_infinity
		#print(splited)
		Similarity_Matrix[i]= splited
		#print(Similarity_Matrix)
		i+=1
with open(personInput, 'r') as f:
	i=0	
	for line in f:
	    ownerClasses[i]=int(line)
	    i+=1

print("Number Photos:",len(Similarity_Matrix))

#Returning FFR and FAR values via output variable
def return_FFR_and_FAR(threshold,similarity_matrix,output,boolean=False,lookForImpostorData=False):
	frrNo=0
	farNo=0
	samePersonComparisonNo=0
	differentPersonComparisonNo=0
	if lookForImpostorData:
		global samePersonData
		global differentPersonData
	
	for i in range(numberOfPhotos):
		j=i+1
		while j<numberOfPhotos:
			if ownerClasses[j]==ownerClasses[i]:
				samePersonComparisonNo+=1
				if lookForImpostorData:
					samePersonData.append(similarity_matrix[i,j])
				if similarity_matrix[i,j]<threshold:
					frrNo+=1	##frr sample detected
			else:
				differentPersonComparisonNo+=1
				if lookForImpostorData:
					differentPersonData.append(similarity_matrix[i,j])
				if similarity_matrix[i,j]>threshold:
					farNo+=1
			j+=1
	output[0]=frrNo/samePersonComparisonNo
	output[1]=farNo/differentPersonComparisonNo
	
	if boolean:
		print("SamePersonNo: ", samePersonComparisonNo)
		print("differentPersonComparisonNo:", differentPersonComparisonNo)
matrixMin=(np.min(Similarity_Matrix))
matrixMax=(np.max(Similarity_Matrix))
outputs=np.zeros(2)

#Calculate genuine and impostor graphs

return_FFR_and_FAR(0,Similarity_Matrix,outputs,True,True)


#print(outputs)	
#print(matrixMax)
#print(matrixMin)
#thresholdDistances=100


aralıks=((matrixMax-matrixMin)/resolution)
testThresholds=np.array(range(int(matrixMin /aralıks),int(matrixMax/aralıks)+1))*aralıks


############################################################

#Generating frr and far values for threshold values
print("Number of testThresholds:", len(testThresholds))
plotFRR=np.zeros(len(testThresholds))
plotFAR=np.zeros(len(testThresholds))
thresholdValues=np.zeros(len(testThresholds))
t=0
for i in testThresholds:
	print(t,"th threshold:",i)
	return_FFR_and_FAR(i,Similarity_Matrix,outputs)
	plotFRR[t]=outputs[0]
	plotFAR[t]=outputs[1]
	thresholdValues[t]=i
	t+=1

############################################################

#Find EER point
jump=((matrixMax-matrixMin)/10)
startPoint=(matrixMax*1.1)

return_FFR_and_FAR(startPoint,Similarity_Matrix,outputs)
far=outputs[1]
frr=outputs[0]
frrIsBigger=True
k=0
while abs(far-frr)>EERprecision:
	startPoint-=jump
	return_FFR_and_FAR(startPoint,Similarity_Matrix,outputs)
	far=outputs[1]
	frr=outputs[0]
	if frrIsBigger:
		if far>frr:
			frrIsBigger=False
			jump=-1*jump/2
	else:
		if far<frr:
			frrIsBigger=True
			jump=-1*jump/2

print("FAR:",far,"FRR:",frr,"Threshold:",startPoint)
EERvalue=(far+frr)/2
print("EER:",EERvalue)
EERthreshold=startPoint

############################################################

#finds Far value Points location
def findFarPoint(value):
	global matrixMin
	global matrixMax
	global Similarity_Matrix
	global outputs

	#Find FAR %value point
	jump=((matrixMax-matrixMin)/10)
	startPoint=(matrixMax*1.1)
	return_FFR_and_FAR(startPoint,Similarity_Matrix,outputs)
	far=outputs[1]
	frr=outputs[0]
	farIsNotBigger=True
	while abs(far-value)>value*FARvaluePrecisionRatio:
		startPoint-=jump
		return_FFR_and_FAR(startPoint,Similarity_Matrix,outputs)
		far=outputs[1]
		if farIsNotBigger:
			if far>value:
				farIsNotBigger=False
				jump=-1*jump/2
		else:
			if far<value:
				farIsNotBigger=True
				jump=-1*jump/2
	return startPoint


value0_1=findFarPoint(0.1)
value0_01=findFarPoint(0.01)
value0_001=findFarPoint(0.001)

print("EER value, threshold:", EERvalue, EERthreshold)

output_0_1=np.zeros(2)
output_0_01=np.zeros(2)
output_0_001=np.zeros(2)
return_FFR_and_FAR(value0_1,Similarity_Matrix,output_0_1)
return_FFR_and_FAR(value0_01,Similarity_Matrix,output_0_01)
return_FFR_and_FAR(value0_001,Similarity_Matrix,output_0_001)
print("0.1 FAR and corresponding FFR:", output_0_1[1],"-",output_0_1[0])
print("0.01 FAR and corresponding FFR:",output_0_01[1],"-",output_0_01[0])
print("0.001 FAR and corresponding FFR:",output_0_001[1],"-",output_0_001[0])

############################################################
#Plots

plt.hist([samePersonData,differentPersonData],bins='auto',density=True,label=['Genuine','Impostor'])
plt.xlabel('Score')
plt.ylabel('Frequency')
plt.legend()
plt.show()

plt.plot(plotFAR,1-plotFRR,'b')
plt.xlabel('FAR')
plt.ylabel('GAR')
plt.title('ROC')
plt.show()