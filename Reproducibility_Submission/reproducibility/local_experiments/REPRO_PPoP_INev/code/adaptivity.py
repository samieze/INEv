#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 16:26:36 2022

@author: samira


Used for adaptivity experiments.

Computes costs of given INEv graph. 
Checks if for given network rates INEv graph contains broken projections or broken multi-node placements.
Computes costs of repaired graph.

"""
import sys
import csv
from EvaluationPlan import *
from generate_projections import *
import pickle
import math 


with open('EvaluationPlan', 'rb') as EvaluationPlan_file: 
          myplan = pickle.load(EvaluationPlan_file)[0]
  
def compute_dependencies_simple(combiDict):# has as input a final combination
    ''' outputs a dictionary which has as keys the projections of a final combination and as corresponding key the level of the projection in the muse graph, for sis and ms projections having the same level, level for msp is increased as placements can be exploited here'''         
    levels = {}
    for proj in combiDict.keys():
        if len(proj.leafs()) == 2 or set(combiDict[proj]) == set(proj.leafs()):
            levels[proj] = 0           
            
    for proj in sorted([x for x in combiDict.keys() if not x in levels.keys()], key= lambda z: len(z.leafs())): # mit vorsicht zu genießen
        mymax = max(list(map(lambda x: levels[x], [x for x in combiDict[proj] if x in combiDict.keys()])))
        levels[proj] = mymax + 1
    
    return levels               
  
def getTuples(mylist):
    if mylist:
        if isinstance(mylist[0], list):
            myTuples = []
            for i in mylist:
                myTuples += getTuples_single(i)
            return list(set(myTuples))
        else:
            return  getTuples_single(mylist)
    else:
        return []

def getTuples_single(mylist):
     
    newlist = []
    if len(mylist) > 0:
        if isinstance(mylist[0], tuple):
            return mylist
        else: 
            for i in range(len(mylist) - 1):
                newlist.append((mylist[i],mylist[i+1] ))
                
    return newlist

def getSubgraph(routingTree, eventtype): # get subgraph for given routing tree and event type
    sinks = nodes[eventtype]
    myG= nx.Graph()
    myG.add_edges_from(routingTree)
    subGraph =  steiner_tree(myG, sinks)
    return list(subGraph.edges)

def getSingleSinkRouting(etbsource, destination):
    myshortest = nx.shortest_path(G, etbsource, destination, method='dijkstra')
    return getTuples(myshortest)
          
def getNewProjrates():
    myProjrates = {}
    for proj in myplan.projections:
        thisproj = proj.name.name          
        rate = thisproj.evaluate() * return_selectivity(thisproj.leafs())
        myProjrates[thisproj] = rate
    for eventtype in  rates.keys():
        myProjrates[eventtype] = rates[eventtype]
    return myProjrates    

def getparttype(projection):
    sinks = set(projection.sinks)
    for instance in projection.getInputInstances():
        sources = set(instance.sources)
        if sinks == sources:
            return instance.projname
        

def getMultiNodeRoutes(projection):
    mydict = {}
    parttype = getparttype(myplan.getProjection(projection).name)
    for inputproj in mycombi[projection]:
        if len(inputproj) > 1: 
            for etb in myplan.getProjection(inputproj).name.spawnedInstances:
                etbDict = myplan.getByName(etb).routingDict
                for route in list(etbDict.values()):
                    if len(route) > 1:
                        if isinstance(route[0], tuple):
                            mydict[etb] = getSubgraph(route, parttype)
        else:
            for etb in IndexEventNodes[inputproj]:
                etbDict = myplan.getByName(etb).routingDict
                for route in list(etbDict.values()):
                    if len(route) > 1:
                        if isinstance(route[0], tuple):     
                            mydict[etb] = getSubgraph(route, parttype)
    return mydict        




def inputcosts(projection): #input rate of projection
    costs = 0   
    for myinput in mycombi[projection]:
        if len(myinput) >1 :
            costs +=  myprojrates[myinput] *  math.prod(instances[x] for x in myinput.leafs())
        else:
            costs += rates[myinput] * instances[myinput]
    return costs                   

def getRoutingInfo(routingDict):
    finalroute = []
    for proj in routingDict.keys():
        finalroute.append(getTuples(routingDict[proj]))
    return list(set(sum(finalroute, [])))

def getSingleNodeRoute(routingDict):
    finalroute = []
    for proj in routingDict.keys():
        if routingDict[proj]:
            if isinstance(routingDict[proj][0], int):
                finalroute.append(routingDict[proj])
    return finalroute            


def getCosts(routing, rates):
    costs = 0 
    for i in myplan.instances: 
        
        costs += len(routing[i.name]) * rates[i.projname] * NumETBsByKey(i.name, i.projname)
    return costs

 
# compute projection rates (additionally to proj rates)
myprojrates = getNewProjrates()

#print(wl)
myprojs = []
multinode = []
sources = {}
mycombi = {}
myrate = {}
myRouting = {}
multinodeRoutes = {}
singleNodeRoutes =  {}

# 1. iterate through projections, get sub-graphs for multi-node placed projections per input etb

for k in myplan.projections:    
    myprojs.append(k.name.name)
    mycombi[k.name.name] = k.name.combination.keys()
    if len(k.name.sinks)>1:
        multinode.append(k.name.name)
        multinodeRoutes[k.name.name]= getMultiNodeRoutes(k.name.name)

# 2. get sources for each instance and general routing information
for i in myplan.instances:     
             
             # 0. construct dict with sources per etb, update for m-n placements that become single sink placements
            # if not i.projname in wl:
             if ''.join([n for n in i.name if n.isdigit()]) != '':
                     sources[i.name] = int(''.join([n for n in i.name if n.isdigit()]))# get original source by extracting node name from etb name
             elif i.sources:
                     sources[i.name]  = i.sources[0] #TODO!!!
             myRouting[i.name] = getRoutingInfo(i.routingDict)
             singleNodeRoutes[i.name] = getSingleNodeRoute(i.routingDict)
             
# Compute Costs for current config 
costsBefore =  getCosts(myRouting,  myprojrates)  
print("Costs", getCosts(myRouting,  myprojrates))



# 2. change projrates to sum of input rates (repair broken projections) 
# 3. multi-node placed projections for which the projection is broken are also broken

brokenProjs = []
brokenMNplacements = []

levels = compute_dependencies_simple(mycombi)
for projection in sorted(myprojs, key = lambda x: levels[x]):
    if not projection in wl:
        if myprojrates[projection] * getNumETBs(projection) > inputcosts(projection): 
            brokenProjs += [projection]
            if projection in multinode:
                brokenMNplacements  += [projection]
            myprojrates[projection] = inputcosts(projection) /  getNumETBs(projection)

print("broken projs",  len(list(set(myprojs))), len(brokenProjs), list(map(lambda x: str(x), brokenProjs) ))

costsRep1 = getCosts(myRouting,  myprojrates)
print("repaired Costs", getCosts(myRouting,  myprojrates))


# 4. compute additional broken multi-node placements 
for i in list(set(multinode)): 
    projection = myplan.getProjection(i).name
    combination =  projection.combination.keys()
    parttype = getparttype(myplan.getProjection(i).name)  
    if not NEW_isPartitioning_customRates(parttype, combination, projection.name, myprojrates):       
       brokenMNplacements += [projection.name] 
       
brokenMNplacements = list(set(brokenMNplacements))   

print("broken MN placements: ", len(list(set(multinode))), len(brokenMNplacements), list(map(lambda x: str(x), brokenMNplacements) ))    


for i in brokenMNplacements:
    print(i, list(map(lambda x: str(x), list(mycombi[i]))))
print("---------------")

# 5. for each broken multi-node placement, substitute sub-graph for each etb input to shortest path für jedes kaputte multi-node placement
for projection in sorted(brokenMNplacements, key = lambda x: levels[x]):
    partType = getparttype(myplan.getProjection(projection).name)  
    sink = nodes[partType][0]
    for inputetb in multinodeRoutes[projection].keys():
        multinodeRoutes[projection][inputetb] = getSingleSinkRouting(sources[inputetb], sink)
    if not projection in wl:
        for etb in myplan.getProjection(projection).name.spawnedInstances:            
            # add shortest path to new single-sink for former partitioning event type 
            myRouting[etb] = getSingleSinkRouting(sources[etb], sink)
            # add source for each etb of ex multi-node projection
            sources[etb] = sink 
            
# unify for each etb pathes
newPath = {}
for proj in [x for x in multinodeRoutes.keys() if x in brokenMNplacements]:
    for etb in multinodeRoutes[proj]:
        if not etb in newPath.keys():
            newPath[etb] = multinodeRoutes[proj][etb]
        else:
            newPath[etb] = list(set(newPath[etb]).union(set(multinodeRoutes[proj][etb])))
        newPath[etb] =    list(set(newPath[etb]).union(set(getTuples(singleNodeRoutes[etb])))) 
        
for etb in myRouting.keys():
    if etb in newPath.keys():
        myRouting[etb] = newPath[etb]
        
costsRep2 = getCosts(myRouting,  myprojrates)
print("MN repaired Costs", getCosts(myRouting,  myprojrates))


experimentname = 0
numberOfswaps = 0
skew = 0
if len(sys.argv) > 1:
        experimentname = int(sys.argv[1])
if len(sys.argv) > 2:
        numberOfswaps = int(sys.argv[2])       
if len(sys.argv) > 3:
        skew = float(sys.argv[3])        
       
        
schema = ["ID", "Swaps", "NumberProjections", "brokenProjections", "NumberPlacements", "brokenPlacements", "costs", "costs_rep1", "costs_rep2",'Skew'] 
myResult = [experimentname, numberOfswaps,  len(myprojs) , len(brokenProjs), len(multinode),  len(brokenMNplacements), costsBefore, costsRep1, costsRep2, skew]
new = False
try:
        f = open("adaptivity/results_adaptivity.csv")   
except FileNotFoundError:
        new = True           
        
with open("adaptivity/results_adaptivity.csv", "a") as result:
      writer = csv.writer(result)  
      if new:
          writer.writerow(schema)              
      writer.writerow(myResult)