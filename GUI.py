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
		nextStepBtnPE = QPushButton("Etape suivante PE")
		runPE = QPushButton("Run PE")

		nextStepBtnPE.clicked.connect(self.onNextStepPEClicked)
		runPE.clicked.connect(self.runPEClicked)

		layout = QVBoxLayout()
		layout.addWidget(nextStepBtnCh)
		layout.addWidget(nextStepBtnPE)
		layout.addWidget(runPE)
		layout.setSpacing(5)
		layout.addStretch(1)
		self.solverGroupBox.setLayout(layout)

	def createGraphGroupBox(self):
		self.graphGroupBox = QGroupBox("Graphe")
		createGraphBtn = QPushButton("Créer le graphe")
		self.graphSizeCB = QComboBox()
		self.graphSizeCB.addItems(["3","4","5","6","10"])

		createGraphBtn.clicked.connect(self.onCreateGraphBtnClicked)


		layout = QVBoxLayout()
		layout.setSpacing(5)
		layout.addWidget(self.graphSizeCB)
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
		graphSize = int(self.graphSizeCB.currentText())
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

	def updatePE(self,usedEdges,color = "black"):
		self.PECanvas.drawStep(usedEdges,color)

	def colorSubTours(self,subTours,step):
		self.PECanvas.colorSubTour(subTours,step)





