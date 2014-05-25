import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from numpy import array

start_node  = (0,10)
target_node = (15,1)

nodes_with_ones=[]
edgelist_a=[]
edgelist_d=[]
dijkstra_edges=[]
astar_edges=[]

with open('map.txt') as f:
    mapp = []
    for line in f:
        line = line.split() # to deal with blank 
        if line:            # lines (ie skip them)
            line = [int(i) for i in line]
            mapp.append(line)

matx = array(mapp)
matx_len = len(matx)
rows = len(matx)
colms = len(matx[0])

map_rot270 = np.rot90(matx, 3) #rot90(a,b); a-array, b-rotate array 'b' times by 90 deg

#collects all nodes with '1'
for x in range(rows):
    for y in range(colms):
        if map_rot270[x,y]==1:
            nodes_with_ones.append((x,y))

R = nx.grid_2d_graph(rows, colms)
pos=dict(zip(R,R)) # dictionary of node names->positions
node_labels=dict(zip(R,R)) # dictionary of node names->labels
node_labels[(0,10)]='S'
node_labels[(15,1)]='F'

R.remove_nodes_from(nodes_with_ones)

def dist(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

d_path = nx.dijkstra_path(R, start_node, target_node)
print "Dijkstra path: ", d_path

ast_path = nx.astar_path(R, start_node, target_node, dist)
print "Astar path: ", ast_path

def generate_path_a(nodes):
    l = len(nodes)-1
    for x in range(l):
        a = ((ast_path[x]),(ast_path[x+1]))
        edgelist_a.append(a)
    return edgelist_a
def generate_path_d(nodes):
    l = len(nodes)-1
    for x in range(l):
        d = ((d_path[x]),(d_path[x+1]))
        edgelist_d.append(d)
    return edgelist_d

dijkstra_edges = generate_path_d(d_path)
astar_edges = generate_path_a(ast_path)

