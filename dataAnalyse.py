import matplotlib.pyplot as plt
# from monteGame import aleaGame_generator

folder = "Uct_Uct_data/"
fd1 = "UCT1_Win"
fd2 = "UCT2_Win"
fd3 = "UCTUCT_Equal"

#met les data contenu dans f dans tab
def put_data_in_tab(f):
	tab = []
	e = ""
	e = f.readline()
	while(e):
		efloat = float(e)
		tab.append(int(efloat))
		e = f.readline()
	return tab

#recupere data de f1, f2 et f3 et crée un histogramme
def get_data():
    f1 = open(folder + fd1, "r")
    f2 = open(folder + fd2, "r")
    f3 = open(folder + fd3, "r")
    tabP1 = put_data_in_tab(f1)
    tabP2 = put_data_in_tab(f2)
    tabP3 = put_data_in_tab(f3)
    f1.close()
    f2.close()
    f3.close()
    histoWin(tabP1, tabP2, tabP3)

#cree un histogramme a partir de 3 tab
def histoWin(win1, win2, win3):
    plt.hist(win1, bins=range(max(win1)), label =fd1)
    plt.hist(win2, bins=range(max(win2)), label =fd2)
    plt.hist(win3,bins=range(max(win3)), label =fd3)
    plt.xlabel("Nb of rounds")
    plt.ylabel("Nb of games")
    plt.legend()
    plt.grid(lw = 0.25)
    plt.title('Win and nb of rounds distribution')
    plt.savefig(folder + 'Win_distrib.png')
    plt.show()


get_data()

# def count_Equal_Games(nb):
#   res = aleaGame_generator(nb)
#   return len(res[2]) / nb