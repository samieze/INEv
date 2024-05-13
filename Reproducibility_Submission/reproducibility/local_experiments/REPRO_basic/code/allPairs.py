#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 17:01:50 2021

@author: samira

Initialize all pair shortest paths for graph.

"""

import multiprocessing
import networkx as nx 
import pickle
import time
import numpy as np
import random as rd 

with open('graph',  'rb') as graph_file:
    G = pickle.load(graph_file)


myNodes = list(G.nodes)
allPairs = [[] for x in myNodes]

def fillMyMatrice(me):  
    myDistances = []
    for j in range(len(G.nodes)):            
           myDistances.append(len(nx.shortest_path(G, me, j, method='dijkstra')) - 1)   
    return (me, myDistances)

pool = multiprocessing.Pool()
         


start = time.time()
result = pool.map(fillMyMatrice, myNodes)
for i in result:
    allPairs[i[0]] = i[1]
end = time.time()


print("All Pairs " + str(end-start))


with open('allPairs', 'wb') as allPairs_file:
          pickle.dump(allPairs,allPairs_file)      
          
