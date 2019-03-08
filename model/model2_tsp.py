# model2_tsp
from __future__ import division
from pyomo.environ import *

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
model.ConvV = Set(model.V, initialize = ConvV_init)

#définition parametre C 
model.C = Param(model.Arcs)

#definition x
model.X = Var(model.Arcs, domain=Binary )

#Fonction objective
def obj_expression(model):
    return summation( model.C, model.X )
model.OBJ = Objective(rule=obj_expression)

#Définition de Contrainte
def ax_constraint_rule(model):
    # return the expression for the constraint for i
    return sum( model.X[E] for E in model.Arcs) == 2
model.AxbConstraint = Constraint(model.Arcs, rule=ax_constraint_rule)
