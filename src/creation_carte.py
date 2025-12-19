import numpy.random as rd
import numpy as np

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
