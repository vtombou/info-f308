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

	def solveInstance(self):
		self.peSolver.solveInstance(self.TSP)

	def updateView(self,usedEdges):
		self.GUI.updatePE(usedEdges)
