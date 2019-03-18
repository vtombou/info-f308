from PyQt5.QtWidgets import QGraphicsView,QGraphicsScene
from PyQt5.QtGui import QPen,QBrush,QColor
from PyQt5.QtCore import Qt
from math import sin,cos,radians
from random import randint

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
		self.verticesNb =verticesNb

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

	def drawStep(self,edges,color = "black"):
		self.scene.clear()
		pen = QPen(eval("Qt."+color))
		pen.setWidth(3)
		self.drawVertices()
		for e in edges:
			self.scene.addLine(e[0][0],e[0][1],e[1][0],e[1][1],pen)

		self.scene.update()

	def colorSubTour(self,subTours):
		self.scene.clear()
		pen = QPen()
		pen.setWidth(2)
		self.drawVertices()
		for subTour in subTours:
			pen.setColor(QColor(randint(0,255),randint(0,255),randint(0,255)))
			for i in range(len(subTour)-1):
				self.scene.addLine(subTour[i][0],subTour[i][1],subTour[i+1][0],subTour[i+1][1],pen)
			self.scene.addLine(subTour[-1][0], subTour[-1][1], subTour[0][0], subTour[0][1],pen)



	def drawVertices(self):
		pen = QPen(Qt.black)
		pen.setWidth(2)
		for i in range(self.verticesNb):
			y = (self.height/10+self.width/2)-sin(radians(i*360/self.verticesNb))*(self.width/2-20)
			x = self.width/2 + cos(radians(i*360/self.verticesNb))*(self.width/2-20)
			ellipse = self.scene.addEllipse(x-15,y-15,30,30,pen)