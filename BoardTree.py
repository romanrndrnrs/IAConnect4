import numpy as np
from math import sqrt, log10

class BoardTree:
    def __init__(self,gain,parent,num):
        self.num = num
        self.gain = gain
        self.visitCount = 0
        self.uctVal = 0.0
        self.children = np.array([None,None,None,None,None,None,None])
        self.parent = parent
        if self.parent is None:
            self.player = 1
        else:
            if(self.parent.player == 1):
                self.player = -1
            else:
                self.player = 1
        #initialise uctVals (value 0 is non attributed)
        #self.uctChildrenVals = np.zeros(10)

    def addGain(self,gain):
        self.gain += gain

    def addVisitCount(self):
        self.visitCount += 1

    def setUctVal(self,uct):
        self.uctVal = uct
    
    def updateChildUct(self):
        for i in range(len(self.children)):
            if(self.children[i] is not None):
                if(self.children[i].visitCount != 0):
                    self.children[i].uctVal = self.children[i].gain / self.children[i].visitCount + sqrt(2*log10(self.visitCount)/self.children[i].visitCount)
            
    


