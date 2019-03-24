import networkx as nx
import networkx.algorithms.approximation as pm
from threading import Thread
from time import sleep
from TSP import TSP


class ChSolver:

    def __init__(self,controller):
        self.controller = controller
        self.controller.setChristofidesSolver(self)

    def graphe_PE(self,tsp):
        graphe = nx.Graph()

        # Initialisation TSP

        # Initialisation du graphe
        size = tsp.getSize()  # ensemble de sommets
        matriceCost = tsp.getCostMat()  # matrice des couts
        for i in range(size):
            graphe.add_node(i)
            for j in range(i+1,size):
                graphe.add_edge(i, j, weight=matriceCost[j-1][i])
#                graphe.add_edge(j,i, weight = matriceCost[j-1][i])
        return graphe

    def graphe_impairs(self,graphe, mst):
        """
        Cette fonction retourne un sous-graphe de 'graphe' induit par l'ensemble des sommets de dégré impairs de 'mst'
        :params netW, graphe, mst:
        :return:
        """
        grapheI = nx.Graph()
        # construction de l'ensemble de sommets
        for i in mst.nodes():
            if mst.degree[i] % 2 != 0:
                grapheI.add_node(i)
        # construction de l'ensemble d'aretes
        for arete in graphe.edges():
            if arete[0] in grapheI.nodes and arete[1] in grapheI.nodes:
                grapheI.add_edge(*arete)

        return grapheI

    def euler_circ(self,graphe):
        """
        Cette fonction prend en paramètre un graphe et retourne un tuple constitué de la liste d'aretes et
        la liste de sommets dans l'ordre de parcours du circuit euleurien; ou -1 si le graphe n'est euleurian.
        :param netW:
        :param graphe:
        :return:
        """
        if nx.is_eulerian(graphe):
            aretes_euler = list(nx.eulerian_circuit(graphe))
            sommets_euler = [aretes_euler[0][0]]
            for arete in aretes_euler:
                for sommet in arete:
                    if sommet != sommets_euler[-1]:
                        sommets_euler.append(sommet)
            return aretes_euler, sommets_euler
        else:
            return -1, -1

    def multi_graphe(self,mst, cp):
        """
        Cette fonction retourne un multigraphe construit a partir d'un MST et de son couplage parfait de poid minimal.
        :param netW:
        :param mst:
        :param cp:
        :return:
        """
        graphe = nx.Graph()
        graphe.add_nodes_from(mst.nodes())
        graphe.add_edges_from(mst.edges())
        graphe.add_edges_from(list(cp))

        return graphe

    def halmiton_euler(self,list_sommets):
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

    def solve(self,tsp,chQueue,step):
        """
        *******************************
        *     Programme Principal     *
        *******************************
        """
        # 1- création d'un graphe G connexe et triangulaire
        G = self.graphe_PE(tsp)

        # 2- Construction d'un MST de G
        MST = nx.minimum_spanning_tree(G)
        edgesCoords = self.changeToCoordsEdges(tsp,MST.edges)
        chQueue.put(("self.updateChristofides",edgesCoords))

        if step:
            self.block()
        # 3- Construction du sous graphe MImpairs de G, induit par l'ensemble des sommets de dégré impair du MST
        MImpairs = self.graphe_impairs(G, MST)
        chQueue.put(("self.updateChristofides",MImpairs))
        if step:
            self.block()
        # 4- construction d'un couplage parfait CP de poids minimum de MImpairs
        CP = pm.min_maximal_matching(MImpairs)  # retourne un set de tuples d'aretes
        edgesCoords = self.changeToCoordsEdges(tsp,CP)
        chQueue.put(("self.updateChristofides", edgesCoords))

        if step:
            self.block()
        # 5- On définit un multigraphe H à partir des arêtes issues de  CP et MST
        H = self.multi_graphe(MST, CP)

        # 6- Trouver un cycle eulérien dans H
        aretes_cycle_euler, sommets_euler = self.euler_circ(H)

        # 7- Trouver un cycle Halmitonien de
        hamilton = self.halmiton_euler(sommets_euler)
        hamiltonEdges = self.verticesToEdges(tsp,hamilton)
        chQueue.put(("self.updateChristofides",hamiltonEdges))


    def launchThread(self, tsp, chQueue, step):
        try:
            t = Thread(target=self.solve, args=(tsp, chQueue, step))
            t.start()
        except:
            print("Error: unable to start thread")

    def block(self):
        self.waitingForNextStep = True
        while self.waitingForNextStep:
            sleep(0.3)

    def unblock(self):
        self.waitingForNextStep = False

    def changeToCoordsEdges(self,tsp,edges):
        vertices = tsp.getVertices()
        coordEdges = []
        for e in edges:
            coordEdges.append((vertices[e[0]],vertices[e[1]]))
        return coordEdges

    def verticesToEdges(self,tsp,vertices):
        v = tsp.getVertices()
        edges =[]
        for i in range(len(vertices)-1):
            edges.append((v[vertices[i]],v[vertices[i+1]]))
        edges.append((v[vertices[-1]],v[vertices[0]]))
        return edges

