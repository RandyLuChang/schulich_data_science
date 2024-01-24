"""
@author: Adam Diamant (2023)
"""

import gurobipy as gb

# Create a new optimization model
model = gb.Model("Primal Problem")

# Decision variables
x1 = model.addVar(lb=0, vtype=gb.GRB.CONTINUOUS, name="x1")
x2 = model.addVar(lb=0, vtype=gb.GRB.CONTINUOUS, name="x2")

# Set the objective function to maximize
model.setObjective(5*x1 + 4*x2, gb.GRB.MAXIMIZE)

# Add constraints
constraint1 = model.addConstr(x1 <= 4, "Constraint1")
constraint2 = model.addConstr(x1 + 2*x2 <= 13, "Constraint2")
constraint3 = model.addConstr(5*x1 + 3*x2 <= 31, "Constraint3")

# Optimize the model
model.optimize()

# Check if the optimization was successful
if model.status == gb.GRB.OPTIMAL:
    # Get the optimal solution and objective value
    optimal_x1 = x1.x
    optimal_x2 = x2.x
    optimal_objective_value = model.objVal

    # Print the results
    print("Optimal Solution:")
    print(f"x1 = {optimal_x1}")
    print(f"x2 = {optimal_x2}")
    print("Optimal Objective Value:")
    print(f"z = {optimal_objective_value}")
    
    # These should equal the optimal solution to the dual problem
    print("Shadow Prices: ", (constraint1.pi, constraint2.pi, constraint3.pi))
else:
    print("No feasible solution found.")


