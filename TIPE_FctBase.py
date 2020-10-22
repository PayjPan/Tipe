from random import randint, choice, random
import matplotlib.pyplot as plt
import math
import numpy as np

# Taille de la grille par default
X_MAX = 40
Y_MAX = 40

# Géneration de n points aléatoirement dans un rectangle de taille MAX_X, Y_MAX
def generationDePoints(n, x = X_MAX, y = Y_MAX):
    lst_pts = []
    for k in range(n):
        lst_pts += [[randint(0, x), randint(0, y)]]
    return(lst_pts)

# Calcul de la distance entre deux points 
def distance(pt1, pt2):
    x = pt2[0] - pt1[0]
    y = pt2[1] - pt1[1]
    return(math.sqrt(x*x + y*y))

def matriceDistance(lstpoints):
    n = len(lstpoints)
    dist = np.zeros((n,n))
    
    for i in range(n):
        for j in range(n):
            d = distance(lstpoints[i], lstpoints[j])
            dist[i][j], dist[j][i] = d, d
    
    return dist

# Calcul de la distance entre une liste de points (calcul direct)
def distanceChemin(lst_pts):
    # S'il n'y a pas assez de points on retourne une erreur
    if len(lst_pts) < 2:
        return("ERREUR -- chemin d'une liste trop petite")
    
    dst = distance(lst_pts[0], lst_pts[1])
    
    for k in range(2,len(lst_pts)):
        dst += distance(lst_pts[k-1], lst_pts[k])
    
    # On ferme la boucle
    dst += distance(lst_pts[0], lst_pts[-1])
    
    return (dst)

def distanceCheminNew(lstind, matdist):
    # S'il n'y a pas assez de points on retourne une erreur
    if len(lstind) < 2:
        return("ERREUR -- chemin d'une liste trop petite")
    
    dst = matdist[lstind[0]][lstind[1]]
    for k in range(2,len(lstind)):
        
        d = matdist[lstind[k-1]][lstind[k]]
        dst += d
    
    # On ferme la boucle
    dst += matdist[lstind[-1]][lstind[0]]
    
    return (dst)

    
# Affichage des points
def affichePoints(lst_pts, maxX=-1, maxY=-1):
    X = [l[0] for l in lst_pts]
    Y = [l[1] for l in lst_pts]
    plt.plot(X, Y, 'x')
    
    if maxX == -1:
        maxX = max(X)
    if maxY == -1:
        maxY = max(Y)
    
    plt.axis([0, maxX, 0, maxY])
    plt.show()

# Affichage d'un chemin 
# Prends en entrée un chemin
def afficheChemin(lst, maxX=-1, maxY=-1):
    
    lst += [lst[0]]
    X = [l[0] for l in lst]
    Y = [l[1] for l in lst]
    plt.plot(X, Y, '-x', label=distanceChemin(lst))
    
    if maxX == -1:
        maxX = max(X)
    if maxY == -1:
        maxY = max(Y)
        
    plt.axis([0, maxX, 0, maxY])
    plt.legend()
    plt.show()

def afficheLst(lst):    
    plt.plot([i for i in range (len(lst))], lst, '.')
    plt.show()

def afficheLstMultiple(lst):
    couleurs = ['.b', '.g', '.r', '.c', '.m', '.y', '.k']
    for i in range(len(lst)):
        plt.plot([i for i in range (len(lst[i]))], lst[i], couleurs[i%7])
    
    plt.show()

def afficheGraph(g):
    for x in g:
        print (x)
        print ("----------")
        for y in g[x]:
            print (y,':',g[x][y])
        print('\n')
        
# Sauvegarde des chemin
def saveChemin(lstChm, name):
    
    for lst in lstChm :

        lst_pts, taille_chemin = lst[1], lst[0]
        plt.plot([l[0] for l in lst_pts], [l[1] for l in lst_pts], '-x', label=taille_chemin)
        plt.plot(lst_pts[0][0], lst_pts[0][1], 'ro')
        plt.axis([0, X_MAX, 0, Y_MAX])
        plt.legend()
    
    plt.savefig(name)
    plt.clf()
