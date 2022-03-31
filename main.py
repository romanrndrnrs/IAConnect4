from interactive import interactive
from simulation import simulation

#simulation permet de créer un nouveau set de data 
    #on peu ensuite modeliser ces data avec get_data(dans dataAnalyse)
#interactive permet de lancer une partie avec 2 joueurs aux choix
def main():
    print("Mode :\n1. Simulation\n2. Interactive")
    choice = int(input())
    if (choice == 1):
        simulation()
    else:
        interactive()
main()