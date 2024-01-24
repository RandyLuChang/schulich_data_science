"""
@author: Adam Diamant (2023)
"""

import gurobipy as gb

# Create a new optimization model for the dual problem
model = gb.Model("Dual Problem")

# Dual variables
y1 = model.addVar(lb=0, vtype=gb.GRB.CONTINUOUS, name="y1")
y2 = model.addVar(lb=0, vtype=gb.GRB.CONTINUOUS, name="y2")
y3 = model.addVar(lb=0, vtype=gb.GRB.CONTINUOUS, name="y3")

# Set the objective function to minimize
model.setObjective(4*y1 + 13*y2 + 31*y3, gb.GRB.MINIMIZE)

# Add constraints
dual_constraint1 = model.addConstr(y1 + y2 + 5*y3 >= 5, "Dual_Constraint1")
dual_constraint2 = model.addConstr(2*y2 + 3*y3 >= 4, "Dual_Constraint2")

# Optimize the dual model
model.optimize()

# Check if the optimization was successful
if model.status == gb.GRB.OPTIMAL:
    # Get the optimal solution and objective value for the dual problem
    optimal_y1 = y1.x
    optimal_y2 = y2.x
    optimal_y3 = y3.x
    optimal_dual_objective_value = model.objVal

    # Print the results
    print("Optimal Dual Solution:")
    print(f"y1 = {optimal_y1}")
    print(f"y2 = {optimal_y2}")
    print(f"y3 = {optimal_y3}")
    print("Optimal Dual Objective Value:")
    print(f"Dual z = {optimal_dual_objective_value}")
    
    # These should equal the optimal solution to the primal problem
    print("Shadow Prices: ", (dual_constraint1.pi, dual_constraint2.pi))
else:
    print("No feasible solution found for the dual problem.")
