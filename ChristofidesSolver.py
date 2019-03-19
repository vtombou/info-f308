import networkx as nx
import networkx.algorithms.approximation as pm

# 1- création d'un graphe G connexe et triangulaire
G = nx.Graph()
# 1.1-Initialisation des sommets
nodes = range(5)
for i in nodes:
    G.add_node(i)
# 1.2-Initialisation des aretes
G.add_edge(0, 1, weight=1)
G.add_edge(0, 3, weight=2)
G.add_edge(1, 2, weight=2)
G.add_edge(0, 2, weight=1)
G.add_edge(1, 3, weight=1)
G.add_edge(1, 4, weight=1)
G.add_edge(0, 4, weight=1)
G.add_edge(2, 3, weight=1)
G.add_edge(2, 4, weight=1)
G.add_edge(3, 4, weight=1)

#2- Construction d'un MST de G
MST = nx.minimum_spanning_tree(G)

#3- Construction du sous graphe M_Impairs induit par l'ensemble des sommets de dégré impair
MImpairs = nx.Graph()
for i in MST.nodes():
    if MST.degree[i] % 2 != 0:
        MImpairs.add_node(i)

for arete in G.edges():
    if arete[0] in MImpairs.nodes and arete[1] in MImpairs.nodes:
        MImpairs.add_edge(*arete)

#4- construction d'un couplage parfait M de poids minimum de MImpairs
M = pm.min_maximal_matching(MImpairs)  # retourne un set de tuples d'aretes

#5- On définit un multigraphe H à partir des arêtes issues de  M et MST
H = nx.Graph()
H.add_nodes_from(MST.nodes())
H.add_edges_from(MST.edges())
H.add_edges_from(list(M))

#6- Trouver un cycle eulérien dans H
if nx.is_eulerian(H) :
    aretes_cycle_euler = list (nx.eulerian_circuit(H))
    sommets_cycle_euler = [aretes_cycle_euler[0][0]]
    for arete in aretes_cycle_euler:
        for sommet in arete :
            if sommet != sommets_cycle_euler[-1] :
                sommets_cycle_euler.append(sommet)


#7- Trouver un cycle Halmitonien de
hamilton , visites = [], []
for i in range(0, len(sommets_cycle_euler)) :
    if sommets_cycle_euler[i] not in visites or i == len(sommets_cycle_euler) - 1:
        visites.append(sommets_cycle_euler[i])
        hamilton.append(sommets_cycle_euler[i])


print("Euleurian circuit of E")
print(aretes_cycle_euler)
print(sommets_cycle_euler)

print("Halmitonian circuit of E")
print(hamilton)