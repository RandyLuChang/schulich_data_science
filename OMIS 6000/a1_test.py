import pandas as pd
import numpy as np
from gurobipy import GRB
import gurobipy as gb

# Create the optimization model
model = gb.Model('Can2Oil_Transportation_Optimization')
# Decision variables
## Let x[i, j] denote the amount of canola oil transported directly from production facility i to refinement center j.
## Let y[i, k] denote the amount of canola oil transported from production facility i to transshipment hub k.
## Let z[k, j] denote the amount of canola oil transported from transshipment hub k to refinement center j.

x = model.addVars(25, 5, name="Direct Production Facilities")
y = model.addVars(15, 2, name="Transshipment Production Facilities")
z = model.addVars(2, 5, name="Transshipment Hubs")

direct_prod_capacity_df = pd.read_csv('/Users/changlu/Downloads/Capacity_for_Direct_Production_Facilities.csv')
trans_prod_capacity_df = pd.read_csv('/Users/changlu/Downloads/Capacity_for_Transship_Production_Facilities.csv')
trans_capacity_df = pd.read_csv('/Users/changlu/Downloads/Capacity_for_Transship_Distribution_Centers.csv')
refinement_demand_df = pd.read_csv('/Users/changlu/Downloads/Refinement_Demand.csv')

direct_prod_refinement_cost_df = pd.read_csv('/Users/changlu/Downloads/Cost_Production_to_Refinement.csv')
trans_prod_trans_cost_df = pd.read_csv('/Users/changlu/Downloads/Cost_Production_to_Transshipment.csv')
trans_refinement_cost_df = pd.read_csv('/Users/changlu/Downloads/Cost_Transshipment_to_Refinement.csv')

direct_prod_capacity = direct_prod_capacity_df['Capacity']
trans_prod_capacity = trans_prod_capacity_df['Capacity']
trans_capacity = trans_capacity_df['Capacity']
refinement_demand = refinement_demand_df['Demand']

direct_prod_refinement_cost = [group["Cost"].tolist() for _, group in direct_prod_refinement_cost_df.groupby("ProductionFacility")]
trans_prod_trans_cost = [group["Cost"].tolist() for _, group in trans_prod_trans_cost_df.groupby("ProductionFacility")]
trans_refinement_cost = [group["Cost"].tolist() for _, group in trans_refinement_cost_df.groupby("TransshipmentHub")]


# Constraints

## Capacity constraints for direct production facility
for i in range(25):
    model.addConstr(gb.quicksum(x[i, j] for j in range(5)) <= direct_prod_capacity[i], name=f"Capacity_Constraint_Direct_Production_{i}")

## Capacity constraints for transshipment production facility
for i in range(15):
    model.addConstr(gb.quicksum(y[i, k] for k in range(2)) <= trans_prod_capacity[i], name=f"Capacity_Constraint_Transship_Production_{i}")

## Capacity constraints for transshipment hub
for k in range(2):
    # Flow conservation: Inflow equals outflow
    model.addConstr(gb.quicksum(y[i, k] for i in range(15)) == gb.quicksum(z[k, j] for j in range(5)), name=f"Flow_Conservation_Transship_Hub_{k}")
    
    # Capacity constraint: Inflow does not exceed hub capacity
    model.addConstr(gb.quicksum(y[i, k] for i in range(15)) <= trans_capacity[k], name=f"Capacity_Constraint_Transship_Hub_{k}")

## Demand constraints for refinement centers
for j in range(5):
    model.addConstr(gb.quicksum(x[i, j] for i in range(25)) + gb.quicksum(z[k, j] for k in range(2)) == refinement_demand[j], name=f"Demand_Constraint_Refinement_{j}")
# The objective function
total_cost = gb.quicksum(gb.quicksum(direct_prod_refinement_cost[i][j] * x[i, j] for j in range(5)) for i in range(25)) + \
             gb.quicksum(gb.quicksum(trans_prod_trans_cost[i][k] * y[i, k] for k in range(2)) for i in range(15)) + \
             gb.quicksum(gb.quicksum(trans_refinement_cost[k][j] * z[k, j] for j in range(5)) for k in range(2))

model.setObjective(total_cost, GRB.MINIMIZE)

# Optimally solve the problem
model.optimize()

# Output the results
if model.status == GRB.Status.OPTIMAL:
    print('Optimal Total Transportation Cost:', model.objVal)

    for i, j in x.keys():
        if x[i, j].X > 0:
            print(f"From Production Facility {i} to Refinement Center {j}: {x[i, j].X} units")
    
    for i, k in y.keys():
        if y[i, k].X > 0:
            print(f"From Production Facility {i} to Transshipment Hub {k}: {y[i, k].X} units")

    for k, j in z.keys():
        if z[k, j].X > 0:
            print(f"From Transshipment Hub {k} to Refinement Center {j}: {z[k, j].X} units")
