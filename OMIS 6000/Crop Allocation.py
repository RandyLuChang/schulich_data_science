"""
@author: Adam Diamant (2023)
"""

from gurobipy import GRB
import gurobipy as gb

# The parameters
oat_yield = 4.25
maize_yield = 3.0
soybean_yield = 20.0

# Number of options
CROPS = 3
PURCHASED = 2
SOLD = 4

# Selling prices
sell = [220, 260, 55, 26]
purchase = [264, 312]

# Create a new optimization model to maximize profit
model = gb.Model("Farming Problem")

# Construct the decision variables.
x = model.addVars(3, lb=0, vtype=GRB.CONTINUOUS, name="Crops")
w = model.addVars(4, lb=0, vtype=GRB.CONTINUOUS, name="Sold")
y = model.addVars(2, lb=0, vtype=GRB.CONTINUOUS, name="Purchased")

# Objective Function
model.setObjective(gb.quicksum(w[i]*sell[i] for i in range(SOLD)) - gb.quicksum(y[i]*purchase[i] for i in range(PURCHASED)), GRB.MAXIMIZE)

# Land capacity constraints 
land_constraint = model.addConstr(x[0] + x[1] + x[2] <= 500, "Land Capacity")

# Cattle feed constraints (oats)
cattle_constraint = model.addConstr(oat_yield*x[0] + y[0] - w[0] >= 200, "Oats")

# Cattle feed constraints (Maize)
oat_constraint = model.addConstr(maize_yield*x[1] + y[1] - w[1] >= 260, "Oats")

# Quota constraints (Soybean)
model.addConstr(w[2] <= 7000, "Quota")
soy_constraint = model.addConstr(w[2] + w[3] == soybean_yield*x[2], "Soybean")

# Solve our model
model.optimize()

# Append the objective function value
print("The optimal solution: ", model.objVal)
    
# Check if the optimization was successful
if model.status == gb.GRB.OPTIMAL:
    # Print the sensitivity analysis for the amount sold
    print("Optimal Amount Sold:")
    print(f"{'Oats'} = {w[0].x, w[0].RC, sell[0], w[0].SAObjUp, w[0].SAObjLow}")
    print(f"{'Maize'} = {w[1].x, w[1].RC, sell[1], w[1].SAObjUp, w[1].SAObjLow}")
    print(f"{'Soybean'} = {w[2].x, w[2].RC, sell[2], w[2].SAObjUp, w[2].SAObjLow}")
    print(f"{'Soybean'} = {w[3].x, w[3].RC, sell[3], w[3].SAObjUp, w[3].SAObjLow}")
else:
    print("Optimization was not successful.")

# Print sensitivity information
print("")
print(f"Sensitivity Information for Land Capacity Constraint {land_constraint.pi:.2f}:")
print("(LHS, RHS, Slack): ", (model.getRow(land_constraint).getValue(), land_constraint.RHS, land_constraint.slack))
print("Shadow Price: ", land_constraint.pi)
print("Range of Feasibility: ", (land_constraint.SARHSUp, land_constraint.SARHSLow))

