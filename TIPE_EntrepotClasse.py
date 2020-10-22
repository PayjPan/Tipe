import numpy as np
from copy import deepcopy
from random import randint, choice, random
import time
import matplotlib.pyplot as plt
import sys

class Entrepot:
        
    def __init__(self, nbcases=5, nbcolonnes=3, nblignes=2, entree=[-1,-1]):
        
        self.nbcases = nbcases
        self.nbcolonnes= nbcolonnes
        self.nblignes = nblignes
        
        # Initalisation de l'entrée si elle n'a pas été définie
        '''
            On la place par défaut à droite le plus au centre possible en face d'un allée
        ''' 
        if entree == [-1, -1]:
            x = (nblignes//2) * (nbcases+1)
            y = 0
            entree = [x,y]
        
        self.entree = entree
        
        self.tableau = self.generationEntrepotVide()
  
        
    def generationEntrepotVide(self):
        X = self.nbcases * self.nblignes + self.nblignes + 1
        Y = self.nbcolonnes * 2 + self.nbcolonnes + 1
        entrepot = np.full((X, Y),'-2', dtype=int)
        
        
        x,y = 1, 0
        while x < X-1 :
            while y < Y-1:
                y += 1
                entrepot[x:x+self.nbcases, y] = -1
                y += 1
                entrepot[x:x+self.nbcases, y] = -1
                y += 1
            y = 0
            x += self.nbcases + 1
                
        return entrepot
        
    def caseAccecibleLaPlusProche(self,pt):
        if self.tableau[pt[0], pt[1]] == -2:
            return pt
        if self.tableau[pt[0], pt[1]-1] == -2:
            return [pt[0], pt[1]-1]
        if self.tableau[pt[0], pt[1]+1] == -2:
            return [pt[0], pt[1]+1]
    
    def adjacentVide(self):
        '''
        Créé un dictionaire des noeuds d'intesections initialisé à des distances infinie de la forme :
        
            {((x,y), k): {((x',y'), k): inf | pour toute les intersections} | pour toutes les intersections}
        
        (x,y) : coordonée de l'intersection
        k = 0 si intersection, n si objet numéro n
        '''
        
        adjacentvide = {}
        
        for i in range (0, self.nblignes+1):
            for j in range (0, self.nbcolonnes+1):
                
                # Coordonnées du noeuds intesction
                x = i*(self.nbcases+1)
                y = j*3
                
                adjacentvide[((x,y), -1)] = float('inf')
        
        return adjacentvide
        
    def graphVide(self):
        graphentr = {}
        
        nbcases = self.nbcases
        nblignes = self.nblignes
        nbcolonnes = self.nbcolonnes
        
        adjacents = self.adjacentVide()
        
        for i in range (0, nblignes+1):
            for j in range(0, nbcolonnes+1):
                
                newadj = deepcopy(adjacents)
                
                x = i*(self.nbcases+1)
                y = j*3
                
                # Pour revenir sur soi = distance nulle
                newadj[((x,y),-1)] = 0
                
                # Les coordonées des 2 possibles noeuds intersection (les noeuds verticaux dépendent de la présence ou non d'un objet)
                left = ((x,y-3),-1)
                right = ((x,y+3),-1)
                
                if left in newadj:
                    newadj[left] = 2        # Le nombre de case pour traverser une étagère en largeure
                if right in newadj:
                    newadj[right] = 2
                
                graphentr[(x,y),-1]= newadj
                
        return graphentr
    
    def generationListeObjet(self, nbobjet):
        nbrestant = nbobjet
        lst = []
        x, y = np.shape(self.tableau)
        
        while nbrestant > 0:
            ptpotentiel = [randint(0, x-1), randint(0, y-1)]
            if self.tableau[ptpotentiel[0], ptpotentiel[1]] != -2 and not(ptpotentiel in lst):
                lst += [ptpotentiel]
                nbrestant -= 1
        
        return [self.entree]+lst    # l'entrée fait toujours partie des noeuds à rencontrer
    
    def afficher(self, lstobj=[], chm=[]):
        tbl = deepcopy(self.tableau)
        
        # On place les objets
        i = 0
        for o in lstobj:
            tbl[o[0]][o[1]] = i
            i += 1

        # On place le chemin s'il est donné
        if chm != []:
            for i in range(len(chm)-1):
                self.remplissageChemin(tbl, chm[i], chm[i+1])
        
        tbl[self.entree[0]][self.entree[1]] = 0
        
        shape = np.shape(self.tableau)
        for x in range(shape[0]):
            for y in range(shape[1]):
                
                symboles = { 0: '◉',
                            -1: '□',
                            -2: ' ',
                            -3: '→',
                            -4: '↓',
                            -5: '←',
                            -6: '↑',
                            -7: '⇄',
                            -8: '⇅'}
                
                if tbl[x][y] > 0:
                    print('■', end='')
                    #print(tbl[x][y], end='')
                else:
                    print(symboles[tbl[x][y]], end='')
            print('')
    
    def afficherplt(self, lstobj=[], chm=[]):
        # fonctions d'affichage

        tbl = deepcopy(self.tableau)
        
        fig, ax = plt.subplots()
        plt.set_cmap('gray')
        plt.axis([0, len(tbl[0]), 0, len(tbl)])
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.invert_yaxis()
        
        def up(x, y):
            up = plt.arrow(0.5+x, 0.1+y, 0, 0.8, width = 0.1, length_includes_head=True, color='k')
            
        def down(x, y):
            down = plt.arrow(0.5+x, 0.9+y, 0, -0.8, width = 0.1, length_includes_head=True, color='k')
        
        def right(x, y):
            right = plt.arrow(0.1+x, 0.5+y, 0.8, 0, width = 0.1, length_includes_head=True, color='k')
        
        def left(x, y):
            left = plt.arrow(0.9+x, 0.5+y, -0.8, 0, width = 0.1, length_includes_head=True, color='k')
        
        def updown(x, y):
            up = plt.arrow(0.25+x, 0.1+y, 0, 0.8, width = 0.1, length_includes_head=True, color='k') 
            down = plt.arrow(0.75+x, 0.9+y, 0, -0.8, width = 0.1, length_includes_head=True, color='k')
        
        def rightleft(x, y):
            right = plt.arrow(0.1+x, 0.75+y, 0.8, 0, width = 0.1, length_includes_head=True, color='k')
            left = plt.arrow(0.9+x, 0.25+y, -0.8, 0, width = 0.1, length_includes_head=True, color='k')
        
        def box(x,y):
            box = plt.Rectangle([x,y], 1, 1, linewidth=1, color="k", fill= False)
            ax.add_patch(box)        
        
        def objet(x,y, num):
            box = plt.Rectangle([x,y], 1, 1, color="silver", fill=True)
            ax.add_patch(box)
            ax.annotate(str(num), [x+0.5,y+0.5], ha='center', va='center')

        
        def entree(x,y):
            ent = plt.Circle([x+0.5,y+0.5], 0.4, color='k')
            ax.add_patch(ent)

        # On place les objets
        i = 0
        for o in lstobj:
            tbl[o[0]][o[1]] = i
            i += 1

        # On place le chemin s'il est donné
        if chm != []:
            for i in range(len(chm)-1):
                self.remplissageChemin(tbl, chm[i], chm[i+1])
        
        tbl[self.entree[0]][self.entree[1]] = 0
        
        shape = np.shape(self.tableau)
        for x in range(shape[0]):
            for y in range(shape[1]):
                
                if tbl[x][y] > 0:
                    objet(y,x, tbl[x][y])
                    #print(tbl[x][y], end='')
                elif tbl[x][y] == -1:
                    box(y,x)
                elif tbl[x][y] == 0:
                    entree(y,x)
                elif tbl[x][y] == -3:
                    right(y,x)
                elif tbl[x][y] == -4:
                    up(y,x)
                elif tbl[x][y] == -5:
                    left(y,x)
                elif tbl[x][y] == -6:
                    down(y,x)
                elif tbl[x][y] == -7:
                    rightleft(y,x)
                elif tbl[x][y] == -8:
                    updown(y,x)
                
        plt.show()
        
    def remplissageChemin(self, tbl, pt1, pt2):
        x1, y1 = pt1[0], pt1[1]
        x2, y2 = pt2[0], pt2[1]
        
        '''
        Légende :
            i > 0 --> Objets : ■
            0 --> l'entrée : ◉
            -1 --> box vide : □
            -2 --> chemin vide : _
            -3 --> fleche droite : →
            -4 --> fleche bas : ↓
            -5 --> flèce gauche : ←
            -6 --> fleche haut : ↑
            -7 --> fleche droite-gauche : ⇄
            -8 --> fleche haut-bas : ⇅
        '''
        
        if x1 == x2:
            if y1 < y2:
                while y1 <= y2:
                    if tbl[x1][y1] == -2:
                        tbl[x1][y1] = -3
                    if tbl[x1][y1] == -5:
                        tbl[x1][y1] = -7
                    y1 += 1
            else:
                while y2 <= y1:
                    if tbl[x1][y1] == -2:
                        tbl[x1][y1] = -5
                    if tbl[x1][y1] == -3:
                        tbl[x1][y1] = -7
                    y1 -= 1
        else:
            if x1 < x2:
                while x1 <= x2:
                    if tbl[x1][y1] == -2:
                        tbl[x1][y1] = -4
                    if tbl[x1][y1] == -6:
                        tbl[x1][y1] = -8
                    x1 += 1
            else:
                while x2 <= x1:
                    if tbl[x1][y1] == -2:
                        tbl[x1][y1] = -6
                    if tbl[x1][y1] == -4:
                        tbl[x1][y1] = -8
                    x1 -= 1
    
    def afficherpap(self, lstobj=[], chm=[]):
        tbl = deepcopy(self.tableau)
        
        stop = False
        
        # On place les objets
        i = 0
        for o in lstobj:
            tbl[o[0]][o[1]] = i
            i += 1

        # On affiche le chemin pas à pas
        for i in range(len(chm)-1):
                    
            tbltmp = deepcopy(tbl)
            
            self.remplissageChemin(tbltmp, chm[i], chm[i+1])
                
            tbltmp[self.entree[0]][self.entree[1]] = 0
            
            shape = np.shape(self.tableau)
            
            str = ''
            
            for x in range(shape[0]):
                for y in range(shape[1]):
                    
                    symboles = { 0: '◉',
                                -1: '□',
                                -2: ' ',
                                -3: '→',
                                -4: '↓',
                                -5: '←',
                                -6: '↑',
                                -7: '⇄',
                                -8: '⇅'}
                    
                    if tbltmp[x][y] > 0:
                        str += '■'
                    else:
                        str += symboles[tbltmp[x][y]]
                str += '\n'
            
            sys.stdout.write(str)
            
            time.sleep(0.1)
            
            sys.stdout.flush()