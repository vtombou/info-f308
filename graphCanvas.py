from PyQt5.QtWidgets import QGraphicsView,QGraphicsScene
from PyQt5.QtGui import QPen,QBrush
from PyQt5.QtCore import Qt
from math import sin,cos,radians

class GraphCanvas(QGraphicsView):
	def __init__(self,width,height):
		QGraphicsView.__init__(self)
		self.width,self.height = width,height
		self.setGeometry(0,0,width,height)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.scene = QGraphicsScene(0,0,width,height -80)
		self.setScene(self.scene)

	def drawGraph(self,verticesNb):
		self.scene.clear()
		blackPen = QPen(Qt.black)
		blackPen.setWidth(3)
		vertices = []

		for i in range(verticesNb):
			y = (self.height/10+self.width/2)-sin(radians(i*360/verticesNb))*(self.width/2-20)
			x = self.width/2 + cos(radians(i*360/verticesNb))*(self.width/2-20)
			ellipse = self.scene.addEllipse(x-15,y-15,30,30,blackPen)
			j = i+1
			for j in range(i):
				self.scene.addLine(x,y,vertices[j][0],vertices[j][1])
			vertices.append((x,y))
		

		self.scene.update()
		return vertices

##	def drawStep(self,edges):
