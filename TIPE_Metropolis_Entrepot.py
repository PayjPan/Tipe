import copy
import numpy as np
import math
from random import randint, choice, random
import TIPE_DstEntrepot as dstentrepot
import TIPE_FctBase as fctB
import TIPE_EntrepotClasse as ent
from copy import deepcopy


# Calcul l'énergie du système (ici cela correspond à la distance totale)
def energieChemin(chm, distance):
    return(dstentrepot.distanceChemin(chm, distance))
    
def cheminProche(chmactuel):
    """
    Genere un chemin proche de l'actuel en echangeant deux points
    """
    newchm = deepcopy(chmactuel)
    l = randint(2, len(chmactuel) - 1)
    i = randint(0, len(chmactuel) - l)

    newchm[i: (i + l)] = reversed(newchm[i: (i + l)])
    
    return newchm

def accepterChemin(enrgactuelle, enrgnew, alpha):
    """
    Détermine la probalilité que l'on doivent changer les chemins
    Si la nouvelle distance est plus basse on remplace tt le temps
    Sinon on la remplace qu'avec une certaine probabilité
    """
    if enrgnew < enrgactuelle:
        return 1
    else:
        proba = np.exp((enrgactuelle - enrgnew)*alpha)
        tirage = random()
        
        return tirage < proba

def rechercheMetropolis(entrepot, lstobjets, tmpdepart=100, tmpfinale = 0.00000001, refroidissement = 0.0005, maxfreeze = 1000000):
        
    chmactuel = [i for i in range(len(lstobjets))]
    distance, chmentreobjets = dstentrepot.distanceEntreObjets(entrepot, lstobjets)

    enrgactuelle = energieChemin(chmactuel, distance)
    print('Distance de départ: %.3f' % enrgactuelle)

    chmbest = chmactuel
    enrgbest = enrgactuelle
    
    hist = []
    
    lstenrg = []
    lsttmp = []
    
    tmp = tmpdepart
    freeze = 0
    
    while tmp > tmpfinale and freeze < maxfreeze:
    
        chmnew = cheminProche(chmactuel)
        enrgnew = energieChemin(chmnew, distance)
        
        if enrgnew > enrgactuelle:
            freeze += 1
        
        l = accepterChemin(enrgactuelle, enrgnew, 1/(tmp))
        
        if l:
            chmactuel = chmnew
            enrgactuelle = enrgnew
            
            hist += [chmnew]
    
        # On sauvgarde la meilleure solution
        if enrgactuelle < enrgbest:
            chmbest = chmactuel
            enrgbest = enrgactuelle
            
            freeze = 0
            
        tmp *= 1 - refroidissement
        
        lsttmp.append(tmp)
        lstenrg.append(enrgactuelle)

    
    print('Distance finale: %.3f' % enrgbest)

    # On effectue une rotation au chemin trouvé pour avoir l'entrée en premier
    i = 0
    while chmbest[i] != 0:
        i += 1
    chmbest = chmbest[i:]+chmbest[:i]
    
    # On récupère le chemin finale en explicitant les noeuds par lesquels on doit passer
    chmnoeuds = [(entrepot.entree[0], entrepot.entree[1])]
    for i in range(len(chmbest)-1):
        chmnoeuds += chmentreobjets[chmbest[i+1]][chmbest[i]]
    
    chmnoeuds += chmentreobjets[chmbest[0]][chmbest[-1]]
        
    # On traduit le chemin des objets en une liste de coordonnées pour réutilisé l'agorithme
    chmcoordonnées = []
    for i in chmbest:
        chmcoordonnées += [lstobjets[i]]   
    
    return (enrgbest, chmbest, chmnoeuds, chmcoordonnées, lstenrg)


