# import random
# import math
from Player import Player
from BoardTree import BoardTree
import numpy as np
from PlayerAiRandom import PlayerAIRandom
import sys
sys.setrecursionlimit(5000)

NBSIM = 5000

class PlayerAiUct(Player):
    '''Definition d'un joueur UCT avec son numero le définissant'''
    name = "UCT"
    def play(self, board, joueur):
        # Each time we create a new root which is the actual board bc
        # we start another MCTS algo at each play
        root = BoardTree(0,None,-1)
        simBoard = board.clone()
        # Children values initialisation:
        for i in range(board.size_x):
            simBoard2 = simBoard.clone()
            simBoard2.play(i,joueur)
            root = self.iterationWithoutSelection(simBoard2,root.player,i,root)
        
        for i in range(NBSIM):
            root = self.iteration(simBoard,root.player,root)
        
        columns = np.array([e for e in range(board.size_x)])
        availableColumns = np.array([e for e in columns if board.data[0][e] == 0 ])
        availableChild = np.array([e for e in root.children if e is not None])
        childUct = np.array([availableChild[e].uctVal for e in range(len(availableChild))])
        select = childUct.argmax()
        return select

    def selectionUct(self,board,joueur,root,current):
        columns = np.array([e for e in range(board.size_x)])
        availableColumns = np.array([e for e in columns if board.data[0][e] == 0 ])
        availableChild = np.array([e for e in root.children if e is not None])
        select = current
        res = {"leaf":root,"board":board,"selection":select}
        
        if (len(availableChild) == 7):
            childUct = np.array([availableChild[e].uctVal for e in range(len(availableChild))])
            select = childUct.argmax()
            boardCopy = board.clone()
            boardCopy.play(select,joueur)
            if(joueur == 1):
                joueur = -1
            else:
                joueur = 1
            res = self.selectionUct(boardCopy,joueur,availableChild[select],select)
        return res

    def expansion(self,board,joueur,selection,leaf):
        if(joueur == 1):
            joueur = -1
        else:
            joueur = 1
        columns = np.array([e for e in range(board.size_x)])
        availableColumns = np.array([e for e in columns if board.data[0][e] == 0 ])
        availableChild = np.array([list(leaf.children).index(e) for e in leaf.children if e is None])

        selection = np.random.choice(availableChild)
        leaf.children[selection] = BoardTree(0,leaf,selection)
        board.play(selection,joueur)
        leaf = leaf.children[selection]
        return {"board":board,"leaf":leaf}
    
    def simulation(self, board, joueur, games):
        win = 0
        p1 = PlayerAIRandom(joueur)
        if (joueur == 1):
            p2 = PlayerAIRandom(-1)
        else :
            p2 = PlayerAIRandom(1)
        for i in range(games):
            copy = board.clone()
            res = copy.run(p2, p1, 0)[1]
            if(res == joueur):
                win = 1
            else:
                win = 0
        return win

    def backPropagation(self,board,joueur,gain,leaf):
        actual = leaf
        while(actual): 
            actual.addGain(gain)
            # Add visit count for the current node
            actual.addVisitCount()
            actual.updateChildUct()
            if(actual.parent is not None):
                actual = actual.parent
                gain = -gain
            else:
                break
        disp = [list(actual.children).index(e) for e in actual.children if e is not None]     
        return actual     

    def iterationWithoutSelection(self,board,joueur,selection,leaf):
        expansionRes = self.expansion(board,joueur,selection,leaf)
        board = expansionRes["board"]
        leaf = expansionRes["leaf"]
        if(joueur == 1):
            simPlayer = -1
        else:
            simPlayer = 1
        gain = self.simulation(board,simPlayer,1)
        gain = -gain
        
        root = self.backPropagation(board,joueur,gain,leaf)
        return root

    def iteration(self, board,joueur,root):
        selection = self.selectionUct(board,joueur,root,None)
        root = self.iterationWithoutSelection(selection["board"],selection["leaf"].player,selection["selection"],selection["leaf"])
        return root
