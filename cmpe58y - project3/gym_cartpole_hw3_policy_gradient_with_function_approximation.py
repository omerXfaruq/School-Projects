#_By FarukOzderim_

import gym
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import sys
env = gym.make("CartPole-v1")


#Global Variables
numberOfEpisodes=100
rollBacksPerEpisode=50
roundsPerRollBack=500

discountedRewardAverageInEpisode=0

rewardsInEpisode=np.zeros(rollBacksPerEpisode*roundsPerRollBack).reshape(rollBacksPerEpisode,roundsPerRollBack)
statesInEpisode=np.zeros(rollBacksPerEpisode*(roundsPerRollBack+1)*5).reshape(rollBacksPerEpisode,roundsPerRollBack+1,5)
actionsInEpisode=np.zeros(rollBacksPerEpisode*roundsPerRollBack).reshape(rollBacksPerEpisode,roundsPerRollBack)
plotEpisodeAverageReward=np.zeros(numberOfEpisodes)


thetas=np.zeros(5)
for j in range(5):
	thetas[j]=np.random.random()

gama=0.99

#Alpha is 0.05
def chooseAlpha(time):
    return 0.05

#Choose action 0 with probability outputOfModel
def chooseAction(oldObservation):
	if np.random.random() > outputOfModel(oldObservation):
		return 0
	else:
		return 1

def activationFunction(x):
	return 1/(1+np.exp(-1*x))

#Gradient of log_phi_, according to bernolli distribution
def gradientOfLogPhi(action,state):
	p=outputOfModel(state)
	return (action*(1-p)*state + (1-action)*-p*state)


#Update Model with policy gradient
def updateModel(rewardsInEpisode,statesInEpisode,actionsInEpisode,discountedRewardAverageInEpisode,alpha):
	discountedRewardsForEachRoundInEpisode=np.zeros(50*500).reshape(50,500)
	rewardsAverage=np.average(rewardsInEpisode,axis=0)

	#Calculate discounted reward for each timestep while using baseline as average reward
	for rollBack in range(rollBacksPerEpisode):
			discountedReward=0
			for round in range(roundsPerRollBack):
				index=roundsPerRollBack-1-round
				discountedReward+=rewardsInEpisode[rollBack][index]-rewardsAverage[index]
				discountedRewardsForEachRoundInEpisode[rollBack][index]=discountedReward
				discountedReward*=gama
		
	thetasUpdate=np.array([0.0,0.0,0.0,0.0,0.0])
	
	#Calculate gradient
	for rollBack in range(rollBacksPerEpisode):
		for round in range(roundsPerRollBack):
			returnSummation=discountedRewardsForEachRoundInEpisode[rollBack][round]
			thetasUpdate+=gradientOfLogPhi(actionsInEpisode[rollBack][round],statesInEpisode[rollBack][round])*returnSummation

	#Expected value for rollBacks in the episode
	thetasUpdate/=rollBacksPerEpisode
	thetasUpdate*=alpha

	#Gradient Descent
	global thetas
	thetas+=thetasUpdate

#Returns output of the model
#1 layer neural network
def outputOfModel(state):
	p=activationFunction(np.dot(thetas,state))
	return p

#Append constant variable to states for bias
def convertState(state):

	state=np.append(state,1)
	return state


#Run the environment
for episode in range(numberOfEpisodes):
	averageRewardInEpisode=0
	averageRewardInRollBack=0
	
	discountedRewardAverageInEpisode=0
	discountedRewardInRollback=0

	alpha=chooseAlpha(episode)

	for rollBack in range(rollBacksPerEpisode):
		averageRewardInRollBack=0
		discountedRewardInRollback=0
		ongoingGamaConstant=1

		oldObservation=env.reset()
		oldObservation=convertState(oldObservation)
		statesInEpisode[rollBack][0]=oldObservation

		for round in range(roundsPerRollBack):		
			
			#env.render()
			action=chooseAction(oldObservation)
			newObservation, reward, done, info = env.step(action)
						
			newObservation=convertState(newObservation)
			
			rewardsInEpisode[rollBack][round]=reward
			statesInEpisode[rollBack][round+1]=newObservation
			actionsInEpisode[rollBack][round]=action

			oldObservation=newObservation
			
			averageRewardInRollBack+=reward
			discountedRewardInRollback+=ongoingGamaConstant*reward
			ongoingGamaConstant*=gama

		discountedRewardAverageInEpisode+=discountedRewardInRollback
		plotEpisodeAverageReward[episode]+=averageRewardInEpisode

		averageRewardInEpisode+=averageRewardInRollBack/rollBacksPerEpisode
	
	plotEpisodeAverageReward[episode]=averageRewardInEpisode
	discountedRewardAverageInEpisode/=rollBacksPerEpisode	
	print("averageRewardInEpisode:",episode,averageRewardInEpisode)
	
	updateModel(rewardsInEpisode,statesInEpisode,actionsInEpisode,discountedRewardAverageInEpisode,alpha)


plt.plot(plotEpisodeAverageReward)
plt.show()
print("Thetas:")
print(thetas)


#Test part after training
print("Now render for 1000 rounds")
oldObservation=env.reset()
oldObservation=convertState(oldObservation)

totalReward=0
for round in range(1000):		
	
	env.render()
	action=chooseAction(oldObservation)
	newObservation, reward, done, info = env.step(action)
	totalReward+=reward	
	newObservation=convertState(newObservation)
	oldObservation=newObservation
	
print("Total Reward In 1000 Rounds:",totalReward)
env.close()
