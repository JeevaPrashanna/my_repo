import pandas as pd
from pulp import *
import math

df = pd.read_csv("data.csv")  # Read the csv file

""" Loop to find the number of products and product names in csv file"""
productCounter = 0
productList = []
for i in df.columns:
    if i.startswith('P'):
        productCounter += 1
        productList.append(i)

"""Loop to get number of machines from csv file"""
machineCounter = 0
for i in df['Ma / Pd']:
    if type(i) == float:
        if math.isnan(i):
            break
    else:
        machineCounter += 1


m = 1  # var to initialise the value
machines = list(df['Ma / Pd'])[0:machineCounter]  # List containing name of all machines

productTime = []  # Contains product time
for i in range(0, len(machines)):
    productTime.append(dict(zip(productList, df.iloc[i][m:productCounter + 1].fillna(0))))

capacity = dict(zip(machines, df['Max capacity']))  # Contains capacity of machines
demand = dict(zip(productList, df.iloc[22][m:productCounter+1]))  # Contains demand list of products
profit = dict(zip(productList, df.iloc[19][m:productCounter+1]))  # Contains profits of each product

"""---------------CONSTRAINTS---------------"""

model = LpProblem("Problem", LpMaximize)  # Initialise model
varCells = LpVariable.dicts('', productList, lowBound=0, cat='Continuous')  # Declare Variable cells

capacityIterator = iter(list(capacity.values()))  # Iter function to iterate over the capacity

model += lpSum([profit[i] * varCells[i] for i in productList]), "Objective Function"

for j in productTime:
    model += lpSum([j[i] * varCells[i] for i in productList]) <= next(capacityIterator)  # Capacity Constraint

for i in productList:
    model += lpSum(varCells[i]) <= demand[i]  # Maximum product Constraint

for i in productList:
    model += lpSum(varCells[i]) >= 0  # Minimum product constraint

model.solve()

print("Status:", LpStatus[model.status])

"""Loop to add product quantities to find profit"""
optimalProductQuantity = {}
for v in model.variables():
    optimalProductQuantity[v.name.replace('_', '')] = v.varValue

maxProfit = 0
for i in productList:
    maxProfit += profit[i] * optimalProductQuantity[i]

"""Printing optimal quantities"""
quantities = []
for v in model.variables():
    quantities.append(v.varValue)

producingQuantities = dict(zip(productList, quantities))
print(pd.DataFrame.from_dict(optimalProductQuantity, orient='index', columns=['Qty']))
print(f"Maximum Profit: {maxProfit}")
