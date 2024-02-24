"""
@author: Adam Diamant (2023)
"""

import gurobipy as gb
from gurobipy import GRB

# Create a new model
model = gb.Model("Project Investment")

# Variables
x = model.addVars(6, vtype=GRB.BINARY, name="Project")

# Objective function
objective = 16 * x[0] + 22 * x[1] + 12 * x[2] + 8 * x[3] + 11 * x[4] + 19 * x[5]
model.setObjective(objective, GRB.MAXIMIZE)

# Constraints
model.addConstr(5 * x[0] + 7 * x[1] + 4 * x[2] + 3 * x[3] + 4 * x[4] + 6 * x[5] <= 14, "Cash_Constraint")
model.addConstr(x[0] + x[1] + x[2] + x[3] + x[4] + x[5] == 3, "Logical_Constraint1")
model.addConstr(x[1] <= x[0], "Logical_Constraint2")
model.addConstr(x[0] + x[2] <= 1, "Logical_Constraint3")
model.addConstr(x[3] + x[4] == 1, "Logical_Constraint4")
model.addConstr(x[0] + x[1] <= 1 + x[2], "Logical_Constraint5")
model.addConstr(1 <= x[5] + x[3] + x[4], "Logical_Constraint6")

# Optimize the model
model.optimize()

# Print the optimal solution
if model.status == GRB.OPTIMAL:
    print("Optimal objective value: ", model.objVal)
    print("Optimal solution:")
    for i, var in x.items():
        print(f"x{i} = {var.x}")
else:
    print("No solution found.")
