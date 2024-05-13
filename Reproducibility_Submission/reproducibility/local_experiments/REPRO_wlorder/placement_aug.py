#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 13:16:11 2021

@author: samira
"""
import multiprocessing
from processCombination_aug import *
from functools import partial


def computeMSplacementCosts(projection, combination, partType, sharedDict, noFilter):
    costs = 0
    Filters  = []
    
    ##### FILTERS, append maximal filters
    intercombi = []
    
    automaticFilters = 0
    for proj in combination:
        #if len(proj) > 1 and len(IndexEventNodes[proj]) == 1:     #here a node can only have already ALL events if the node is a sink for the projection, this case is however already covered in normal placement cost calculation
            # automaticFilters +=  getFilters(proj, partType[0]) # TODO first version
            
        intercombi.append(proj)
        if len(proj) > 1 and len(getMaximalFilter(projFilterDict, proj, noFilter)) > 0: # those are the extra events that need to be sent around due to filters
            Filters.append((proj,getMaximalFilter(projFilterDict, proj, noFilter) ))
            #print("Using Filter: " + str(getMaximalFilter(projFilterDict, proj)) + ": " + str(projFilterDict[proj][getMaximalFilter(projFilterDict, proj)][0]) + " instead of " + str(projrates[proj])  )
            for etype in getMaximalFilter(projFilterDict, proj, noFilter):
                intercombi.append(etype)
    combination = list(set(intercombi))
    myPathLength = 0
  
    totalInstances = [] #!
    myNodes = [] #!
    
    for i in IndexEventNodes[partType[0]]: #!
        myNodes += getNodes(i) #!
        
    myProjection = Projection(projection, {}, myNodes, [], Filters) #!
    for myInput in combination:
            if not partType[0] == myInput:
                    if myInput in sharedDict.keys():                         
                        #result = NEWcomputeMSplacementCosts_Path(projection, [myInput], sharedDict[myInput], noFilter)
                        result = NEWcomputeMSplacementCosts(projection, [myInput], sharedDict[myInput], noFilter)
                        costs +=  result[0] #fix SharedDict with Filter Inputs
                        
                    else:
                        #result = NEWcomputeMSplacementCosts_Path(projection, [myInput],  partType[0], noFilter) 
                        result = NEWcomputeMSplacementCosts(projection, [myInput],  partType[0], noFilter) 

                        costs +=  result[0]
                    if result[1] > myPathLength:
                        myPathLength = result[1]
                    
                    myProjection.addInstances(myInput, result[2]) #!
                    totalInstances += result[2] #!
            else:
                myInstances = [Instance(partType[0], partType[0], nodes[partType[0]], {})]
                myProjection.addInstances(partType[0], myInstances)
                    
    # here generate an instance of etbs per parttype and add one line per instance
    MSManageETBs(projection, partType[0])    
    
    spawnedInstances = IndexEventNodes[projection]
    myProjection.addSpawned(spawnedInstances)
    
    
    costs -= automaticFilters            
    
    return costs, myPathLength, myProjection, totalInstances, Filters

def getFilters(projection, partType): # move to filter file eventually 
        totalETBs = 0
        for etb in IndexEventNodes[partType]: #for each multi-sink
            
                numETBs = 1
                node = getNodes(etb)[0]        
                myETBs = getETBs(node)       
                if not set(IndexEventNodes[projection]).issubset(set(getETBs(node))): # it is  checked if the node already received all etbs of the projection, if this is the case its not necessary to reduce something here     
                    # jedes etb eines leaftypes von projection, aufsummieren, wenn von jedem mindestens 1 dann aufmultiplizieren und somit etbs ausrechnen und dann rate der etbs aufsummieren pro knoten
                    for primEvent in projection.leafs():
                        numETBs *= len(list(set(myETBs) & set(IndexEventNodes[primEvent])))
                       
                    totalETBs += numETBs
      #  print("AUTO FILTERS: " + str(totalETBs * projrates[projection][1]))    # if the projection is also input to another projection in the combination, it may also be the case that the nodes of the parttypes already received all instances of the projections, hence filters can't help anymore...
        return totalETBs * projrates[projection][1]
    

def NEWcomputeMSplacementCosts(projection, sourcetypes, destinationtypes, noFilter): #we need tuples, (C, [E,A]) C should be sent to all e and a nodes ([D,E], [A]) d and e should be sent to all a nodes etc
    #print(projection, sourcetypes)
    costs = 0
    destinationNodes = []     

    for etype in destinationtypes:
        for etb in IndexEventNodes[etype]:
            destinationNodes += getNodes(etb)
            
            
    newInstances = [] #!
    pathLength = 0        
    etype = sourcetypes[0]
    
    f = open("msFilter.txt", "w")
    if etype in projFilterDict.keys() and getMaximalFilter(projFilterDict, etype, noFilter):
        print("hasFilter")
        f.write("VAR=true")
    else:        
        f.write("VAR=false")
    f.close()     
        
        
    for etb in IndexEventNodes[etype]: #parallelize         
            MydestinationNodes = list(set(destinationNodes).difference(set(getNodes(etb)))) #only consider nodes that do not already hold etb
            if MydestinationNodes: #are there ms nodes which did not receive etb before
                    node = findBestSource(getNodes(etb), MydestinationNodes) #best source is node closest to a node of destinationNodes
                    treenodes = copy.deepcopy(MydestinationNodes) 
                    treenodes.append(node)
                                        
                    mytree = steiner_tree(G, treenodes)
                    myInstance = Instance(etype, etb, [node], {projection: list(mytree.edges)}) #! #append routing tree information for instance/etb                    
                    newInstances.append(myInstance) #!
                    
                    
                    
                    myPathLength = max([len(nx.shortest_path(mytree, x, node, method='dijkstra')) for x in MydestinationNodes]) - 1
                    
                    
                    if etype in projFilterDict.keys() and  getMaximalFilter(projFilterDict, etype, noFilter): #case input projection has filter
                        mycosts =  len(mytree.edges()) * getDecomposedTotal(getMaximalFilter(projFilterDict, etype, noFilter), etype)                    
                        if len(IndexEventNodes[etype]) > 1 : # filtered projection has ms placement
                             partType = returnPartitioning(etype, mycombi[etype])[0]                     
                             mycosts -= len(mytree.edges())  * rates[partType] * singleSelectivities[getKeySingleSelect(partType, etype)] * len(IndexEventNodes[etype])
                             mycosts += len(mytree.edges())  * rates[partType] * singleSelectivities[getKeySingleSelect(partType, etype)] 
                    elif len(etype) == 1:
                        mycosts = len(mytree.edges()) * rates[etype]
                    else:                    
                        num = NumETBsByKey(etb, etype)                 
                        mycosts = len(mytree.edges()) *  projrates[etype][1] * num     # FILTER              
                        
                    placementTreeDict[(tuple(destinationtypes),etb)] = [node, MydestinationNodes, mytree] #only kept for updating in the next step
                    costs +=  mycosts 
                    
                    pathLength = max([pathLength, myPathLength])
                    
                    # update events sent over network
                    for routingNode in mytree.nodes():
                        if not routingNode in getNodes(etb):
                            setEventNodes(routingNode, etb)
    
        
  # print(list(map(lambda x: str(x), sourcetypes)), costs)           
    return costs, pathLength, newInstances




def NEWcomputeMSplacementCosts_Path(projection, sourcetypes, destinationtypes, noFilter): #for PathVariant - fix generate EvalPlan
    costs = 0
    destinationNodes = []     

    for etype in destinationtypes:
        for etb in IndexEventNodes[etype]:
            destinationNodes += getNodes(etb)            
            
    newInstances = [] #!
    longestPath = 0        
    etype = sourcetypes[0]
    routingInfo = []
        
    for etb in IndexEventNodes[etype]: #parallelize
        
        newInstance = False   
        MydestinationNodes = list(set(destinationNodes).difference(set(getNodes(etb)))) #only consider nodes that do not already hold etb
        if MydestinationNodes:     
                for dest in MydestinationNodes:
                   if not dest in getNodes(etb):  
                        #are there ms nodes which did not receive etb before
                        node = findBestSource(getNodes(etb), [dest]) #best source is node closest to a node of destinationNodes
                        
                        shortestPath = nx.shortest_path(G, dest, node, method='dijkstra') 
                        if len(shortestPath) > longestPath:
                            longestPath = len(shortestPath)
                    
                        if etype in projFilterDict.keys() and  getMaximalFilter(projFilterDict, etype, noFilter): #case input projection has filter
                            mycosts =  len(shortestPath) * getDecomposedTotal(getMaximalFilter(projFilterDict, etype, noFilter), etype)                    
                            if len(IndexEventNodes[etype]) > 1 : # filtered projection has ms placement
                                 partType = returnPartitioning(etype, mycombi[etype])[0]                     
                                 mycosts -= len(shortestPath)  * rates[partType] * singleSelectivities[getKeySingleSelect(partType, etype)] * len(IndexEventNodes[etype])
                                 mycosts += len(shortestPath)  * rates[partType] * singleSelectivities[getKeySingleSelect(partType, etype)] 
                        elif len(etype) == 1:
                            mycosts = len(shortestPath) * rates[etype]
                        else:                    
                            num = NumETBsByKey(etb, etype)                 
                            mycosts = len(shortestPath) *  projrates[etype][1] * num          
                        costs +=  mycosts     

                        routingInfo.append(shortestPath)    # destinations have different sources
                    
                        for routingNode in shortestPath:
                            if not routingNode in getNodes(etb):
                                setEventNodes(routingNode, etb)  
                        newInstance = True        
        if newInstance:
            myInstance = Instance(etype, etb, [node], {projection: routingInfo}) #! #append routing tree information for instance/etb                    
            newInstances.append(myInstance) #!        
    return costs, longestPath, newInstances




def NEWcomputeMSplacementCosts_par(projection, sourcetypes, destinationtypes): #we need tuples, (C, [E,A]) C should be sent to all e and a nodes ([D,E], [A]) d and e should be sent to all a nodes etc
    costs = 0
    
    destinationNodes = []
    for etype in destinationtypes:
        for etb in IndexEventNodes[etype]:
            destinationNodes += getNodes(etb)        
                
    newInstances = [] #!
    curpathLength = 0                
    pathLength = 0
    
    pool = multiprocessing.Pool()
    func = partial(placeMS,destinationNodes,etype)
    for etype in sourcetypes:  #parallelize
        result = pool.map(func, IndexEventNodes[etype])
    #pool.close()
    #pool.join()        
    for i in result:
        costs += i[0]    
        pathLength = max(i[1], curpathLength)
        newInstances.append(i[2])  
        # update events sent over network

        for node in i[3][0]:
            if not node in getNodes(i[3][1]):
                setEventNodes(node, i[3][1]) 
                
    return costs, pathLength, newInstances

def placeMS(destinationNodes, etype, etb):
    
    mycosts = 0
    myPathLength = 0
    myInstance = Instance(etype, etb,[], {})
    mytree = nx.Graph()
    
    destinationNodes = list(set(destinationNodes).difference(set(getNodes(etb)))) #only consider nodes that do not already hold etb
            
    if destinationNodes: #are there ms nodes which did not receive etb before
                
                    node = findBestSource(getNodes(etb), destinationNodes) #best source is node closest to a node of destinationNodes
                    
                    treenodes = copy.deepcopy(destinationNodes) 
                    treenodes.append(node)
                                        
                    mytree = steiner_tree(G, treenodes)
                    
                    myInstance = Instance(etype, etb, [node], {projection: mytree.edges}) #! #append routing tree information for instance/etb                
                    
                    myPathLength = max([len(nx.shortest_path(mytree, x, node, method='dijkstra')) for x in destinationNodes])
                    
                    if len(etype) == 1:
                        mycosts = len(mytree.edges()) * rates[etype]
                    else:                    
                        num = NumETBsByKey(etb, etype)                 
                        mycosts = len(mytree.edges()) * projFilterDict[etype][getMaximalFilter(projFilterDict, etype, noFilter)][0] * num     # FILTER              
                        #mycosts = len(mytree.edges()) * projrates[etype][1] * num                         
          
    return (mycosts, myPathLength, myInstance, (mytree.nodes, etb))    

def alternative_NEWcomputeMSplacementCosts(sourcetypes, destinationtypes): #we need tuples, (C, [E,A]) C should be sent to all e and a nodes ([D,E], [A]) d and e should be sent to all a nodes etc
    costs = 0
    destinationNodes = []
    pathLength = 0
    
    # for etype in destinationtypes:
    #     for etb in IndexEventNodes[etype]:
    #         destinationNodes += getNodes(etb)  
    for etype in destinationtypes:
        for etb in IndexEventNodes[etype]:
            destinationNodes += getNodes(etb)
    for sourcetype in sourcetypes:
                destinationNodes = [x for x in destinationNodes if not set(IndexEventNodes[sourcetypes]).issubset(set(getETBs(x)))]
            
    mytree = steiner_tree(G, destinationNodes)
    
    
    for etype in sourcetypes:  
        for etb in IndexEventNodes[etype]:                             
                    node = findBestSource(getNodes(etb), mytree.nodes()) #best source is node closest to a node of destinationNodes

                    if len(etype) == 1:
                        mycosts = (len(mytree.edges()) + min([allPairs[node][x] for x in  mytree.nodes()])) * rates[etype] 
                    else:                    
                        num = NumETBsByKey(etb, etype)                 
                        mycosts = (len(mytree.edges()) + min([allPairs[node][x] for x in  mytree.nodes()])) * projFilterDict[etype][getMaximalFilter(projFilterDict, etype, noFilter)][0] * num     # FILTER              
                        #mycosts = len(mytree.edges()) * projrates[etype][1] * num  
                        
                    placementTreeDict[(tuple(destinationtypes),etb)] = [node, destinationNodes, mytree] #only kept for updating in the next step
                    costs +=  mycosts 
            
                    # update events sent over network
                    treenode = [x for x in mytree.nodes() if allPairs[node][x] == min([allPairs[node][x] for x in  mytree.nodes()])][0]
                    shortestPath = nx.shortest_path(G, treenode, node, method='dijkstra') #next three lines for hop latency
                    
                    curLength = max([allPairs[treenode][x] for x in mytree.nodes])+  len(shortestPath)
                    if curLength > pathLength:
                        pathLength = curLength
                    for routingNode in [x for x in mytree.nodes()] + shortestPath:
                        if not routingNode in getNodes(etb):
                            setEventNodes(routingNode, etb)
                  
    print(pathLength)           
    return costs, pathLength          

def findBestSource(sources, actualDestNodes): #this is only a heuristic, as the closest node can still be shit with respect to a good steiner tree ?+
    curmin = np.inf     
    for node in sources:        
        if min([allPairs[node][x] for x in actualDestNodes]) < curmin:
           curmin =  min([allPairs[node][x] for x in actualDestNodes])
           bestSource = node
    return bestSource
        
def getDestinationsUpstream(projection):
    return  range(len(allPairs))    
    myPartTypes = []
    nodes = []
    for i in mycombi.keys():
        if projection in mycombi[i]:
            partType = originalDict[i][1]
            if partType:
                myPartTypes.append(partType[0])
    if myPartTypes:
        for k in myPartTypes:
            for etb in IndexEventNodes[k]:
                nodes.append(getNodes(etb)[0])
        
        return nodes
    else:        
        return  range(len(allPairs))      
        
def ComputeSingleSinkPlacement(projection, combination, noFilter):
    costs = np.inf
    node = 0
    Filters  = []    
    
     
    # add filters of projections to eventtpes in combi, if filters added, use costs of filter -> compute costs for single etbs of projrates 
    intercombi = []
    ##### FILTERS
    for proj in combination:
        intercombi.append(proj)  
        #print(list(map(lambda x: str(x), list(projFilterDict.keys()))))
        if len(proj) > 1 and len(getMaximalFilter(projFilterDict, proj, noFilter)) > 0:            
            Filters.append((proj,getMaximalFilter(projFilterDict, proj, noFilter)))            
            for etype in getMaximalFilter(projFilterDict, proj, noFilter):
                intercombi.append(etype)
    combination = list(set(intercombi))
    
    myProjection = Projection(projection, {}, [], [], Filters) #!
    
    goodDestinations = getDestinationsUpstream(projection) # consider only placement at upstream projections in cas of ms placements
    #goodDestinations = [x for x in range(len(allPairs))]
    #print(list(map(lambda x: str(x), combination)))
    for destination in goodDestinations: 
        mycosts = 0       
        for eventtype in combination:
                for etb in IndexEventNodes[eventtype]: #check for all sources #here iterated over length of IndesEventNodes to get all sources for etb Instances
                        possibleSources = getNodes(etb)
                        mySource = possibleSources[0]
                        for source in possibleSources:
                            if allPairs[destination][source] < allPairs[destination][mySource]:                               
                                   mySource  = source
                        if eventtype in projFilterDict.keys() and  getMaximalFilter(projFilterDict, eventtype, noFilter): #case filter 
                            mycosts +=  allPairs[destination][mySource] * getDecomposedTotal(getMaximalFilter(projFilterDict, eventtype, noFilter), eventtype)                    
                            if len(IndexEventNodes[eventtype]) > 1 : # filtered projection has ms placement
                                partType = returnPartitioning(eventtype, mycombi[eventtype])[0]                     
                                mycosts -= allPairs[destination][mySource] * rates[partType] * singleSelectivities[getKeySingleSelect(partType, eventtype)] * len(IndexEventNodes[eventtype])
                                mycosts += allPairs[destination][mySource] * rates[partType] * singleSelectivities[getKeySingleSelect(partType, eventtype)] 
                        elif eventtype in rates.keys():        # case primitive event
                            mycosts += rates[eventtype] * allPairs[destination][mySource]  
                        else: # case projection                         
                             num = NumETBsByKey(etb, eventtype)
                             mycosts += projrates[eventtype][1] * allPairs[destination][mySource] * num 
 
        if mycosts < costs:
            costs = mycosts
            node = destination
    
    myProjection.addSinks(node) #!
    newInstances = [] #!
    # Update Event Node Matrice, by adding events etbs sent to node through node x to events of node x
    longestPath  = 0
    for eventtype in combination:
            curInstances = [] #!
            for etb in IndexEventNodes[eventtype]:
                possibleSources = getNodes(etb)
                mySource = possibleSources[0] #??
                for source in possibleSources:                    
                    if allPairs[node][source] < allPairs[node][mySource]:
                       mySource  = source     
                shortestPath = nx.shortest_path(G, mySource, node, method='dijkstra') 
              
                if len(shortestPath) - 1 > longestPath:
                    longestPath = len(shortestPath) - 1                    
                newInstance = Instance(eventtype, etb, [mySource], {projection: shortestPath}) #!
                curInstances.append(newInstance) #!    
                
                for stop in shortestPath:
                    if not stop in getNodes(etb):                        
                        setEventNodes(stop, etb) 
                        
            newInstances += curInstances          #!   
            myProjection.addInstances(eventtype, curInstances)     #!        
                        
    SiSManageETBs(projection, node)
    
    myProjection.addSpawned(IndexEventNodes[projection][0]) #!
        
    return costs, node, longestPath, myProjection, newInstances, Filters

def costsAt(eventtype, node):
    mycosts = 0
    for etb in IndexEventNodes[eventtype]:
                possibleSources = getNodes(etb)
                mySource = possibleSources[0]
                for source in possibleSources:
                    if allPairs[node][source] <= allPairs[node][mySource]:
                       mySource  = source
                mycosts += rates[eventtype] * allPairs[node][mySource] 
    return mycosts

def NEWcomputeCentralCosts(workload):
    eventtypes = []
    for i in workload:
        myevents = i.leafs()
        for e in myevents:
            if not e in eventtypes:
                eventtypes.append(e)
    costs = np.inf
    node = 0
    for destination in range(len(allPairs)):
        mycosts = 0      
        for eventtype in eventtypes:
            oldcosts = mycosts
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
    longestPath = max(allPairs[node])
    
    routingDict = {} # for evaluation plan
    for e in eventtypes:        
        routingDict[e] = {}
        for etb in IndexEventNodes[e]:
            possibleSources = getNodes(etb)
            mySource = possibleSources[0]
            shortestPath = nx.shortest_path(G, mySource, node, method='dijkstra')  
            routingDict[e][etb] = shortestPath
 
    for eventtype in eventtypes:    
        thiscosts = 0
        for etb in IndexEventNodes[eventtype]:
                    mySource = getNodes(etb)[0]         
                    thiscosts += rates[eventtype] * allPairs[node][mySource]
                  #  print(allPairs[node][mySource])
      #  print(eventtype, thiscosts )    
    return (costs, node, longestPath, routingDict) 
                    
#TODO compute and print rates saved by placement