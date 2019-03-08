from GUI import GUI
from controller import Controller
from TSP import TSP
def main():
	controller = launchController()
	TSP = createTSP()
	controller.setTSP(TSP)
	TSP.setController(controller)
	GUI = GUILaunch(controller)
	

def GUILaunch(controller):
	Gui = GUI(controller)
	return Gui

def launchController():
	controller= Controller()
	return controller

def createTSP():
	Tsp= TSP()
	return Tsp

main()