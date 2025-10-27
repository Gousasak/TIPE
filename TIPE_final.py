
import random
import numpy.random as rd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from numpy import zeros
import numpy as np



def afficher_carte(carte):
    unique_values = list(set(carte.flatten()))
    colors = []    
    if 0 in unique_values:  
        colors.append('white')
    if 1 in unique_values:  
        colors.append('green')
    if 2 in unique_values:  
        colors.append('red')
    if 3 in unique_values:  
        colors.append('black')    
    cmap = ListedColormap(colors)
    plt.matshow(carte, cmap=cmap)
    plt.show()
   	 
    
    
def dico_adja(carte):
    dico = {}
    l = len(carte)
    L = len(carte[0])
    for i in range(0, l):
        for j in range(0, L):
            if carte[i][j]:
                dico[(i, j)] = []
    for i in range(0, l):
        for j in range(0, L - 1):
            if carte[i][j] and carte[i][j + 1]:
                dico[(i, j)].append(((i, j + 1),0))
                dico[(i, j + 1)].append(((i, j),2))
    for i in range(0, l - 1):
        for j in range(0, L):
            if carte[i][j] and carte[i + 1][j]:
                dico[(i, j)].append(((i + 1, j),3))
                dico[(i + 1, j)].append(((i, j),1))
    return dico


def carte_tranchée(l, L, proba1, proba2):   
    x = (l-L) // 2
    A = rd.binomial(1, proba1, (l, x))
    B = rd.binomial(1, proba2, (l, L))
    C = rd.binomial(1, proba1, (l, x))
    return np.concatenate([A, B, C], axis=1)



def propagation(taille, densité1, proba_mort, vent_coef,onoff): #onoff liste d'activation du onoff, ensuite  largeur de la tranchée et probabilité de la tranchée
    if onoff[0]==1  :
        carte=carte_tranchée(taille, onoff[1], densité1, onoff[2])
    else :
        carte=rd.binomial(1, densité1, (taille, taille))
    #afficher_carte(carte) #afficher la carte avant le passage du feu
    dic = dico_adja(carte)
    carte[0,0] = 2
    arbres_en_feu = [(0,0)]  
    while arbres_en_feu :
        nouveaux_en_feu = []
        for (i, j) in arbres_en_feu:
            for voisin, direction in dic.get((i, j), []):
                ni, nj = voisin
                if carte[ni, nj] == 1 and random.random() <= vent_coef[direction]:
                    carte[ni, nj] = 2
                    nouveaux_en_feu.append((ni, nj))
        for (i, j) in arbres_en_feu:
            if random.random() <= proba_mort:
                carte[i, j] = 3
        arbres_en_feu = nouveaux_en_feu + [(i, j) for (i, j) in arbres_en_feu if carte[i, j] == 2]
    return carte



def touche_bordure(carte):
    n=len(carte)
    for i in range(n):
        if carte[i][n-1]==3 :
            return 1
        if carte[n-1][i]==3 :
            return 1
    return 0



def tableau (n, taille, densité1, proba_mort, precision,onoff=[0,1,1]):
    
    taillematrice = int(1//precision)
    T = zeros((taillematrice,taillematrice))
    for i in range(taillematrice):
        for j in range(taillematrice):
            nb = 0
            for k in range(n):
                a = touche_bordure(propagation(taille, densité1, proba_mort,[i*precision,0,0,j*precision],onoff))
                nb += a
            T[i,j] = nb/n
    plt.matshow(T)
    plt.show()
    
    return T





#afficher_carte(propagation(100,0.8,1,[1,0,0,1],[0,10,20]))
tableau(20,20,0.8,1,0.01,[1,20,0.4])



