from TSP import TSP
from GUI import GUI
class Controller:

	def setGUI(self,GUI):
		self.GUI = GUI

	def setTSP(self,TSP):
		self.TSP = TSP

	def setPE(self,peSolver):
		self.peSolver = peSolver

	def updateTSPGraph(self,vertices):
		self.TSP.updateGraph(vertices)

	def updateViewPE(self,edges):
		self.GUI.updatePE(edges)

	def colorSubTours(self,subTours):
		self.GUI.colorSubTours(subTours)

	def solveInstance(self,step):
		self.peSolver.launchThread(self.TSP,step)

	def updateView(self,usedEdges,color = "black"):
		self.GUI.updatePE(usedEdges,color)

	def unblockSolver(self):
		self.peSolver.unblock()
