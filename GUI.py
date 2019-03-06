from PyQt5.QtWidgets import *
from graphCanvas import GraphCanvas

class GUI:
	def __init__(self):
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
		self.PECanvas = GraphCanvas(self.width/4,self.height)
		self.chrisCanvas = GraphCanvas(self.width/4,self.height)

		self.createGraphGroupBox()
		self.createSolverGroupBox()
		self.createSettingsBox()

	def createSolverGroupBox(self):
		self.solverGroupBox = QGroupBox("Solver")

		nextStepBtnCh = QPushButton("Etape suivante christophides")
		nextStepBtnPE = QPushButton("Etape suivante PE")
		runComplete = QPushButton("Run")

		layout = QVBoxLayout()
		layout.addWidget(nextStepBtnCh)
		layout.addWidget(nextStepBtnPE)
		layout.addWidget(runComplete)
		layout.setSpacing(5)
		layout.addStretch(1)
		self.solverGroupBox.setLayout(layout)

	def createGraphGroupBox(self):
		self.graphGroupBox = QGroupBox("Graphe")
		createGraphBtn = QPushButton("Créer le graphe")
		graphSizeCB = QComboBox()

		layout = QVBoxLayout()
		layout.setSpacing(5)
		layout.addWidget(graphSizeCB)
		layout.addWidget(createGraphBtn)
		layout.addStretch(1)
		self.graphGroupBox.setLayout(layout)
		self.graphGroupBox.setMaximumHeight(self.height/2.5)

	def createSettingsBox(self):
		self.settingsBox = QVBoxLayout()

		self.settingsBox.setSpacing(2)
		# self.settingsBox.setMargin(2)

		self.settingsBox.addWidget(self.graphGroupBox)
		self.settingsBox.addWidget(self.solverGroupBox)



