from random import randint
class TSP:
	def __init__(self,vertices = None, edgesCosts = []):
		self.vertices = vertices
		self.edgesCosts = edgesCosts

	# def setController(self,controller):
	# 	self.controller = controller

	def setVertices(self,vertices):
		self.vertices = vertices
		self.tspSize = len(self.vertices)

	def createEdgesCostMat(self):
		for i in range(self.tspSize-1):
			self.edgesCosts.append([randint(1,100) for x in range(i+1)])

	def updateGraph(self,vertices):
		self.setVertices(vertices)
		self.createEdgesCostMat()
		print(self.edgesCosts)

	def getSize(self):
		return self.tspSize

	def getCostMat(self):
		return self.edgesCosts

	def getVertices(self):
		return self.vertices

	

