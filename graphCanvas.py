from PyQt5.QtWidgets import QGraphicsView,QGraphicsScene

class GraphCanvas(QGraphicsView):
	def __init__(self,width,height):
		QGraphicsView.__init__(self)
		print(width,height)
		self.scene = QGraphicsScene(0,0,width,height)
		self.setScene(self.scene)
