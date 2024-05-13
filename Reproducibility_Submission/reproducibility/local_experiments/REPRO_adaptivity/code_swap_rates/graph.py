#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 13:16:11 2021

@author: samira
"""
#from structures import *
from filter import *
from combigen import *



def computeMSplacementCosts(projection, combination, partType, sharedDict):
    costs = 0
    print(" computing MS costs for " +str(projection))
    
    ##### FILTERS, append maximal filters
    intercombi = []
    
    automaticFilters = 0
    
    for proj in combination:
        
        if len(proj) > 1 and len(IndexEventNodes[proj]) == 1:     #here a node can only have already all events if the node is a sink for the projection, this case is however already covered in normal placement cost calculation

            automaticFilters +=  getFilters(proj, partType[0]) # TODO first version
        
        intercombi.append(proj)
        if len(proj) > 1 and len(getMaximalFilter(projFilterDict, proj)) > 0:
            for etype in getMaximalFilter(projFilterDict, proj):
                intercombi.append(etype)
    combination = list(set(intercombi))
    
    for myInput in combination:
             # we need a function that computes for all input and then updates eventNode dict         
            if not partType[0] == myInput:
                    costs += NEWcomputeMSplacementCosts([myInput], sharedDict[myInput])
    
    # here we have to generate an instance of etbs per parttype and add one line per instance
    MSManageETBs(projection, partType[0])    
    
    costs -= automaticFilters            
    
    return costs

def getFilters(projection, partType): # move to filter file eventually 
        totalETBs = 0
        for etb in IndexEventNodes[partType]:
            numETBs = 1
            node = getNodes(etb)[0]        
            myETBs = getETBs(node)
            
           
            # jedes etb eines leaftypes von projection, aufsummieren, wenn von jedem mindestens 1 dann aufmultiplizieren und somit etbs ausrechnen und dann rate der etbs aufsummieren pro knoten
            for primEvent in projection.leafs():
                numETBs *= len(list(set(myETBs) & set(IndexEventNodes[primEvent])))
            totalETBs += numETBs
        print("AUTO FILTERS: " + str(totalETBs * projrates[projection][1]))    
        return totalETBs * projrates[projection][1]
    

def NEWcomputeMSplacementCosts(sourcetypes, destinationtypes): #we need tuples, (C, [E,A]) C should be sent to all e and a nodes ([D,E], [A]) d and e should be sent to all a nodes etc
    costs = 0
    destinationNodes = []
    
    for etype in destinationtypes:
        for etb in IndexEventNodes[etype]:
            destinationNodes += getNodes(etb)          
    
    
            
            
    for etype in sourcetypes:  
        print(etype)
        for etb in IndexEventNodes[etype]:
            mycosts = np.Inf
            mytree = nx.Graph()
            for node in getNodes(etb):
                treenodes = copy.deepcopy(destinationNodes)
                treenodes.append(node)
                placementTree = steiner_tree(G, treenodes)
                if len(etype) == 1:
                    curcosts = len(placementTree.edges()) * rates[etype]
                else:
                    
                    num = NumETBsByKey(etb, etype)
                    #curcosts = len(placementTree.edges()) * projrates[etype][1] * num

                    curcosts = len(placementTree.edges()) * projFilterDict[etype][getMaximalFilter(projFilterDict, etype)][0] * num     # FILTER       
                    
                if curcosts < mycosts:
                    mycosts = curcosts
                    mytree = placementTree
            placementTreeDict[(tuple(destinationtypes),etb)] = [node, destinationNodes, mytree]
            costs +=  mycosts 
            
            # update events sent over network
            for routingNode in mytree.nodes():
                if not routingNode in getNodes(etb):
                    setEventNodes(routingNode, etb)
                
                
    return costs              



def ComputeSingleSinkPlacement(projection, combination):
    costs = np.inf
    node = 0
    
    # add filters of projections to eventtpes in combi, if filters added, use costs of filter -> compute costs for single etbs of projrates 
    intercombi = []
    ##### FILTERS
    for proj in combination:
        intercombi.append(proj)
        
        if len(proj) > 1 and len(getMaximalFilter(projFilterDict, proj)) > 0:
            for etype in getMaximalFilter(projFilterDict, proj):
                intercombi.append(etype)
    combination = list(set(intercombi))
    
    for destination in range(len(allPairs)):
        mycosts = 0       
        for eventtype in combination:
            for etb in IndexEventNodes[eventtype]: #check for all sources #here iterated over length of IndesEventNodes to get all sources for etb Instances
                possibleSources = getNodes(etb)
                mySource = possibleSources[0] #??
                for source in possibleSources:
                    if allPairs[destination][source] <= allPairs[destination][mySource]:
                       mySource  = source
                if eventtype in rates.keys():        # case primitive event
                    mycosts += rates[eventtype] * allPairs[destination][mySource]  
                else: # case projection
                     
                     num = NumETBsByKey(etb, eventtype)
                     #mycosts += projrates[eventtype][1] * allPairs[destination][mySource] * num
                     mycosts += projFilterDict[eventtype][getMaximalFilter(projFilterDict, eventtype)][0] * allPairs[destination][mySource] * num 
        if mycosts < costs:
            costs = mycosts
            node = destination
    
    # Update Event Node Matrice, by adding events etbs sent to node through node x to events of node x
    for eventtype in combination:
            for etb in IndexEventNodes[eventtype]:
                possibleSources = getNodes(etb)
                mySource = possibleSources[0] #??
                for source in possibleSources:
                    if allPairs[destination][source] <= allPairs[destination][mySource]:
                       mySource  = source     
                for stop in nx.shortest_path(G, source, node, method='dijkstra'):
                    if not stop in getNodes(etb):
                        setEventNodes(stop, etb)        
    
    # add all etbs to EventNode Matrice and maintain Index
    # for a SingleSinkPlacement we only need a generic ETB AxBxCx
    SiSManageETBs(projection, node)
 
        
    return (costs, node) 


def NEWcomputeCentralCosts(eventtypes):
    costs = np.inf
    node = 0
    for destination in range(len(allPairs)):
        mycosts = 0       
        for eventtype in eventtypes:
            for etb in IndexEventNodes[eventtype]:
                possibleSources = getNodes(etb)
                mySource = possibleSources[0]
                for source in possibleSources:
                    if allPairs[destination][source] <= allPairs[destination][mySource]:
                       mySource  = source
                mycosts += rates[eventtype] * allPairs[destination][mySource]              
        if mycosts < costs:
            costs = mycosts
            node = destination
                        
    return (costs, node) 
                    
        
