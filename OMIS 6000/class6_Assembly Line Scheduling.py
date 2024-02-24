"""
@author: Adam Diamant (2023)
"""

import gurobipy as gb
from gurobipy import GRB

# Create a new model
model = gb.Model("Assembly Line Scheduling ")

# Variables
x = model.addVars(7, lb=0, vtype=GRB.INTEGER, name="Shift Variable")

# Objective function
objective = 680 * x[0] + 705 * x[1] + 705 * x[2] + 705 * x[3] + 705 * x[4] + 680 * x[5] + 655 * x[6]
model.setObjective(objective, GRB.MINIMIZE)

# Constraints
model.addConstr(x[2] + x[3] + x[4] + x[5] + x[6] >= 27, "Monday_Constraint")
model.addConstr(x[3] + x[4] + x[5] + x[6] + x[0] >= 22, "Tuesday_Constraint")
model.addConstr(x[4] + x[5] + x[6] + x[0] + x[1] >= 26, "Wednesday_Constraint")
model.addConstr(x[5] + x[6] + x[0] + x[1] + x[2] >= 25, "Thursday_Constraint")
model.addConstr(x[6] + x[0] + x[1] + x[2] + x[3] >= 21, "Friday_Constraint")
model.addConstr(x[0] + x[1] + x[2] + x[3] + x[4] >= 19, "Saturday_Constraint")
model.addConstr(x[1] + x[2] + x[3] + x[4] + x[5] >= 18, "Sunday_Constraint")

# Optimize the model
model.optimize()

# Print the optimal solution
if model.status == GRB.OPTIMAL:       
    print("Total Cost", model.ObjVal)          
    # Print the LHS of the constraints
    constraints = model.getConstrs()
    for con in constraints:
        print(f"LHS = {model.getRow(con).getValue()}, {con.RHS} = RHS")
    
else:
    print("No solution found.")
