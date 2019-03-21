from GUI import GUI
from controller import Controller
from TSP import TSP
from PESolver import PESolver
def main():
	controller = Controller()
	controller.setTSP(TSP())
	PESolver(controller)
	GUI(controller)

main()