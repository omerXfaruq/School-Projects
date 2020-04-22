import numpy as np
import matplotlib.pyplot as plt
import sys

matrixInput=sys.argv[1]
personInput=sys.argv[2]

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

print(len(Similarity_Matrix))

#input is output
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


matrixMin=int(np.min(Similarity_Matrix))
matrixMax=int(np.max(Similarity_Matrix))
outputs=np.zeros(2)
return_FFR_and_FAR(-78.744,Similarity_Matrix,outputs,True,True)
print(outputs)	

thresholdDistances=40
matrixMax=20
matrixMin=-300
resolution=int((matrixMax-matrixMin)/thresholdDistances)
aralıks=int((matrixMax-matrixMin)/resolution)


#testThresholds2=np.array([-4100,-3800,-3500,-3200,-2900,-2600,-2300,-2000,-1700,-1400,-1100,-800,-500,-300,-100])
testThresholds=np.array(range(int(matrixMin /aralıks),int(matrixMax/aralıks)+1))*aralıks
#testThresholds=np.concatenate([testThresholds,testThresholds2])
#testThresholds_old2=np.array(range(-100,-50))
#testThresholds_old3=np.divide(np.array(range(-787500,-787400)),10000)
#testThresholds_old4=np.divide(np.array(range(-4534,-4530)),100)


#Generating frr and far values for threshold values
print("Number of testThresholds:", len(testThresholds))
plotFRR=np.zeros(len(testThresholds))
plotFAR=np.zeros(len(testThresholds))
thresholdValues=np.zeros(len(testThresholds))
t=0
for i in testThresholds:
	print(i, ": th round")
	return_FFR_and_FAR(i,Similarity_Matrix,outputs)
	plotFRR[t]=outputs[0]
	plotFAR[t]=outputs[1]
	thresholdValues[t]=i
	t+=1

minDistanceEER=10**10
minDistance0_1=10**10
minDistance0_01=10**10
minDistance0_001=10**10
threshold0_1=-1
threshold0_01=-1
threshold0_001=-1

FARvalue=-1
FRRvalue=-1
EERthreshold=-1
#Finding the threshold close to EER
for i in range(len(testThresholds)):
	if abs(plotFAR[i]-plotFRR[i])<minDistanceEER:
		minDistanceEER=abs(plotFAR[i]-plotFRR[i])		
		FARvalue=plotFAR[i]
		FRRvalue=plotFRR[i]
		EERthreshold=thresholdValues[i]
		print("Far Frr EERthreshold: ", FARvalue, FRRvalue, EERthreshold)
	if abs(plotFAR[i]-0.1)<minDistance0_1:
		minDistance0_1=plotFAR[i]
		threshold0_1=i
	if abs(plotFAR[i]-0.01)<minDistance0_01:
		minDistance0_01=plotFAR[i]
		threshold0_01=i
	if abs(plotFAR[i]-0.001)<minDistance0_001:
		minDistance0_001=plotFAR[i]
		threshold0_001=i
print("FAR 0.1 0.01 0.001", plotFAR[threshold0_1], plotFAR[threshold0_01], plotFAR[threshold0_001])

#Generating frr and far values for threshold values closer to EER
testThresholds=np.array(range(int((EERthreshold-thresholdDistances)),int((EERthreshold+thresholdDistances))+1))
t=0
sec_plotFRR=np.zeros(len(testThresholds))
sec_plotFAR=np.zeros(len(testThresholds))
sec_thresholdValues=np.zeros(len(testThresholds))
for i in testThresholds:
	print(i, ": th round")
	return_FFR_and_FAR(i,Similarity_Matrix,outputs)
	sec_plotFRR[t]=outputs[0]
	sec_plotFAR[t]=outputs[1]
	sec_thresholdValues[t]=i
	t+=1
#Finding the EER
for i in range(len(testThresholds)):
	if abs(sec_plotFAR[i]-sec_plotFRR[i])<minDistanceEER:
		minDistanceEER=abs(sec_plotFAR[i]-sec_plotFRR[i])		
		FARvalue=sec_plotFAR[i]
		FRRvalue=sec_plotFRR[i]
		EERthreshold=sec_thresholdValues[i]
		print("Far Frr EERthreshold: ", FARvalue, FRRvalue, EERthreshold)
		print("minDistance is:", minDistanceEER)










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

print("Far Value:", FARvalue)
print("FRR Value:", FRRvalue)

#plt.hist(differentPersonData,1000)
