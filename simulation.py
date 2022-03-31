from Board import Board
from PlayerAiRandom import PlayerAIRandom
from PlayerAiUct import PlayerAiUct
from PlayerAiMonteCarlo import PlayerAIMonteCarlo


#lance une simulation avec parametres choisis 
def simulation():
    x = 7
    y = 6

    print("Choose simulation type:")
    print("1. Random VS Random\n" +
        "2. Random VS MonteCarlo\n"+
        "3. MonteCarlo VS MonteCarlo\n"+
        "4. Random VS Uct\n"+
        "5. MonteCarlo VS Uct\n"+
        "6. Uct VS Uct\n")
    choice = int(input())
    if (choice == 2):
        p1 = PlayerAIRandom(1)
        print("Choose Monte Carlo nb simulation")
        lvl = int(input())
        p2 = PlayerAIMonteCarlo(-1, lvl)
        folder = "Random_Monte_data/"
        print("Switch order?\n1. Yes\n2. No\n")
        if (int(input()) == 1):
            p1, p2 = p2, p1
            p1.num, p2.num = p2.num, p1.num
    elif (choice == 3):
        print("Choose Monte Carlo 1 nb simulation")
        lvl = int(input())
        p1 = PlayerAIMonteCarlo(1, lvl)
        print("Choose Monte Carlo 2 nb simulation")
        lvl = int(input())
        p2 = PlayerAIMonteCarlo(-1, lvl)
        folder = "Monte_data/"
    elif (choice == 4):
        p1 = PlayerAIRandom(1)
        p2 = PlayerAiUct(-1)
        folder = "Random_Uct_data/"
        print("Switch order?\n1. Yes\n2. No\n")
        if (int(input()) == 1):
            p1, p2 = p2, p1
            p1.num, p2.num = p2.num, p1.num
    elif (choice == 5):
        print("Choose Monte Carlo nb simulation")
        lvl = int(input())
        p1 = PlayerAIMonteCarlo(1, lvl)
        p2 = PlayerAiUct(-1)
        folder = "Monte_Uct_data/"
        print("Switch order?\n1. Yes\n2. No\n")
        if (int(input()) == 1):
            p1, p2 = p2, p1
            p1.num, p2.num = p2.num, p1.num
    elif (choice == 6):
        p1 = PlayerAiUct(1)
        p2 = PlayerAiUct(-1)
        folder = "Uct_Uct_data/"
    else :
        p1 = PlayerAIRandom(1)
        p2 = PlayerAIRandom(-1)
        folder = "Random_data/"
    
    b = Board(x, y)
    nb_play = int(input("Number of simulations :"))
    
    f1 = open(folder + p1.name + "1_Win","a")
    f2 = open(folder + p2.name + "2_Win","a")
    f3 = open(folder + p1.name + p2.name + "_Equal","a")
    
    for i in range(nb_play):
        res = b.run(p1, p2, 0)
        if (res[1] == 1):
            f1.write(str(res[0])+"\n")
        elif (res[1] == -1):
            f2.write(str(res[0])+"\n")
        elif (res[1] == 0):
            f3.write(str(res[0])+"\n")
        b.reset()
    f1.close()
    f2.close()
    f3.close()