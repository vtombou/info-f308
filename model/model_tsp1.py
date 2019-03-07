# abstract1.py
from __future__ import division
from pyomo.environ import *

#Définition d'un model Abstract de donné
model = AbstractModel()

#définition d'un parametre n appartenant a l'ensemble des entiers naturel non null 
model.n = Param(within=NonNegativeIntegers)

#définition des ensemble I et J pris dans {1 ..n}
model.I = RangeSet(1, model.n)
model.J = RangeSet(1, model.n)

#définition des parametres c, d'indices i, j
model.c = Param(model.I, model.J)

# definition des la variable x d'indice i,j
model.x = Var(model.J, model.J, domain=Binary)

#Fonction objective
def obj_expression(model):
    return summation( model.c, model.x )

model.OBJ = Objective(rule=obj_expression)

#Définition des Contraintes
def ax_constraint_rule1(model, i):
    # return the expression for the constraint for i
    return sum( model.x[i, j] for i in model.I) == 1

def ax_constraint_rule2(model, i):
    # return the expression for the constraint for j
    return sum( model.x[i, j] for j in model.J) == 1

#Contrainte sur i
model.AxbConstraint = Constraint(model.I, rule=ax_constraint_rule1)

#Contrainte sur j
model.AxbConstraint = Constraint(model.I, rule=ax_constraint_rule2)