import pulp
from pulp import *

retval = {}
retval['obj'] = None
retval['x1'] = None
# there should be retval['xi'] for each company number i


file = open('hw1-03.txt', 'r')
a = []
for row in file:
    a.append([int(x) for x in row.split()])

model = LpProblem("Minimization", LpMinimize)

i = []
for x in range(1,70):
    i.append(x)

variables = LpVariable.dicts('x', indexs=i, lowBound=0.0, upBound=None, cat='Continuous')


model += sum(x for x in variables.values())

for i in range(len(a)):
    model += (variables[a[i][0]] + variables[a[i][1]]) >= 2

model.solve()

for i in range(1, 70):
    retval[f'x{i}'] = variables[i].varValue

retval['obj'] = value(model.objective)

print(retval)