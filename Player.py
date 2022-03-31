from miscFunctions import color

class Player:
  '''Definition d'un joueur'''
  def __init__(self, num):
    self.num = num

  def play(self, board, joueur):
    print(color(joueur) + " need to play\n")
    ask = 1
    while (ask):
      print("Please enter a value between 0 and " +
              str(board.size_x - 1) + "\n")
      choice = input()
      if (input == ''):
          self.play(board, joueur)
      else:
          choice = int(choice)
      if (choice < 0 or choice >= board.size_x):
        print("Error :wrong input")
      else:
        ask = 0
    return choice
    
  def getColor(self):
    if self.num == 1:
      return "Jaune"
    else:
      return "Rouge"
