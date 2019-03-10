from __future__ import division
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pprint
class PESolver:

	def __init__(self,controller):
				#solver
		self.controller = controller
		self.controller.setPE(self)

		self.opt = SolverFactory("cplex")

		# model Abstrait de données
		model = AbstractModel()

		#Ensemble de noeuds
		model.Nodes = Set()

		model.V = Set(within = model.Nodes)

		#Ensemble d'Arcs
		model.Arcs = Set(within = model.Nodes * model.Nodes)

		#Fonction qui retourne l'ensemble des aretes incident a V ( Conv V )
		def ConvV_init(model,V):
		        return ( E for E in model.Arcs if V in E )
		#Définition convV
		model.ConvV = Set(model.Nodes, initialize = ConvV_init,within= model.Nodes*model.Nodes)

		#définition parametre C 
		model.C = Param(model.Arcs)

		#definition x
		model.X = Var(model.Arcs, domain=Binary )

		def obj_expression(model):
		    return summation( model.C, model.X )
		model.OBJ = Objective(rule=obj_expression)

		#Définition de Contrainte
		def ax_constraint_rule(model,V):
		    # return the expression for the constraint for i
		    return sum( model.X[E] for E in model.ConvV[V]) == 2
		model.AxbConstraint = Constraint( model.Nodes,rule=ax_constraint_rule)

		self.model = model

	def solveInstance(self,tsp,step = False):
		data = self.formatTspData(tsp)
		# data = {None:{
		# 		"Nodes": {None: [str(i) for i in range(size)]},
		# 		"Arcs": {None: [("A","B"),("A","C"),("B","C"),("A","D"),("B","D"),("C","D")]},
		# 		"C": {("A","B"): 1.4, ("A","C"): 2.7,("B","C"): 1.6,("A","D"): 2.0,("B","D"): 3.0, ("C","D"): 5.0},
		# }}
		i= self.model.create_instance(data)
		results = self.opt.solve(i)
		usedEdges = self.findUsedEdges(tsp,i)
		self.controller.updateView(usedEdges)

	def formatTspData(self,tsp):
		size = tsp.getSize()
		costMat = tsp.getCostMat()
		Nodes = []
		Arcs = []
		C = {}
		for i in range(size):
			Nodes.append(str(i))
			for j in range(i+1,size):
				arc = (str(i),str(j))
				Arcs.append(arc)
				C[arc] = costMat[j-1][i]
		data = {None:{
				"Nodes": {None: Nodes},
				"Arcs": {None: Arcs},
				"C" : C,
		}}
		return data

	def findUsedEdges(self,tsp,instance):
		vertices = tsp.getVertices()
		usedEdges = []
		for e,v in instance.X.items():
			if v == 1:
				edge = (vertices[int(e[0])],vertices[int(e[1])])
				usedEdges.append(edge)
		return usedEdges


