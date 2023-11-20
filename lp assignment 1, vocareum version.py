import pulp
from pulp import *

retval = {}
retval["x"] = None
retval["y"] = None
retval["obj"] = None
retval["tight_constraints"] = [ None ]


model = LpProblem("Minimization", LpMinimize)

x = LpVariable("x", -10, None) 
y = LpVariable("y", None, 10)

model += 122*x + 143*y

model += x >= -10
model += y <= 10
model += 3*x + 2*y <= 10
model += 12*x + 14*y >= -12.5
model += 2*x + 3*y >= 3
model += 5*x - 6*y >= -100

model.solve()


retval["x"] = x.varValue
retval["y"] = y.varValue
retval["obj"] = value(model.objective)
    
i = 1
if (x.varValue == -10):
    retval["tight_constraints"] = []
    retval["tight_constraints"].append(i)
i += 1
if (y.varValue == 10):
    if retval["tight_constraints"] == [ None ]:
        retval["tight_constraints"] = []
    retval["tight_constraints"].append(i)
i += 1
if (3*x.varValue + 2*y.varValue == 10):
    if retval["tight_constraints"] == [ None ]:
        retval["tight_constraints"] = []
    retval["tight_constraints"].append(i)
i += 1
if (12*x.varValue + 14*y.varValue == -12.5):
    if retval["tight_constraints"] == [ None ]:
        retval["tight_constraints"] = []
    retval["tight_constraints"].append(i)
i += 1
if (2*x.varValue + 3*y.varValue == 3):
    if retval["tight_constraints"] == [ None ]:
        retval["tight_constraints"] = []
    retval["tight_constraints"].append(i)
i += 1
if (5*x.varValue  - 6*y.varValue == -100):
    if retval["tight_constraints"] == [ None ]:
        retval["tight_constraints"] = []
    retval["tight_constraints"].append(i)

print(retval.values())