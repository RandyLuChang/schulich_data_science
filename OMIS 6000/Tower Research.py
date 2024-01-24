"""
@author: Adam Diamant (2023)
"""

from gurobipy import GRB
import gurobipy as gb

# Create the optimization model
model = gb.Model("Tower Research")

# Create the three classes of decision variables where each Python
# variable represents a different number of Gurobi decision variables
I = model.addVars(2, lb=0, vtype=GRB.CONTINUOUS, name="Invest")
B = model.addVars(3, lb=0, vtype=GRB.CONTINUOUS, name="Borrow")
w = model.addVars(4, lb=0, vtype=GRB.CONTINUOUS, name="Wealth")

# The objective function
model.setObjective(w[3], GRB.MAXIMIZE)

# Add the constraints
model.addConstr(w[0] == 4000 + 1000 + B[0] - 1200 - I[0], "Period 1 Constraint")
model.addConstr(w[1] == w[0] + B[1] + 4400 - 1.03*B[0] - 4800 - I[1], "Period 1 Constraint")
model.addConstr(w[2] == w[1] + B[2] + 5800 + 1.02*I[0] - 4212 - 1.03*B[1], "Period 2 Constraint")
model.addConstr(w[3] == w[2] + 3000 + 1.02*I[1] - 1000 - 1.03*B[2], "Period 3 Constraint")

# We could also define these constraints as upper bounds in the definition of the decision variables
for t in range(3):
    model.addConstr(B[t] <= 3000, "Borrowing Constraint %i" % t)

# Optimally solve the problem
model.optimize()

# Number of constraints in the model
print("Number of Constraints: ", model.numConstrs)

# The status of the model
print("Model Status: ", model.status)

# Value of the objective function
print("Total costs: ", model.objVal)

# Print the decision variables
print(model.printAttr('X'))