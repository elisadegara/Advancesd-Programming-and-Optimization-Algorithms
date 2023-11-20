import numpy as np
import networkx as nx



def comp_dist(file1, file2):
    # OPEN THE TWO FILES AND TRANSFORM THEM INTO 2 MATRICES
    with open(file1, 'r') as f1:
        rows = f1.readlines()
    F1 = []
    for row in rows:
        row = [int(digit) for digit in row.strip()]
        F1.append(row)
    F1 = np.array(F1, dtype=object)
    

    with open(file2, 'r') as f2:
        rows = f2.readlines()
    F2 = []
    for row in rows:
        row = [int(digit) for digit in row.strip()]
        F2.append(row)
    F2 = np.array(F2, dtype=object)

    # NORMALIZE MATRICES TO HAVE EQUAL TOTALE DEMAND FOR EVERY FILE
    s1 = 0
    for i in range(10):
        for j in range(80):
            s1 = s1 + F1[i][j]
    s2 = 0
    for i in range(10):
        for j in range(80):
            s2 = s2 + F2[i][j]
    if s1 == s2:
        for i in range(10):
            for j in range(80):
                F1[i][j] = F1[i][j] * s1 * 39
                F2[i][j] = F2[i][j] * s1 * 39
    else:
       for i in range(10):
            for j in range(80):
                F1[i][j] = F1[i][j] * s2 * s1
                F2[i][j] = F2[i][j] * s1 * s1      


    # CREATE THE GRAPH
    G = nx.DiGraph()

    # add source
    G.add_node('source', demand = -5000000000)

    # add sink
    G.add_node('sink', demand = 5000000000)

   # add nodes of the first picture
    for i in range(10):
        for j in range(80):
            G.add_node(f'F1_({i}, {j})', demand = -F1[i][j])

    # add nodes of the second picture
    for i in range(10):
        for j in range(80):
            G.add_node(f'F2_({i}, {j})', demand = F2[i][j])

    # add edges from source to nodes of first picture
    for i in range(10):
        for j in range(80):
            G.add_edge('source', f'F1_({i}, {j})')

    # add edges from nodes of first picture to nodes of the second one    
    for i in range(10):
        for j in range(80):
            for k in range(10):
                for h in range(80):
                    if G.nodes[f'F1_({i}, {j})']['demand'] != 0:
                        if h >= j:
                            w = np.abs(h-j)
                        else:
                            w = np.abs(90-j+h)
                        G.add_edge(f'F1_({i}, {j})', f'F2_({k}, {h})', weight = w)
    
    # add edges for nodes of second picture to sink
    for i in range(10):
        for j in range(80):
            G.add_edge(f'F2_({i}, {j})', 'sink')

    distance = nx.min_cost_flow_cost(G)
    return float(distance)




def sort_files():
    files = ['P1.txt', 'P2.txt', 'P3.txt', 'P4.txt', 'P5.txt', 'P6.txt', 'P7.txt', 'P8.txt', 'P9.txt', 'P10.txt', 'P11.txt', 'P12.txt', 'P13.txt', 'P14.txt', 'P15.txt']
    temp = {}
    for i in range(2, 16):
        dist = comp_dist('P1.txt', f'P{i}.txt')
        temp[f'P{i}.txt'] = dist

    sorted_files = ['P1.txt']

    sorted_dict = dict(sorted(temp.items(), key=lambda item: item[1]))
    for x in sorted_dict.keys():
        sorted_files.append(x)

    return sorted_files

print(sort_files())