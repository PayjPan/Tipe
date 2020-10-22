from copy import deepcopy
import TIPE_EntrepotClasse as entrepot
import TIPE_FctBase as fctB

def floydMarshall(graph, parents):
    noeuds = graph.keys()
    
    for k in noeuds:
        for x in noeuds:
            for y in noeuds:
                w = graph[x][k] + graph[k][y]
                if w < graph[x][y]:
                    graph[x][y] = w
                    parents[x][y] = parents[x][k]
                    
    return()

def ajoutObjetsGraphVide(entrepot, graph, noeudsobjets):
    
    adjvide = entrepot.adjacentVide()
    graphobjet = deepcopy(graph)
    
    # On rajoute les noeuds objets aux noeuds intersections
    for i in graphobjet.keys():
        for j in noeudsobjets:

            graphobjet[i][j] = float('inf')
    
    # On rajoute les noeuds objets
    for i in noeudsobjets:
            
        adj = deepcopy(adjvide)
        
        for j in noeudsobjets:
                        
            if i == j:
                adj[j] = 0
            else:
                adj[j] = float('inf')
                
        graphobjet[i] = adj
    
    return(graphobjet)
    
def remplissageGraph(entrepot, graph):
    
    '''
    On cherche les noeuds voisins superieur et inferieur de chaque noeuds
        
        On monte l'allée jusqu'à trouver un noeud existant (peut ne pas exister)
        On fait de même en descendant
    '''
    
    for i in graph.keys():
        
        keys = list(graph[i].keys())
        keys.remove(i)
        
        x,y = i[0]
        
        # On associe une distance nul à tout les objets avec le même noeuds : objets l'un en face de l'autre ou dans la même case
        lstnoeudsaccecible = [item for item in keys if (x,y) in item]
        
        for k in lstnoeudsaccecible:
            graph[i][k] = 0
        
        # On monte (si c'est possible)...
        if x > 0:
            x2 = x-1
            dst = 1
            
            # On cherche tous les noeuds placé en (x2,y) 
            lstnoeudsaccecible = [item for item in keys if (x2,y) in item]
        
            while lstnoeudsaccecible == []: 
                x2 -= 1
                dst += 1
                
                lstnoeudsaccecible = [item for item in keys if (x2,y) in item]
        
            # On met la distance pour tout les noeuds correspondant 
            for k in lstnoeudsaccecible:
                graph[i][k] = dst
            
        # ... On descends (si c'est possible) 
        if x < len(entrepot.tableau)-1:
            x2 = x+1
            dst = 1
        
            lstnoeudsaccecible = [item for item in keys if (x2,y) in item]
        
            while lstnoeudsaccecible == []: 
                x2 += 1
                dst += 1
                
                lstnoeudsaccecible = [item for item in keys if (x2,y) in item]
        
        # On met la distance pour tout les noeuds correspondant 
        for k in lstnoeudsaccecible:
            graph[i][k] = dst
        
        # plus rarement on peut avoir des noeuds à droite et à gauche
        
        # On va à droite... (si c'est possible) 
        if y < len(entrepot.tableau[0])-1 and entrepot.tableau[x][y+1] == -2 :
            y2 = y+1
            dst = 1
        
            lstnoeudsaccecible = [item for item in keys if (x,y2) in item]
        
            while lstnoeudsaccecible == []: 
                y2 += 1
                dst += 1
                
                lstnoeudsaccecible = [item for item in keys if (x,y2) in item]
        
        # On met la distance pour tout les noeuds correspondant 
        for k in lstnoeudsaccecible:
            graph[i][k] = dst
            
        # ... et à gauche (si c'est possible) 
        if y > 0 and entrepot.tableau[x][y-1] == -2 :
            y2 = y-1
            dst = 1
        
            lstnoeudsaccecible = [item for item in keys if (x,y2) in item]
        
            while lstnoeudsaccecible == []: 
                y2 -= 1
                dst += 1
                
                lstnoeudsaccecible = [item for item in keys if (x,y2) in item]
        
        # On met la distance pour tout les noeuds correspondant 
        for k in lstnoeudsaccecible:
            graph[i][k] = dst
                
        
                
    return graph
   
def lstObjetsToLstNoeuds(entrepot, lst):
    '''
    Création de la liste des noeuds objets
    
    noeudsobjets = [((x',y'),k) | pour tout objets dans la liste]
    
    (x',y') position du noeud, corresponds à la case de l'allée la plus proche de (x,y)
    k = numéro de l'objet
    '''
    
    noeudsobjets = []
    for j in range(len(lst)):
        x = lst[j][0]
        y = lst[j][1]
            
        x, y = entrepot.caseAccecibleLaPlusProche([x, y])
        
        noeudsobjets += [((x,y),j)]
    return noeudsobjets
     
def distanceEntreObjets(entrepot, lst):
    
    graph = entrepot.graphVide()
    
    lstnoeuds = lstObjetsToLstNoeuds(entrepot, lst)
    
    graph = ajoutObjetsGraphVide(entrepot, graph, lstnoeuds)
    
    graph = remplissageGraph(entrepot,graph)
    
    # On créé un graph qui contiendra les parents des noeuds pour reconstruire le chemin final
    global parents 
    parents = {}
    for x in graph.keys():
        parents[x] = {}
    
    for i in graph.keys():
        for j in graph[i].keys():
            parents[i][j] = j
    
    floydMarshall(graph, parents)
    
    # On ne garde que les distances et les chemins entre objets
    dst = {}
    chm = {}
    for k in graph.keys():
        # On regarde les noeuds qui correspondent à des objets
        if k[1] > -1:
            dstvoisin = {}
            chmvoisin = {}
            
            for x in graph[k].keys():
                # On regarde les distances aux autres objets
                if x[1] > -1:
                    
                    # {j: distance de i --> j | pour j E [1,N]}
                    dstvoisin[x[1]] = graph[k][x]
                    # {j: chemin de i --> j | pour j E [1,N]}
                    chmvoisin[x[1]] = chmEntreNoeuds(parents, k, x)
                    
            #{i : {j: distance de i --> j | pour j E [1,N]} | pour i E [1,N] }
            dst[k[1]] = dstvoisin
            chm[k[1]] = chmvoisin
    
    return (dst, chm)

def distanceChemin(chm, distance):
    if len(chm) < 2:
        return("ERREUR -- chemin d'une liste trop petite")
    
    # On initialise
    dst = distance[chm[0]][chm[1]]
    
    # On calcul la distance total du chemin
    for k in range(2,len(chm)):
        dst += distance[chm[k-1]][chm[k]]
    
    # On ferme le chemin
    dst += distance[chm[0]][chm[k]]
    
    return (dst)

def chmEntreNoeuds(parents, pt1, pt2):
    pttmp = pt2
    chm = []
    
    while pttmp != pt1: 
        if pt1 in parents[pttmp].keys():
            pttmp = parents[pttmp][pt1]
        else:
            pttmp = pt1  
            
        chm += [pttmp[0]] 
    return chm

