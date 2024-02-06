"""
@author: Adam Diamant (2023)
"""

from gurobipy import GRB
import gurobipy as gb

# Should we implement a variable pricing scheme?
isVariablePricing = True

# Linear price response functions (intercept, slope)
response = [[3100, 62], [1900, 50], [1700, 40], [1710, 42], [2000, 53], [2500, 54], [3300, 60]]

# Create a new optimization model to maximize revenue
model = gb.Model("Variable Pricing Model")

# Construct the decision variables
p = model.addVars(7, lb=0, ub=40, vtype=GRB.CONTINUOUS, name="Price")
d = model.addVars(7, lb=0, ub=1100, vtype=GRB.CONTINUOUS, name="Daily Demand")

#Objective Function
model.setObjective(gb.quicksum((p[n]-19)*d[n] for n in range(7)), GRB.MAXIMIZE)

# Demand is diverted from days of higher prices to days with lower prices
model.addConstrs((d[n] == response[n][0] - response[n][1]*p[n] + 9*gb.quicksum(p[m] - p[n] for m in range(7)) for n in range(7)), "Demand Constraint")
    
# If variable pricing is not allowed, we must add constraints to ensure that
# the price on each day of the week is the same. 
if not isVariablePricing:
    for n in range(6):
        model.addConstr(p[n] == p[n+1], "Equality Constraint %i" %n)
      
# Solve our model
model.optimize()

# Print the objective and decision variables
model.printAttr('X')
