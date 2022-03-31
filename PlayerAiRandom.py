import random
import math
from Player import Player
# from miscFunctions import color
		
class PlayerAIRandom(Player):
    '''Definition d'un joueur aleatoire avec son numero le définissant'''
    name="Random"
    def play(self, board, joueur):
        choice = math.floor(random.random() * board.size_x)
        # print(color(joueur) + " played")
        return choice

