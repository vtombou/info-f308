from __future__ import division
from pyomo.environ import *
from pyomo.opt import SolverFactory
from threading import Thread
from time import sleep
import pyutilib.subprocess.GlobalData
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
		pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False

	def solveInstance(self,tsp,step = False):
		finished = False
		data = self.formatTspData(tsp)
		i= self.model.create_instance(data)
		while not finished:
			results = self.opt.solve(i)
			usedEdgesCoords,usedSubGraph = self.findUsedEdges(tsp,i)
			compCon = self.detectSubTours(usedSubGraph)
			if len(compCon) > 1:
				compConCoords = self.translateCompConToCoords(compCon,tsp.getVertices())
				self.controller.colorSubTours(compConCoords)
				if step:
					# t = Thread(target = self.waitForNextStep)
					# t.start()
					self.waitingForNextStep = True
					while self.waitingForNextStep:
						sleep(0.3)
					print("Yeeeey")
			else:
				finished = True
				self.controller.updateView(usedEdgesCoords,"green")




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
		usedEdgesCoords = []
		usedSubGraph = [[] for i in range (tsp.getSize())]
		for e,v in instance.X.items():
			if v == 1:
				print("e: "+str(e))
				edgeCoords = (vertices[int(e[0])],vertices[int(e[1])])
				usedEdgesCoords.append(edgeCoords)
				usedSubGraph[int(e[0])].append(int(e[1]))
				usedSubGraph[int(e[1])].append(int(e[0]))
		print(usedSubGraph)
		return usedEdgesCoords,usedSubGraph

	def detectSubTours(self,subGraph):
		conComp = 0
		ind = 0
		val = [ 0 for k in range(len(subGraph))]
		comp = []
		#inval = [ 0 for k in range(len(subGraph))]
		for k in range(len(subGraph)):
			if val[k] == 0:
				inval = []
				conComp += 1
				val,inval,ind = self.explore(k,subGraph,val,inval,ind)
				#inval[val[k]-1]= -inval[val[k]-1]
				comp.append(inval)
		print(val,comp,conComp)
		return comp


	def explore(self,k,subGraph,val,inval,ind):
		ind +=1
		print("k: "+str(k))
		print("indice: "+ str(ind))
		val[k] = ind
		inval.append(k)
		#inval[ind-1] = k
		print("val: " + str(val))
		print("inval: "+str(inval))
		for adj in subGraph[k]:
			if (val[adj] == 0):
				val,inval,ind = self.explore(adj,subGraph,val,inval,ind)
		return val,inval,ind

	def translateCompConToCoords(self,compCon,verticesCoords):
		for i in compCon:
			for j in range(len(i)):
				i[j] = verticesCoords[i[j]]
		return compCon

	def launchThread(self,tsp,step):
		try:
			t = Thread(target = self.solveInstance, args=(tsp,step))
			print("hey")
			t.start()
		except:
			print("Error: unable to start thread")

	def unblock(self):
		self.waitingForNextStep = False

	# def waitForNextStep(self):
	# 	self.waitingForNextStep = True
	# 	while self.waitingForNextStep:
	# 		sleep(0.3)
	# 	print("Yeeeey")



