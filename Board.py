import numpy as np
# from dataAnalyse import *
CHOICE = False
# from miscFunctions import color

class Board:
  '''Definition d'un plateau de taille size_x * size_y'''
  #initialise size and board
  def __init__(self, size_x=7, size_y=6):
    self.size_x = size_x
    self.size_y = size_y
    self.data = np.full((self.size_y, self.size_x), 0)
    
  #reset all values of board to 0
  def reset(self):
    self.data = np.full((self.size_y, self.size_x), 0)

  #return clone de self.Board
  def clone(self):
    copy = Board(self.size_x, self.size_y)
    copy.data = np.copy(self.data)
    return copy   

  #return 1 or -1 if a player won 0 else
  def has_won(self):
    for x in range(self.size_x):
      for y in range(self.size_y):
        cur = self.data[y][x]
        dist = 0
        ver = True
        hor = True
        diag1 = True
        diag2 = True
        if (cur != 0):
          while (dist < 4 and (ver or hor or diag1 or diag2)):
            if (ver and (y + dist >= self.size_y or self.data[y + dist][x] != cur)):
              ver = False
            if (hor and (x + dist >= self.size_x or self.data[y][x + dist] != cur)):
              hor = False
            if (diag1 and (y + dist >= self.size_y or x + dist >= self.size_x or self.data[y + dist][x + dist] != cur)):
                diag1 = False
            if (diag2 and (y - dist < 0 or x + dist >= self.size_x or self.data[y - dist][x + dist] != cur)):
              diag2 = False
            if (dist >= 3 and (ver or hor or diag1 or diag2)):
              return cur
            dist += 1
    return 0
   
   #si possible met joueur.num in row x et retourne 0
  def play(self, x, joueur):
    if x < 0 or x >= self.size_x:
      # print("You can't play outside the board!")
      return 1
    for y in range(self.size_y - 1, -1, -1):
      if (self.data[y][x] == 0):
        self.data[y][x] = joueur
        return 0
    # print("The column %d is full!" % (x))
    return 1
        
  def unplay(self, x, joueur):
      if x < 0 or x >= self.size_x:
        # print("Outside the board")
        return 1
      for y in range(self.size_y - 1, -1, -1):
        if (self.data[y][x] != 0):
          self.data[y][x] = 0
          return 0
      # print("Empty column")
      return 1
  
  #return true if board is full or a player won
  def is_finished(self):
    winner = self.has_won()
    if winner != 0 or 0 not in self.data:
      return True
    return False

  #si choice = True permet de rejouer une partie
  def choice(self, p1, p2):
    print("Do you want to play again?")
    print("yes / no")
    k = input()
    if (k.lower() == "yes" or k == "y"):
      self.reset()
      self.run(p1, p2)
    else:
      print("See you again!")

  #si random joue un coup impossible trop de fois joue dans la 1ere case dispo
  def find_empty(self):
    for i in range(self.size_x):
      if (self.data[0][i] == 0):
        return i
    return -1

  #lance la partie et s'arrete uniquement lorsqu'elle se fini
  def run(self, p1, p2, mode):
    p = [p1, p2]
    which = 0
    cpt = 0
    while (self.is_finished() == False):
      if (mode == 1):
        print(self.data)
      cpt +=1
      max_try = 0
      while (self.play(p[which].play(self, p[which].num), p[which].num)):
        max_try += 1
        if (max_try >= 5):
          empty_spot = self.find_empty()
          if (empty_spot == -1):
            break
          self.play(empty_spot, p[which].num)
          max_try = 0
      which = (which + 1) % 2
      #print(self.data)
    #  print("Game over")
    #  print(self.has_won())
    if (CHOICE == True):
      self.choice(p1, p2)
    return (cpt, self.has_won(),self.data)