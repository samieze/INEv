#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 11:45:00 2021

@author: samira
"""
from util import *

from network import *
import copy
import numpy as np
import pickle
from tree import *
from helper import *
from parse_network import *
from network import *

import matplotlib.pyplot as plt
import networkx as nx 
from networkx.algorithms.approximation import steiner_tree
from networkx.algorithms.components import is_connected
from EvaluationPlan import *
import time
import numpy as np
#G = nx.Graph()

with open("allPairs", "rb") as allPairs_file:
    allPairs = pickle.load(allPairs_file)

with open('graph',  'rb') as graph_file:
    G = pickle.load(graph_file)
ETB = {} # {"A": {"A1": [2,3], "A3" = [3]}, "B" {"B1:[1,3]} ....}
placementTreeDict = {} # {("D", "A1"): (5,[2,3,4], steinerTree(5234)} show steiner tree to connect all D's with A1 -> problem: what about multiple recipient event types? what about single sink placements=
eventNodeDict =  {} # {0: ["B1", "A3", "E0"], 1: ["A1B2", "A1B3", "B1"]} which instances of events/projections are generated or sent to/via node x -> maybe reuse network dict, but atm used for other stuff


def initEventNodes():  #matrice: comlumn indices are node ids, row indices correspond to etbs, for a given etb use IndexEventNodes to get row ID for given ETB
    myEventNodes = []
    myIndexEventNodes = {}
    offset = 0
    index = 0 
    for etype in nodes.keys():
        myetbs = []
        for node in nodes[etype]:
            
            mylist = [0 for x in range(len(network.keys()))]
            mylist[node] = 1
            myEventNodes.append(mylist)
            myIndexEventNodes[etype+str(node)] = index
            index += 1
            myetbs.append(etype+str(node))
        myIndexEventNodes[etype] = myetbs
        offset = index
    return(myEventNodes, myIndexEventNodes)
        
EventNodes = initEventNodes()[0]
IndexEventNodes = initEventNodes()[1]
projFilterDict = {}


def getETBs(node):
    mylist = column1s(column(EventNodes, node))       
    return [list(IndexEventNodes.keys())[list(IndexEventNodes.values()).index(x)] for x in mylist] # index from row id <-> etb

def getNodes(etb):
    return column1s(EventNodes[IndexEventNodes[etb]])

def setEventNodes(node, etb):
    EventNodes[IndexEventNodes[etb]][node] = 1
 
def unsetEventNodes(node, etb):
    EventNodes[IndexEventNodes[etb]][node] = 0    
    
def addETB(etb, etype):
    mylist = [0 for x in range(len(network.keys()))]
    EventNodes.append(mylist)
    index = len(EventNodes)-1
    IndexEventNodes[etb] = index
    if not etype in IndexEventNodes:
        IndexEventNodes[etype] = [etb]
    else:
        IndexEventNodes[etype].append(etb)
    
def SiSManageETBs(projection, node):
    etbID = genericETB("", projection)[0]
    addETB(etbID, projection)           
    setEventNodes(node, etbID)       

def MSManageETBs(projection, parttype):
    etbIDs = genericETB(parttype, projection)
    for projectionETB in etbIDs:
             addETB(projectionETB, projection)             
    for i in range(len(nodes[parttype])):
        setEventNodes(nodes[parttype][i], etbIDs[i])          


def genericETB(partType, projection):
    ETBs = []   
    if len(partType) == 0 or not partType in projection.leafs():
        myID = ""
        for etype in projection.leafs():
            myID += etype
        ETBs.append(myID)
    else:
        for node in nodes[partType]:   
            myID = ""
            for etype in projection.leafs():
                myID += etype
                if etype == partType:
                    myID += str(node)
            ETBs.append(myID)
    return ETBs

def getNumETBs(projection):
    num = 1
    for etype in projection.leafs():
        num *= len(IndexEventNodes[etype])
    return num

def NumETBsByKey(etb, projection):
    instancedEvents = []
    index = 0
    for i in range(1, len(etb)):       
        if not etb[i] in projection.leafs() and etb[index] in projection.leafs() and not etb[index] in instancedEvents:
            instancedEvents.append(etb[index])
        elif etb[i] in projection.leafs():
            index = i
    
    num = getNumETBs(projection)
    for etype in instancedEvents:
        num = num / len(IndexEventNodes[etype])
    return num

def getLongest():
    #Take average over all  
    avs  = []
    for i in allPairs:
        avs.append(np.average(i))
    return np.median(avs)
    #return max([max(x) for x in allPairs])


longestPath = getLongest()
maxDist = max(sum(allPairs,[]))

#print(longestPath)
# G = nx.watts_strogatz_graph(len(nw),2,0.8) # gen topologie -> load from file...
# while not is_connected(G):
#     G = nx.watts_strogatz_graph(len(nw),2,0.8)
#nx.draw(G, with_labels=True, font_weight='bold')
#plt.show()  
   
