import gym
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import sys
env = gym.make("CartPole-v1")
numberOfEpisodes=1000
plotData=np.zeros(numberOfEpisodes)
#Use the pole angle and pole angle speed data
#Position and velocity of the cart is a little side objective, and can be solved by solving pole angle&angle velocity

thetas=np.array([[np.random.random()*1,np.random.random()*1,np.random.random()*1,np.random.random()*1,np.random.random()*1],[np.random.random()*1,np.random.random()*1,np.random.random()*1,np.random.random()*1,np.random.random()*1]])

### TODO: try moment but dont try hard

#ALPHA=0.01
#epsilon=0.01
gama=0.999

#Epsilon starts with 1 and drops to with time
def chooseEpsilon(time):
	return 0.99 ** time

#Alpha is 0.01
def chooseAlpha(time):
    return 0.01

#Choose random action with probabilty epsilon
def chooseAction(epsilon,oldObservation):
	if np.random.random()<epsilon:
		return int(np.random.random()*2)
	else:
		return np.argmax(outputOfModel(oldObservation))

def activationFunction(x):
	return 1/(1+math.exp(-1*x))

		
#Update Model
def updateModel(oldObservation,newObservation,action,reward,alpha):
	thetasUpdate=np.array([0.0,0.0,0.0,0.0,0.0])
	oldOutput=outputOfModel(oldObservation)
	newOutput=outputOfModel(newObservation)
	for j in range(4):
		thetasUpdate[j]+=-1*alpha*(oldObservation[j])*(oldOutput[action]-(reward+gama*np.max(newOutput)))
	thetasUpdate[4]+=-1*alpha*(oldOutput[action]-(reward+gama*np.max(newOutput)))
	
	global thetas
	for j in range(5):
		thetas[action][j]+=(thetasUpdate[j])
		if thetas[action][j]>0:
			thetas[action][j]=min(100.0,thetas[action][j])
		else:

			thetas[action][j]=max(-100-.0,thetas[action][j])		


#Returns output of the model
def outputOfModel(state):
	outputs=np.zeros(2)
	for i in range(4):
		outputs[0]+=(state[i])*thetas[0][i]
		outputs[1]+=(state[i])*thetas[1][i]
	outputs[0]+=thetas[0][4]
	outputs[1]+=thetas[1][4]
	
	return outputs

#State conversion is currently inactive
def convertState(state):
	
	#angle=state[2]
	#angle= angle%np.radians(360)
	#angle=1*(angle-np.radians(180))
	#state[2]=angle
	#State regularizations are closed.
	#angle=angle-np.radians(180)
	#state[0]=0 
	#state[0]=state[0]/10
	#state[1]=0 
	#state[1]=state[1]/5
	#state[2]=state[2]
	#state[3]=state[3]/5
	return state

accumulatedReward=0
#First 500 rounds, mainly for training
for time in range(numberOfEpisodes):
	roundSurvival=0
	alpha=chooseAlpha(time)
	epsilon=chooseEpsilon(time)
	oldObservation=env.reset()
	oldObservation=convertState(oldObservation)
	for survival in range(500):		
		#env.render()
		action=chooseAction(epsilon,oldObservation)
		newObservation, reward, done, info = env.step(action)
		accumulatedReward+=reward
		roundSurvival+=reward

		newObservation=convertState(newObservation)
		updateModel(oldObservation,newObservation,action,reward,alpha)

		oldObservation=newObservation

	plotData[time]=roundSurvival
	print(time, "Round reward and epsilon is:",roundSurvival, epsilon)


plt.plot(plotData)
plt.show()



#Test part after training

print(thetas)
average1=accumulatedReward/500
print("Average rewards in first 500 rounds is:",average1)

oldObservation=env.reset()
roundSurvival=0
accumulatedReward=0
for survival in range(5000):		
	#env.render()
	action=chooseAction(epsilon,oldObservation)
	newObservation, reward, done, info = env.step(action)
	accumulatedReward+=reward
	roundSurvival+=reward

	newObservation=convertState(newObservation)
	#updateModel(oldObservation,newObservation,action,reward,alpha)
	oldObservation=newObservation

#	plotData[time]=roundSurvival
print(time, "Round reward and epsilon is:",roundSurvival, epsilon)
print(roundSurvival," out of 5000 tick")


oldObservation=env.reset()
roundSurvival=0
accumulatedReward=0
for survival in range(1000):		
	env.render()
	action=chooseAction(epsilon,oldObservation)
	newObservation, reward, done, info = env.step(action)
	accumulatedReward+=reward
	roundSurvival+=reward

	newObservation=convertState(newObservation)
	#updateModel(oldObservation,newObservation,action,reward,alpha)
	oldObservation=newObservation

#	plotData[time]=roundSurvival
print(time, "Round reward and epsilon is:",roundSurvival, epsilon)



env.close()

#print(thetas)

#print(plotData.var())
#print(plotData.mean())
