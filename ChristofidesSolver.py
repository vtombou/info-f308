import networkx as nx
import networkx.algorithms.approximation as pm


#1- création d'un graphe G connexe et triangulaire
G = nx.Graph()
#1.1-Initialisation des sommets
nodes = range(5)
for i in nodes:  
    G.add_node(i)
#1.2-Initialisation des aretes
G.add_edge(0,1, weight=1 )
G.add_edge(0,3, weight=2 )
G.add_edge(1,2, weight=2 )
G.add_edge(0,2, weight=1 )
G.add_edge(1,3, weight=1 )
G.add_edge(1,4, weight=1 )
G.add_edge(0,4, weight=1 )
G.add_edge(2,3, weight=1 )
G.add_edge(2,4, weight=1 )
G.add_edge(3,4, weight=1 )



#Construction d'un MST de G
MST = nx.minimum_spanning_tree(G)

#Construction du sous graphe M_Impairs induit par l'ensemble des sommets de dégrée impair
MImpairs = nx.Graph()
for i in MST.nodes():
    if MST.degree[i]%2 != 0 :
        MImpairs.add_node(i)
        
for arete in G.edges():
    if arete[0] in MImpairs.nodes and arete[1] in MImpairs.nodes :
        MImpairs.add_edge(*arete)

 
#construction d'un couplage parfait M de poids minimum de MImpairs
M = pm.min_maximal_matching(MImpairs)   #retourne un set de tuples d'aretes

#On définit un multigraphe H à partir des arêtes issues de  M et MST
H = nx.Graph()
H.add_nodes_from( MST.nodes())
H.add_edges_from(MST.edges() )
H.add_edges_from(list(M))
 
#Trouver un cycle eulérien dans M
E = nx.eulerize(H) #Transforms a graph H into an Eulerian multi-graph

#Transformer le cycle eulérien en un cycle hamiltonien en supprimant les éventuels passages en double sur certains sommets.
#**********************************

print("MST OF GRAPH")
print(MST.edges)
print(MST.nodes)
print("Sous Graphe Induit par l'ensemble sommets Impairs")
print("Sommets de dégré impairs :", MImpairs.nodes)
print(MImpairs.edges)
print("MATCHING TUPLES")
print(M)
print("UNION GRAPH Des Graphe ( multi-graphe )")
print(H.edges)
print(H.nodes)
print("EULEURIAN Multi-GRAPH")
print(E.edges)
print(E.nodes)
