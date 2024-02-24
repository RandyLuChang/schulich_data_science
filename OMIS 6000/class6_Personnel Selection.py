"""
@author: Adam Diamant (2023)
"""

from gurobipy import GRB
import gurobipy as gb

# Create the optimization model
model = gb.Model("Personnel Selection")

# Create the one class of eight decision variables 
x = model.addVars(8, vtype=GRB.BINARY, name="Employee")

# Objective function coefficients
coef = [5, 9, 4, 3, 8, 7, 2, 6]

# The objective function
model.setObjective(gb.quicksum(coef[i]*x[i] for i in range(8)), GRB.MAXIMIZE)

# Add the constraints
model.addConstr(x[0] + x[1] <= 1, "Not Both #1")
model.addConstr(x[3] + x[4] <= 1, "Not Both #2")
model.addConstr(x[2] <= x[1], "If one then both")
model.addConstr(x[6] <= 1 - x[1], "If one then not")
model.addConstr(x[3] <= x[4] + x[5], "If one then another")
model.addConstr(2*x[5] <= x[6] + x[7], "If one then both")
model.addConstr(x[0] + x[1] + x[4] + x[5] + x[7] <= 3, "<= 3 employees")
model.addConstr(x[2] + x[3] + x[6] >= 2, ">= 2 employees")
    
# Optimally solve the problem
model.optimize()

# Print the objective and decision variables
model.printAttr('X')

# The status of the model
print("Model Status: ", model.status)
