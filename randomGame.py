from Board import Board
from PlayerAiRandom import PlayerAIRandom
from dataAnalyse import put_data_in_tab
# from miscFunctions import color

folder = "alea_game_data/"

def full_aleaGame():
  p = Board(7, 6)
  ai = PlayerAIRandom(1)
  ai2 = PlayerAIRandom(-1)
  res = p.run(ai, ai2,1)
  # print( "Nombre de tours : " + str(res[0]))
  # print("Winner : "+ color(res[1]))
  return res

def aleaGame_generator(nb):
    vict1 = []
    vict2 = []
    equal = []
    for i in range(nb):
        res = full_aleaGame()
        if res[1] == 1:
            vict1.append(res[0])
        elif res[1] == -1:
            vict2.append(res[0])
        else:
            equal.append(res[0])
    print(len(vict1))
    print(len(vict2))
    print(len(equal))
    return (vict1,vict2,equal)


def put_file_alea_sim(nb):
    alea_sim = aleaGame_generator(nb)
    f1 = open(folder + "Player1_Win","a")
    f2 = open(folder + "Player2_Win","a")
    f3 = open(folder + "Equal","a")
    for e in alea_sim[0]:
        f1.write(str(e)+"\n")
    for e in alea_sim[1]:
        f2.write(str(e)+"\n")
    for e in alea_sim[2]:
        f3.write(str(e)+"\n")
    f1.close()
    f2.close()
    f3.close()

def count_Equal_Games(nb):
  res = aleaGame_generator(nb)
  return len(res[2]) / nb