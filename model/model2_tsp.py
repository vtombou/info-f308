# model2_tsp
from __future__ import division
from pyomo.environ import *
from pyomo.opt import SolverFactory


#solver
opt = SolverFactory("cplex")

# model Abstrait de données
model = AbstractModel()

#Ensemble de noeuds
model.Nodes = Set()

model.V = Set(within = model.Nodes)

#Ensemble d'Arcs
model.Arcs = Set(within = model.Nodes * model.Nodes)

#Fonction qui retourne l'ensemble des aretes incident a V ( Conv V )
def ConvV_init(model):
    for V in model.Nodes :
        return ( E for E in model.Arcs if V in E )
#Définition convV
model.ConvV = Set(model.Nodes, initialize = ConvV_init,within= model.Nodes*model.Nodes)

#définition parametre C 
model.C = Param(model.Arcs)

#definition x
model.X = Var(model.Arcs, domain=Binary )

data = {None:{
	"Nodes": {None: ["A","B","C","D"]},
	"Arcs": {None: [("A","B"),("A","C"),("B","C"),("A","D"),("B","D"),("C","D")]},
	"C": {("A","B"): 1.4, ("A","C"): 2.7,("B","C"): 1.6,("A","D"): 2.0,("B","D"): 3.0, ("C","D"): 5.0},
}}



#Fonction objective
def obj_expression(model):
    return summation( model.C, model.X )
model.OBJ = Objective(rule=obj_expression)

#Définition de Contrainte
def ax_constraint_rule(model,V):
    # return the expression for the constraint for i
    return sum( model.X[E] for E in model.ConvV[V]) == 2
model.AxbConstraint = Constraint( model.Nodes,rule=ax_constraint_rule)

i= model.create_instance(data)
i.pprint()
results = opt.solve(i)
results.write()
