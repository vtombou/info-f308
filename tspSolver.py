from GUI import GUI
from controller import Controller
from TSP import TSP
from PESolver import PESolver
from ChristofidesSolver import ChSolver
def main():
	controller = Controller()
	controller.setTSP(TSP())
	PESolver(controller)
	ChSolver(controller)
	GUI(controller)

main()