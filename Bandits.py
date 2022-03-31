import numpy as np
import random
from math import floor
from dataAnalyse import put_data_in_tab
import matplotlib.pyplot as plt

NBIT = 1000
NBLEVERS = 50
EXPLOPCT = 0.01
folder = "Bandit_data/"

class Bandits:
    #static Random levers bernoulli parameter
    leversRand = np.random.sample(size = 10)
    #static epsilon
    eps = 0.4
    
    def __init__(self,nbLevers,nbIt,muVals = "random",eps=0.4,algo="baseline"):
        self.nbLevers = nbLevers
        self.nbIt = nbIt
        if((type(muVals).__module__ == np.__name__) or type(muVals) == list):
            self.muVals = np.array(muVals)
        else:
            self.muVals = np.random.sample(size = nbLevers)
            print(self.muVals)
        self.eps = eps
        self.t = 0
        algo = algo.lower()
        if(algo == "greedy" or algo == "greedyeps" or algo == "ucb" or algo == "optimalreward"):
            self.algo = algo
        else:
            self.algo = "baseline"
        #count the reward -> useful to calculate the regret for the loss fonction
        self.reward = 0
    
    def binaryReward(self,levers,action):
        p = random.random()
        #print("Action mu is "+str(levers[action]))
        #print("Result is "+str(p))
        if(p<levers[action]):
            return 1
        else:
            return 0
            
    def baseline(self,meanLeverRewards,nbOfLeverUse):
        a = floor(random.random()*self.nbLevers)
        reward = self.binaryReward(self.muVals,a)
        nbOfLeverUse[a] += 1
        meanLeverRewards[a] = (meanLeverRewards[a]*(nbOfLeverUse[a]-1) + reward) / nbOfLeverUse[a]
        return {"action":a,"reward":reward,"meanLeverRewards":meanLeverRewards,"nbOfLeverUse":nbOfLeverUse}
    

    def greedy(self,meanLeverRewards, nbOfLeverUse):
        a = meanLeverRewards.argmax()
        reward = self.binaryReward(self.muVals,a)
        nbOfLeverUse[a] += 1
        meanLeverRewards[a] = (meanLeverRewards[a]*(nbOfLeverUse[a]-1) + reward) / nbOfLeverUse[a]
        return {"action":a,"reward":reward,"meanLeverRewards":meanLeverRewards,"nbOfLeverUse":nbOfLeverUse}
    
    def greedyEps(self,meanLeverRewards, nbOfLeverUse):
        p = random.random()
        if(p < self.eps):
            return self.baseline(meanLeverRewards, nbOfLeverUse)
        else:
            return self.greedy(meanLeverRewards, nbOfLeverUse)

    def ucb(self,meanLeverRewards, nbOfLeverUse):
        res = meanLeverRewards + np.sqrt(2*np.log10(self.t)/nbOfLeverUse)
        a = np.argmax(res)
        reward = self.binaryReward(self.muVals,a)
        nbOfLeverUse[a] += 1
        meanLeverRewards[a] = (meanLeverRewards[a]*(nbOfLeverUse[a]-1) + reward) / nbOfLeverUse[a]
        return {"action":a,"reward":reward,"meanLeverRewards":meanLeverRewards,"nbOfLeverUse":nbOfLeverUse}
    
    def optimalReward(self,meanLeverRewards,nbOfLeverUse):
        a = self.muVals.argmax()
        reward = self.binaryReward(self.muVals,a)
        nbOfLeverUse[a] += 1
        meanLeverRewards[a] = (meanLeverRewards[a]*(nbOfLeverUse[a]-1) + reward) / nbOfLeverUse[a]
        return {"action":a,"reward":reward,"meanLeverRewards":meanLeverRewards,"nbOfLeverUse":nbOfLeverUse}

    

    def pullLever(self,meanLeverRewards,nbOfLeverUse):
        self.t += 1
        if(self.algo == "baseline"):
            return self.baseline(meanLeverRewards,nbOfLeverUse)
        elif(self.algo == "greedy"):
            return self.greedy(meanLeverRewards,nbOfLeverUse)
        elif(self.algo == "greedyeps"):
            return self.greedyEps(meanLeverRewards,nbOfLeverUse)
        elif(self.algo == "ucb"):
            return self.ucb(meanLeverRewards,nbOfLeverUse)
        elif(self.algo == "optimalreward"):
            return self.optimalReward(meanLeverRewards,nbOfLeverUse)

    


    def run(self):
        meanLeverRewards = np.zeros(len(self.muVals))
        #Start count at 1 to avoid divide by 0
        nbOfLeverUse = np.ones(len(self.muVals))
        regretTab = []
        rewardTab = []
        # If it is a greedy algorithm, we explore first
        if "greedy" in self.algo:
            algoName = self.algo
            # 20% of iterations are set for exploration
            nbItExplo = floor(self.nbIt*EXPLOPCT)
            # For exploration we are using the baseline
            self.algo = "baseline"
            for i in range(nbItExplo):
                pullRes = self.pullLever(meanLeverRewards,nbOfLeverUse)
                meanLeverRewards = pullRes["meanLeverRewards"]
                nbOfLeverUse = pullRes["nbOfLeverUse"]
                self.reward += pullRes["reward"]
                rewardTab.append(self.reward)
                #regretTab.append(self.optimalReward() - self.reward)
            # Actualize the nb of Iterations needed for the rest of the algorithm
            self.nbIt = self.nbIt - nbItExplo
            # We are using the Greedy or EpsGreedy algo for the rest of iterations not the baseline
            self.algo = algoName
        # Iterations for the different algorithms
        for i in range(self.nbIt):
            pullRes = self.pullLever(meanLeverRewards,nbOfLeverUse)
            meanLeverRewards = pullRes["meanLeverRewards"]
            nbOfLeverUse = pullRes["nbOfLeverUse"]
            self.reward += pullRes["reward"]
            rewardTab.append(self.reward)
            #print(self.reward)
            #regretTab.append(self.optimalReward() - self.reward)
        #regret = self.optimalReward()-self.reward
        regret = 0
        #accuracy = (self.reward / self.optimalReward())
        accuracy = 0
        return {"reward":self.reward,"regret":regret,"accuracy":accuracy,"regretTab":regretTab,"rewardTab":rewardTab}
    
