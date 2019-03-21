import networkx as nx
import networkx.algorithms.approximation as pm
from TSP import TSP


class Christofides:

    def graphe_PE(netW, n):
        graphe = netW.Graph()

        # Initialisation TSP
        tsp = TSP()
        tsp.setVertices(range(n))
        tsp.createEdgesCostMat()

        # Initialisation du graphe
        nodes = range(tsp.getSize())  # ensemble de sommets
        matriceCost = tsp.getCostMat()  # matrice des couts
        for i in range(len(nodes) - 1):
            for j in range(i + 1):
                graphe.add_node(i)
                graphe.add_edge(i, j, weight=matriceCost[i][j])

        return graphe

    def graphe_impairs(netW, graphe, mst):
        """
        Cette fonction retourne un sous-graphe de 'graphe' induit par l'ensemble des sommets de dégré impairs de 'mst'
        :params netW, graphe, mst:
        :return:
        """
        grapheI = netW.Graph()
        # construction de l'ensemble de sommets
        for i in mst.nodes():
            if mst.degree[i] % 2 != 0:
                grapheI.add_node(i)
        # construction de l'ensemble d'aretes
        for arete in graphe.edges():
            if arete[0] in grapheI.nodes and arete[1] in grapheI.nodes:
                grapheI.add_edge(*arete)

        return grapheI

    def euler_circ(netW, graphe):
        """
        Cette fonction prend en paramètre un graphe et retourne un tuple constitué de la liste d'aretes et
        la liste de sommets dans l'ordre de parcours du circuit euleurien; ou -1 si le graphe n'est euleurian.
        :param netW:
        :param graphe:
        :return:
        """
        if netW.is_eulerian(graphe):
            aretes_euler = list(netW.eulerian_circuit(graphe))
            sommets_euler = [aretes_euler[0][0]]
            for arete in aretes_euler:
                for sommet in arete:
                    if sommet != sommets_euler[-1]:
                        sommets_euler.append(sommet)
            return aretes_euler, sommets_euler
        else:
            return -1, -1

    def multi_graphe(netW, mst, cp):
        """
        Cette fonction retourne un multigraphe construit a partir d'un MST et de son couplage parfait de poid minimal.
        :param netW:
        :param mst:
        :param cp:
        :return:
        """
        graphe = netW.Graph()
        graphe.add_nodes_from(mst.nodes())
        graphe.add_edges_from(mst.edges())
        graphe.add_edges_from(list(cp))

        return graphe

    def halmiton_euler(list_sommets):
        """
        Cette fonction prend en paramètre une liste de sommets d'un circuit d'euler et retourne la
        liste de sommets du circuit Hamiltonien associé
        :param list_sommets:
        :return:
        """
        if list_sommets != -1:
            hamilton, visites = [], []
            for i in range(0, len(list_sommets)):
                if list_sommets[i] not in visites or i == len(list_sommets) - 1:
                    visites.append(list_sommets[i])
                    hamilton.append(list_sommets[i])
            return hamilton
        else:
            return -1

    def solve(self, netW, n):
        """
        *******************************
        *     Programme Principal     *
        *******************************
        """
        # 1- création d'un graphe G connexe et triangulaire
        G = self.graphe_PE(netW, n)

        # 2- Construction d'un MST de G
        MST = netW.minimum_spanning_tree(G)

        # 3- Construction du sous graphe MImpairs de G, induit par l'ensemble des sommets de dégré impair du MST
        MImpairs = self.graphe_impairs(nx, G, MST)

        # 4- construction d'un couplage parfait CP de poids minimum de MImpairs
        CP = pm.min_maximal_matching(MImpairs)  # retourne un set de tuples d'aretes

        # 5- On définit un multigraphe H à partir des arêtes issues de  CP et MST
        H = self.multi_graphe(netW, MST, CP)

        # 6- Trouver un cycle eulérien dans H
        aretes_cycle_euler, sommets_euler = self.euler_circ(netW, H)

        # 7- Trouver un cycle Halmitonien de
        hamilton = self.halmiton_euler(sommets_euler)

        return hamilton
