"""
@author: Adam Diamant (2023)
"""

from gurobipy import GRB
import gurobipy as gb

# Create the optimization model
model = gb.Model("LG Example")

# Create the three classes of decision variables (type A, B, and C)
a = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="Type A")
b = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="Type B")
c = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="Type C")

# The objective function
model.setObjective(60*a + 75*b + 80*c, GRB.MAXIMIZE)

# Add the constraints
model.addConstr(2*a + 1.5*b + 3*c <= 10000, "Assembly Constraint")
model.addConstr(a + 2*b + c <= 5000, "Package Constraint")

# We could also define these constraints as upper bounds in the definition of the decision variables
model.addConstr(a <= 3000, "Order Limit Constraint (Type A)")
model.addConstr(b <= 2000, "Order Limit Constraint (Type B)")
model.addConstr(c <= 900, "Order Limit Constraint (Type C)")
    
# Optimally solve the problem
model.optimize()

# Number of variables in the model
print("Number of Decision Variables: ", model.numVars)

# The status of the model (Optimization Status Codes)
print("Model Status: ", model.status)

# Print the objective
print(model.ObjVal)

# Print the decision variables
print(model.printAttr('X'))