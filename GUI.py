from PyQt5.QtWidgets import *
from graphCanvas import GraphCanvas
# from controller import *

class GUI:
	def __init__(self,controller):
		self.controller = controller
		self.controller.setGUI(self)

		self.app = QApplication([])
		screenResolution = self.app.desktop().screenGeometry()
		self.width, self.height = screenResolution.width(), screenResolution.height()

		self.window = QWidget()
		self.window.setGeometry(0,0,self.width,self.height)

		self.initWidgets()

		layout = QHBoxLayout()
		layout.addWidget(self.PECanvas)
		layout.addWidget(self.chrisCanvas)
		layout.addLayout(self.settingsBox)
		self.window.setLayout(layout)
		self.window.show()

		self.app.exec_()

	def initWidgets(self):
		self.PECanvas = GraphCanvas(self.width/2.4,self.height)
		self.chrisCanvas = GraphCanvas(self.width/2.4,self.height)

		self.createGraphGroupBox()
		self.createSolverGroupBox()
		self.createSettingsBox()

	def createSolverGroupBox(self):
		self.solverGroupBox = QGroupBox("Solver")

		nextStepBtnCh = QPushButton("Etape suivante christophides")
		runCh = QPushButton("Run christofides")
		nextStepBtnPE = QPushButton("Etape suivante PE")
		runPE = QPushButton("Run PE")
		self.delayEdit = QLineEdit("Délais run")


		nextStepBtnPE.clicked.connect(self.onNextStepPEClicked)
		runPE.clicked.connect(self.runPEClicked)
		nextStepBtnCh.clicked.connect(self.onNextStepChClicked)
		runCh.clicked.connect(self.runChClicked)
		self.delayEdit.returnPressed.connect(self.changeDelay)

		layout = QVBoxLayout()
		layout.addWidget(nextStepBtnPE)
		layout.addWidget(runPE)
		layout.addWidget(nextStepBtnCh)
		layout.addWidget(runCh)
		layout.addWidget(self.delayEdit)
		layout.setSpacing(5)
		layout.addStretch(1)
		self.solverGroupBox.setLayout(layout)

	def createGraphGroupBox(self):
		self.graphGroupBox = QGroupBox("Graphe")
		createGraphBtn = QPushButton("Créer le graphe")
		self.sizeBox = QLineEdit("Taille du graphe")

		createGraphBtn.clicked.connect(self.onCreateGraphBtnClicked)


		layout = QVBoxLayout()
		layout.setSpacing(5)
		layout.addWidget(self.sizeBox)
		layout.addWidget(createGraphBtn)
		layout.addStretch(1)
		self.graphGroupBox.setLayout(layout)
		self.graphGroupBox.setMaximumHeight(self.height/2.5)

	def createSettingsBox(self):
		self.settingsBox = QVBoxLayout()

		self.settingsBox.setSpacing(2)
		self.settingsBox.addWidget(self.graphGroupBox)
		self.settingsBox.addWidget(self.solverGroupBox)

	def onCreateGraphBtnClicked(self):
		self.nextStepCnt = 0
		self.nextStepCntCh = 0
		self.step = True
		graphSize = int(self.sizeBox.text())
		verticesCoords = self.chrisCanvas.drawGraph(graphSize)
		self.PECanvas.drawGraph(graphSize)
		self.controller.updateTSPGraph(verticesCoords)

	def onNextStepPEClicked(self):
		self.nextStepCnt+=1
		if self.nextStepCnt == 1:
			self.controller.solveInstance(True)
		else:
			self.controller.unblockSolver(True)

	def runPEClicked(self):
		self.controller.solveInstance(False)

	def runChClicked(self):
		self.step = False
		self.controller.solveChristofides(False)


	def onNextStepChClicked(self):
		self.nextStepCntCh += 1
		print(self.nextStepCntCh)
		if self.nextStepCntCh != 1:
			self.controller.unblockChristofides(True)

		# if self.nextStepCntCh !=1 and self.nextStepCntCh!= 3 and self.nextStepCntCh!=5:
		# 	self.controller.unblockChristofides(True)
		# elif self.nextStepCntCh == 3:
		# 	vertices = self.controller.getVertices()
		# 	self.chrisCanvas.oddVSubGraph(vertices)
		# elif self.nextStepCntCh == 5:
		# 	self.chrisCanvas.eulerian()
		else:
			self.controller.solveChristofides(True)

	def updatePE(self,usedEdges,color = "black"):
		self.PECanvas.drawStep(usedEdges,color)

	def colorSubTours(self,subTours,step):
		self.PECanvas.colorSubTour(subTours,step)

	def updateChristofides(self,arg):
		if not self.step:
			self.nextStepCntCh +=1
		self.chrisCanvas.updateChristofides(self.step,self.nextStepCntCh,arg)

	def changeDelay(self):
		try:
			delay = int(self.delayEdit.text()) * 1000
			print(delay)
			self.PECanvas.updateDelay(delay)
			self.ChCanvas.updateDelay(delay)
		except:
			pass





