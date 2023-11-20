# Import packages. You can import additional packages, if you want
# You can change the way they are imported, e.g import pulp as pl or whatever
# But take care to adapt the solver configuration accordingly.
from pulp import *
import matplotlib.pyplot as plt

# Use the following solver
solver = COIN_CMD(path="/usr/bin/cbc",threads=8)
# at home, you can try it with different solvers, e.g. GLPK, or with a different
# number of threads.
# WARNING: your code when run in vocareum should finish within 10 minutes!!!

def bakery():
    # Input file is called ./bakery.txt
    input_filename = './bakery.txt'

    # Use solver defined above as a parameter of .solve() method.
    # e.g., if your LpProblem is called prob, then run
    # prob.solve(solver) to solve it.
 
    # SOLVE THE PROBLEM
    
    # open file and create three lists for preparation times, deadlines and baking times
    with open(input_filename, 'r') as f:
        B = []
        for row in f:
            B.append([int(x) for x in row.split()])

    n = 17

    PRE = []
    for i in range(n):
        PRE.append(B[i][1])

    DLN = []
    for i in range(n):
        DLN.append(B[i][2])

    BAK = []
    for i in range(n):
        BAK.append(B[i][3])
        

    # define big-M as maximum deadline + 1
    M = 0
    for x in DLN:
        if x > M:
            M = x
    M += 1


    # define the problem
    problem = LpProblem("Bakery_orders", LpMinimize)

    s = [LpVariable(f"s{i}", lowBound=0, cat='Integer') for i in range(n)]  # starting times
    x = [[LpVariable(f"x{i}_{j}", cat='Binary') for i in range(n)] for j in range(n)] # x[i][j] = 1 if pastry i is baked before pastry j, and 0 otherwise
    T = LpVariable("T", cat='Continuous') # maximum ending time

    problem += T

    for i in range(n):
        problem += T >= s[i] + BAK[i]             # maximum ending time >= any ending time
        problem += s[i] >= PRE[i]                 # any starting time >= any preparation time
        problem += DLN[i] >= s[i] + BAK[i]        # any deadline >= any ending time

    for i in range(n):
        for j in range(n):
            if j>i:
                problem += s[i] + BAK[i] <= s[j] + M*(1 - x[i][j])
                problem += s[j] + BAK[j] <= s[i] + M*(x[i][j])          # big-M method to ensure ei <= sj or ej <= si


    problem.solve(solver)



    retval = {}
    for i in range(n):
        retval[f's_{i}'] = s[i].value()
        
    l = {}
    for i in range(n):
        l[i] = (s[i].value(), s[i].value() + BAK[i])

    sorted_l = dict(sorted(l.items(), key=lambda item: item[1]))
    start_times = [time[0] for time in sorted_l.values()]
    end_times = [time[1] for time in sorted_l.values()]
    pastries = list(sorted_l.keys())
  
    sorted_dln = []
    sorted_pre = []

    for i in pastries:
        sorted_dln.append(DLN[i])
        sorted_pre.append(PRE[i])
    
    # PLOT THE RESULT
    
    # Define task names: sorted list of pastries (based on starting times)
    tasks = []
    for x in pastries:
        tasks.append(f'P.{x}')

    # Define colors
    colors = []
    for i in range(n):
        if sorted_dln[i] == end_times[i]:
            colors.append('red')                   # critical preparation (when ending time == deadline)
        else:
            colors.append('mediumblue')


    # Define oven opening times and pastry movements
    oven_openings = [int(s) for s in start_times]
    for i in range(n):
        if end_times[i] not in oven_openings:
            oven_openings.append(int(end_times[i]))
        if DLN[i] not in oven_openings:
            oven_openings.append(DLN[i])
        if PRE[i] not in oven_openings:
            oven_openings.append(PRE[i])

    # Create Gantt chart
    fig, gnt = plt.subplots(figsize=(10, 5))

    # Set chart title and x-axis and y-axis label
    gnt.set_title("Bakery Schedule")
    gnt.set_xlabel("Time (min)")
    gnt.set_ylabel("Pastry")
    gnt.grid(True)

    # Add tasks to the chart
    for i, task in enumerate(tasks):
        gnt.broken_barh([(start_times[i]//60, (end_times[i]-start_times[i])//60)], (2*i, 1), facecolors=colors[i])
        gnt.broken_barh([(end_times[i]//60, (sorted_dln[i] - end_times[i])//60)], (2*i, 1), facecolors='lightpink')
        gnt.broken_barh([(sorted_pre[i]//60, (start_times[i] - sorted_pre[i])//60)], (2*i, 1), facecolors='lightgreen')

    # Set x-axis limits and ticks
    gnt.set_xlim(0, (M+5)//60)
    gnt.set_xticks([t//60 for t in oven_openings])
    gnt.set_xticklabels([f'{t//60}' for t in oven_openings], rotation = 90)

    y_pos = []
    for i in range(n):
        y_pos.append(2*i+0.5)
    plt.yticks(y_pos, tasks)


    w = ['critical baking (end of baking = deadline)', 'non-critical baking', 'from end of preparation to start of baking', 'from end of baking to deadline']
    col = ['red', 'mediumblue', 'lightgreen', 'lightpink']
    legend_handles = [plt.Rectangle((0,0), 1, 1, fc=c) for c in col]
    gnt.legend(legend_handles, w, loc = (0.68, 0.15), fontsize = 'x-small')
    
    # Write visualization to the correct file:
    visualization_filename = './visualization.png'
    
    plt.savefig(visualization_filename)

    # retval should be a dictionary such that retval['s_i'] is the starting
    # time of pastry i
    return retval
