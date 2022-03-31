from Board import Board
from PlayerAiRandom import PlayerAIRandom 
from PlayerAiMonteCarlo import PlayerAIMonteCarlo 
from PlayerAiUct import PlayerAiUct
from Player import Player


#play one game with interaction - pick opponent and tab size
def interactive():
    print("Enter a tab size (< 0 for default size):")
    print("Column number (x):")
    column = int(input())
    print("Row number (y):")
    row = int(input())
    if (column <= 0 or row <= 0):
        b = Board()
    else :
        b = Board(column, row)
    print("Tab : "+ str(b.size_x) + " x " + str(b.size_y))
    print("Choose player 1:")
    print("1. Player\n2. Random\n3. monteCarlo\n4.UCT")
    p1 = int(input())
    if p1 == 1:
        p1 = Player(1)
    elif p1 == 2 :
        p1 = PlayerAIRandom(1)
    elif p1 == 3 :
        p1 = PlayerAIMonteCarlo(1)
    elif p1 == 4:
        p1 = PlayerAiUct(1)
    else :
        p1 = PlayerAIRandom(1)
    
    print("Choose player 2:")
    print("1. Player\n2. Random\n3. monteCarlo\n4.UCT")
    p2 = int(input())
    if p2 == 1:
        p2 = Player(-1)
    elif p2 == 2 :
        p2 = PlayerAIRandom(-1)
    elif p2 == 3 :
        p2 = PlayerAIMonteCarlo(-1)
    elif p2 == 4:
        p2 = PlayerAiUct(-1)
    else :
        p2 = PlayerAIRandom(-1)
    res = b.run(p1, p2, 1)
    print((res[0],res[1]))
    print(res[2])