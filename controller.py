from TSP import TSP
from GUI import GUI
import queue
from time import sleep

class Controller:

	def setGUI(self,GUI):
		self.GUI = GUI

	def setTSP(self,TSP):
		self.TSP = TSP

	def setPE(self,peSolver):
		self.peSolver = peSolver

	def setChristofidesSolver(self,chSolver):
		self.chSolver = chSolver


	def updateTSPGraph(self,vertices):
		self.TSP.updateGraph(vertices)

	def updateViewPE(self,edges):
		self.GUI.updatePE(edges)

	def colorSubTours(self,subTours,step):
		self.GUI.colorSubTours(subTours,step)

	def solveInstance(self,step):
		isStep = False
		items = []
		self.mainQueue = queue.Queue()
		self.peSolver.launchThread(self.TSP,self.mainQueue,step)
		while items != None and not isStep:
			items = self.mainQueue.get()
			try:
				fct = items[0]
				args = items[1:] + (step,)
				eval(fct + "(*args)")
			except:
				pass
			isStep = step

	def updateView(self,usedEdges,color = "black",step = "False"):
		self.GUI.updatePE(usedEdges,color)

	def unblockSolver(self,step):
		self.peSolver.unblock()
		items = self.mainQueue.get()
		fct = items[0]
		args = items[1:]+(step,)
		eval(fct + "(*args)")

	def solverChristofides(self,step):
		isStep = False
		items = []
		self.chQueue = queue.Queue()
		self.chSolver.launchThread(self.TSP,self.chQueue,step)
		while items != None and not isStep:
			items = self.chQueue.get()
			try:
				fct = items[0]
				args = items[1:] + (step,)
				eval(fct + "(*args)")
			except:
				pass
			isStep = step

	def unblockChristofides(self,step):
		self.chSolver.unblock()
		items = self.chQueue.get()
		fct = items[0]
		args = items[1:]+(step,)
		eval(fct + "(*args)")
