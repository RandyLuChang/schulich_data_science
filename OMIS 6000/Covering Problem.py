"""
@author: Adam Diamant (2023)
"""

import gurobipy as gb
from gurobipy import GRB

# Create a new model
model = gb.Model("Covering Problem")

# Variables
x = model.addVars(16, vtype=GRB.BINARY, name="Region")

# Objective function
objective = gb.quicksum(x[i] for i in range(16))
model.setObjective(objective, GRB.MINIMIZE)

# Constraints
model.addConstr(x[0] + x[1] + x[3] + x[4] >= 1, "Covering 1")
model.addConstr(x[0] + x[1] + x[2] + x[4] + x[5] >= 1, "Covering 2")
model.addConstr(x[1] + x[2] + x[5] + x[6] >= 1, "Covering 3")
model.addConstr(x[0] + x[3] + x[4] + x[7] + x[9] + x[10] >= 1, "Covering 4")
model.addConstr(x[0] + x[1] + x[3] + x[4] + x[5] + x[7] >= 1, "Covering 5")
model.addConstr(x[1] + x[2] + x[4] + x[5] + x[6] + x[7] + x[8] >= 1, "Covering 6")
model.addConstr(x[2] + x[5] + x[6] + x[8] + x[12] >= 1, "Covering 7")
model.addConstr(x[3] + x[4] + x[5] + x[7] + x[8] + x[10] + x[11] >= 1, "Covering 8")
model.addConstr(x[5] + x[6] + x[7] + x[8] + x[11] + x[12] >= 1, "Covering 9")
model.addConstr(x[3] + x[9] + x[10] + x[13] >= 1, "Covering 10")
model.addConstr(x[3] + x[7] + x[9] + x[10] + x[11] + x[13] >= 1, "Covering 11")
model.addConstr(x[7] + x[8] + x[10] + x[11] + x[12] + x[14] >= 1, "Covering 12")
model.addConstr(x[6] + x[8] + x[11] + x[12] + x[14] + x[15] >= 1, "Covering 13")
model.addConstr(x[9] + x[10] + x[13] + x[14] >= 1, "Covering 14")
model.addConstr(x[11] + x[12] + x[13] + x[14] + x[15] >= 1, "Covering 15")
model.addConstr(x[12] + x[14] + x[15] >= 1, "Covering 16")

# Optimize the model
model.optimize()

# Print the optimal solution
if model.status == GRB.OPTIMAL:
    print("Optimal solution:")
    for i, var in x.items():
        print(f"x{i} = {var.x}")
    
    print("Number of Fire Stations", model.ObjVal)
else:
    print("No solution found.")
