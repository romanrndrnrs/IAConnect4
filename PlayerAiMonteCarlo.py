import numpy as np
from Player import Player
from PlayerAiRandom import PlayerAIRandom

class PlayerAIMonteCarlo(Player):
  '''Definition d'un joueur aleatoire avec son numero le définissant'''
  name = "Monte"
  def   __init__(self, p, nbGame = 100):
      self.num = p
      self.nbGame = nbGame

  def play(self, board, joueur):
    reward = np.full(board.size_x, 0)
    copy = board.clone()
    
    for move1 in range(copy.size_x):
      copy.play(move1, joueur)
      reward[move1] = self.simulation(copy, joueur, self.nbGame)
      copy.unplay(move1, joueur)
    return reward.argmax()
    
#plays NB_GAME et retourne le nombre de victoires
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
      win += res == joueur
    return win
        

