"""
@author: Adam Diamant (2023)
"""

from gurobipy import GRB
import gurobipy as gb


# Maximum difference between inventory positions of the warehouses 
max_diff = 1200

# The supply nodes (i.e., the warehouses)
W = 2

# Creates a list that has the number of units of supply for each supply node
supply = [7000, 8000]

# The demand nodes
B = 7

# Creates a list for the number of units of demand for each demand node
demand = [1000, 1800, 3600, 400, 1400, 2500, 2000]

# Creates a list of lists associated with the costs of each transportation path.
# From warehouse i = {A,B} to bar j = {1,2,3,4,5,6,7}. 
costs = [
         #Bars: 1 2 3 4 5 6 7
         [2.00,4.00,5.00,2.00,1.00,2.50,1.90],#A   Warehouses
         [3.00,1.00,3.00,2.00,3.00,1.75,1.60] #B
        ]

# Instantiate our optimization problem in
model = gb.Model("Linearize Absolute Value Constraint")

#Construct decision variables for each class of decision variables
x = model.addVars(W, B, lb = 0, vtype=GRB.INTEGER, name="Transportation")

# Add the objective function to the optimization problem 
model.setObjective(gb.quicksum(x[w,b]*costs[w][b] for w in range(W) for b in range(B)), GRB.MINIMIZE)

# The demand minimum constraints are added to the milp variable for each demand node (bar)
model.addConstrs(gb.quicksum(x[w,b] for w in range(W)) == demand[b] for b in range(B))

# The supply maximum constraints are added to the milp variable for each supply node (warehouse)
model.addConstrs(gb.quicksum(x[w,b] for b in range(B)) <= supply[w] for w in range(W))
                   
# The absolute value of the difference in the inventory supplied to the bars
# model.addConstr(abs(gb.quicksum(x[0,b] for b in range(B)) - gb.quicksum(x[1,b] for b in range(B)))  <= max_diff)
model.addConstr(gb.quicksum(x[0,b] for b in range(B)) - gb.quicksum(x[1,b] for b in range(B))  <= max_diff)
model.addConstr(gb.quicksum(x[1,b] for b in range(B)) - gb.quicksum(x[0,b] for b in range(B))  <= max_diff)

# Optimally solve the problem
model.optimize()

# Each of the variables is printed with it's resolved optimum value
total_supply = [0,0]
for v in model.getVars():    
    if ("[0," in v.varName):
        total_supply[0] += v.x
    else: 
        total_supply[1] += v.x

# The optimized objective function value is printed to the screen    
print("Total Cost of Transportation = ", model.objVal)
print("Supply from Warehouse A = ", total_supply[0])
print("Supply from Warehouse B = ", total_supply[1])
print("Supply Difference = ", abs(total_supply[0]-total_supply[1]))