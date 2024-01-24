"""
@author: Adam Diamant (2023)
"""

from gurobipy import GRB
import gurobipy as gb

# Create the optimization model
model = gb.Model("Transshipment Problem")

# A list of list of costs
source_costs = [[11, 10, 26, 29], [9, 12, 27, 26]]
trans_costs = [[12, 16], [13, 15]]

# Create the a single class of decision variables where
# From = {𝑫𝒂,𝑯𝒐} and To = {𝑪𝒉,𝑳𝑨,𝑺𝑭,𝑵𝒀}.
x = model.addVars(2, 4, lb=0, vtype=GRB.CONTINUOUS, name="Source Nodes")
# From = {𝑪𝒉,𝑳𝑨} and To = {𝑺𝑭,𝑵𝒀}.
y = model.addVars(2, 2, lb=0, vtype=GRB.CONTINUOUS, name="Transshipment Nodes")

# The objective function
source_objective = gb.quicksum(source_costs[i][j]*x[i,j] for i in range(2) for j in range(4))
trans_objective = gb.quicksum(trans_costs[i][j]*y[i,j] for i in range(2) for j in range(2))
model.setObjective(source_objective + trans_objective, GRB.MINIMIZE)

# Add the supply constraints from source nodes
model.addConstr(gb.quicksum(x[0,j] for j in range(4)) <= 200, name="Supply Constraint 1")
model.addConstr(gb.quicksum(x[1,j] for j in range(4)) <= 160, name="Supply Constraint 2")
    
# Add the supply constraints from transshipment nodes
model.addConstr(gb.quicksum(x[i,0] for i in range(2)) <= 90, name="Transship Capacity 1")
model.addConstr(gb.quicksum(x[i,1] for i in range(2)) <= 80, name="Transship Capacity 2")

# Add the flow balance constrainits
model.addConstr(gb.quicksum(x[i,0] for i in range(2)) == gb.quicksum(y[0,k] for k in range(2)), name="Flow Balance 1")
model.addConstr(gb.quicksum(x[i,1] for i in range(2)) == gb.quicksum(y[1,k] for k in range(2)), name="Flow Balance 2")

# Add the demand constraints
model.addConstr(gb.quicksum(x[i,2] + y[i,0] for i in range(2)) == 140, name="Demand Constraint 1")
model.addConstr(gb.quicksum(x[i,3] + y[i,1] for i in range(2)) == 140, name="Demand Constraint 2")

# Ratio constraint
model.addConstr(0.6*gb.quicksum(y[i,j] for i in range(2) for j in range(2)) <= 0.4*gb.quicksum(x[i,j] for i in range(2) for j in range(2,4)), name="Ratio constraint")

# Optimally solve the problem
model.optimize()

# Number of variables in the model
print("Number of Decision Variables: ", model.numVars)

# Value of the objective function
print("Total Transportation cost: ", model.objVal)

# Print the decision variables
print(model.printAttr('X'))