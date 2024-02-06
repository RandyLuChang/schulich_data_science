"""
@author: Adam Diamant (2023)
"""

from gurobipy import GRB
import gurobipy as gb

# Linear price response functions (intercept, slope)
snowsuit = [[80, 0.5], [80, 0.5], [30, 0.5], [30, 1.0]]
jacket = [[120, 0.7], [90, 0.9], [80, 1.0], [50, 0.9]]
snowpants = [[50, 0.8], [70, 0.4], [40, 0.4], [10, 0.4]]

# Create a new optimization model to maximize revenue
model = gb.Model("Markdown Optimization")

# Construct the decision variables
p = model.addVars(3,4, lb=0, vtype=GRB.CONTINUOUS, name="Price")
d = model.addVars(3,4, lb=0, vtype=GRB.INTEGER, name="Month Demand")

#Objective Function
model.setObjective(gb.quicksum(p[i,n]*d[i,n] for i in range(3) for n in range(4)), GRB.MAXIMIZE)

# Define the demand constraints
for n in range(4):
    model.addConstr(d[0,n] == snowsuit[n][0] - snowsuit[n][1]*p[0,n], "Demand Definition Snowsuits")
    model.addConstr(d[1,n] == jacket[n][0] - jacket[n][1]*p[1,n], "Demand Definition Jackets")
    model.addConstr(d[2,n] == snowpants[n][0] - snowpants[n][1]*p[2,n], "Demand Definition Snow Pants")

# Demand must not exceed the number we have in stock
model.addConstr(gb.quicksum(d[0,n] + d[1,n] for n in range(4)) <= 160, "Demand Constraint 1")
model.addConstr(gb.quicksum(d[0,n] + d[2,n] for n in range(4)) <= 160, "Demand Constraint 2")
    
# Prices must be marked down month-over-month
model.addConstrs((p[i,n] <= p[i,n-1] for i in range(3) for n in range(1,4)), "Markdown Constraint")
      
# Solve our model
model.optimize()

# Price of snowsuits 
print("Snowsuit Prices from January to April: \n", ['%.2f' % p[0,n].x for n in range(4)])
print("Jacket Prices from January to April: \n", ['%.2f' % p[1,n].x for n in range(4)])
print("Snow Pant Prices from January to April: \n", ['%.2f' % p[2,n].x for n in range(4)])