def writeInFile():
    fBaseline = open(folder + "Baseline1.txt","w")
    fGreedy = open(folder + "Greedy1.txt","w")
    fGreedyEps = open(folder + "GreedyEps1.txt","w")
    fUcb = open(folder + "UCB1.txt","w")
    fOptimal = open(folder + "Optimal1.txt","w")
    greedy = []
    greedyEps = []
    ucb = []
    optimal = []
    #create a linspace
    #levers = np.linspace(0.0,1.0,NBLEVERS,endpoint = 0)
    #shuffle values
    #np.random.shuffle(levers)
    levers = np.random.sample(size = NBLEVERS)
    print("Starting")
    a = Bandits(NBLEVERS,NBIT,algo="baseline",muVals = levers)
    print("Baseline")
    res = a.run()
    baseline = res["rewardTab"]
    a = Bandits(NBLEVERS,NBIT,algo="greedy",muVals = levers)
    print("Greedy")
    res = a.run()
    greedy = res["rewardTab"]
    a = Bandits(NBLEVERS,NBIT,algo="greedyEps",muVals = levers)
    print("GreedyEps")
    res = a.run()
    greedyEps = res["rewardTab"]
    a = Bandits(NBLEVERS,NBIT,algo="ucb",muVals = levers)
    print("UCB")
    res = a.run()
    ucb = res["rewardTab"]
    a = Bandits(NBLEVERS,NBIT,algo="optimalReward",muVals = levers)
    print("Optimal")
    res = a.run()
    optimal = res["rewardTab"]

    for i in range(NBIT):
        fBaseline.write(str(baseline[i]) + "\n")
        fGreedy.write(str(greedy[i]) + "\n")
        fGreedyEps.write(str(greedyEps[i]) + "\n")
        fUcb.write(str(ucb[i]) + "\n")
        fOptimal.write(str(optimal[i])+ "\n")
    print("Written")

    fBaseline.close()
    fGreedy.close()
    fGreedyEps.close()
    fUcb.close()
    fOptimal.close()

writeInFile()

f1 = open(folder + "Baseline1.txt","r")
f2 = open(folder + "Greedy1.txt","r")
f3 = open(folder + "GreedyEps1.txt","r")
f4 = open(folder + "UCB1.txt","r")
f5 = open(folder + "Optimal1.txt","r")
tabP1 = put_data_in_tab(f1)
tabP2 = put_data_in_tab(f2)
tabP3 = put_data_in_tab(f3)
tabP4 = put_data_in_tab(f4)
tabP5 = put_data_in_tab(f5)
x = np.linspace(0,NBIT,NBIT)
f1.close()
f2.close()
f3.close()
f4.close()
f5.close()
tabArray1 = np.array(tabP1)
tabArray2 = np.array(tabP2)
tabArray3 = np.array(tabP3)
tabArray4 = np.array(tabP4)
tabArray5 = np.array(tabP5)
tabArray1 = tabArray5 - tabArray1
tabArray2 = tabArray5 - tabArray2
tabArray3 = tabArray5 - tabArray3
tabArray4 = tabArray5 - tabArray4

plt.plot(x,tabArray1, label ="BaselineRegret")
plt.plot(x,tabArray2, label ="GreedyRegret")
plt.plot(x,tabArray3, label ="GreedyEpsRegret")
plt.plot(x,tabArray4, label ="UCBRegret")
#plt.plot(x,tabArray5, label ="OptimalGain")
plt.xlabel("Time")
plt.ylabel("Regret")
plt.legend()
plt.grid(lw = 0.25)
plt.title('Regret as a function of time')
plt.savefig(folder + 'Regret.png')
plt.show()
'''

#create a linspace
levers = np.linspace(0.0,1.0,100,endpoint = 0)
#shuffle values
np.random.shuffle(levers)
a = Bandits(NBLEVERS,1000,algo="baseline",muVals = levers)
loss = a.run()
print(loss)
print(a.muVals)
'''