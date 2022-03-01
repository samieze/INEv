#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 15:46:49 2021

@author: samira
"""
import subsets as sbs 
import multiprocessing
#from processCombination import *
from filter import *

with open('current_wl',  'rb') as  wl_file:
    wl = pickle.load(wl_file)
    
#wl = [wl[0]]   
with open('selectivities', 'rb') as selectivity_file:
    selectivities = pickle.load(selectivity_file) 


# structures for speedup in partInput function
MSTrees  = {}
DistMatrices =  {}



def optimisticTotalRate(projection): # USE FILTERED RATE FOR ESTIMATION 
    if projection in projlist: # is complex event        
        for i in projFilterDict.keys():
            if i  == projection: 
                myproj = i
                if getMaximalFilter(projFilterDict, myproj):                                                
                        return getDecomposedTotal(getMaximalFilter(projFilterDict, myproj), myproj)    
                else:
                        return projFilterDict[myproj][getMaximalFilter(projFilterDict, myproj)][0] * getNumETBs(myproj) #TODO change
    else:
        return rates[projection.leafs()[0]] * len(nodes[projection.leafs()[0]])
    
    
def optimisticTotalRate_single(projection): # USE FILTERED RATE FOR ESTIMATION 
    for i in projFilterDict.keys():
            if i  == projection: 
                myproj = i
                if getMaximalFilter(projFilterDict, myproj):                                                
                        return getDecomposedTotal(getMaximalFilter(projFilterDict, myproj), myproj)    
                else:
                        return projrates[myproj][1] * getNumETBs(myproj) #TODO change
    else:
        return rates[projection.leafs()[0]] * len(nodes[projection.leafs()[0]])    


    
def returnPartitioning(proj, combi, *args):
    
    ''' returns list containing partitioning input type of proj generated with combi, args contains critical eventtypes, if potential eventtype in critical events, return False '''
    myevents = [x for x in combi if len(x) == 1]
    myevents = sorted(myevents, key = lambda x: rates[x], reverse = True)
        
    if args:
        args = args[0]
        if myevents:
            if myevents[0] in args:
                return []
    
    if myevents:
        
        res = NEW_isPartitioning(myevents[0], combi, proj)

        if res:               
           return [myevents[0], res[0]]
    return []

def isPartitioning(element, combi, proj):
       ''' returns true if element partitioning input of proj generated with combi '''

       mysum =  0    
       for i in combi:   
           
           if i in rates.keys():        
              additional = rates[i] * instances[i]              
              mysum += additional
              
           else:
               additional = projrates[i][1] * getNumETBs(i)              
               mysum += additional #  len(returnETBs(projection, network))
              
       mysum -= rates[element] * instances[element]
       mysum += projrates[proj][1] * getNumETBs(proj) # additional constraint about ratio of partitioning event type and outputrate of projection
       if rates[element] > mysum : 
           return True

       else: 
           return False   
       
def NEW_isPartitioning(element, combi, proj):
       ''' returns true if element partitioning input of proj generated with combi '''
       
       etbs = IndexEventNodes[element]
       myNodes = [getNodes(x)[0] for x in etbs]   
       if not element in MSTrees.keys():
           myTree = steiner_tree(G, myNodes)
           MSTrees[element] = myTree
       else:
           myTree =  MSTrees[element]
       
       if not myTree in DistMatrices.keys():           
           myAllPairs = fillMyDistMatrice(myTree)
           DistMatrices[myTree] = myAllPairs
       else:
           myAllPairs = DistMatrices[myTree]       
       
       costs = len(myTree.edges())                
       
       mysum =  0    
       for i in [x for x in combi if not x == element]:            
           if i in rates.keys():        
              additional = rates[i] * len(nodes[i])              
              mysum += additional              
           else:
               additional = projrates[i][1] * getNumETBs(i)             
               mysum += additional
       
       myproj  = 0 #costs for outputrates
       if not proj in wl:
           myproj =  projrates[proj][1] * (getNumETBs(proj)) # additional constraint about ratio of partitioning event type and outputrate of projection

       if totalRate(element) * longestPath > (mysum * costs) + myproj * longestPath :  
           return [costs]

       else: 
           return False 
       
        
def NEW_isPartitioning_alt(element, combi, proj, myprojFilterDict):
       ''' returns true if element partitioning input of proj generated with combi '''
       
       etbs = IndexEventNodes[element]
       myNodes = [getNodes(x)[0] for x in etbs]   
       if not element in MSTrees.keys():
           myTree = steiner_tree(G, myNodes)
           MSTrees[element] = myTree
       else:
           myTree =  MSTrees[element]
       
       if not myTree in DistMatrices.keys():           
           myAllPairs = fillMyDistMatrice(myTree)
           DistMatrices[myTree] = myAllPairs
       else:
           myAllPairs = DistMatrices[myTree]       
       
       costs = len(myTree.edges())                
       
       mysum =  0    
       for i in [x for x in combi if not x == element]:            
           if i in rates.keys():        
              additional = rates[i] * len(nodes[i])              
              mysum += additional              
           else:
               additional = getDecomposedTotal(getMaximalFilter(myprojFilterDict, i), i)             
               mysum += additional
       
       myproj  = 0 #costs for outputrates
       if not proj in wl:
           myproj =  getDecomposedTotal(getMaximalFilter(myprojFilterDict, proj), proj)  # additional constraint about ratio of partitioning event type and outputrate of projection
  
       if totalRate(element) * longestPath > (mysum * costs) + myproj * longestPath :  
           return [costs]

       else: 
           return False        
       


def fillMyMatrice(myNodes, myEdges, me):  
    myG = nx.Graph()
    myG.add_nodes_from(myNodes)
    myG.add_edges_from(myEdges)   
    myDistances = []
    for j in myNodes:            
           myDistances.append(len(nx.shortest_path(myG, me, j, method='dijkstra')) - 1)   
    return (me, myDistances)

pool = multiprocessing.Pool()

def fillMyDistMatrice(myG): #all pairs shortest path distance matrice -> also slow for big graphs
    myNodes = list(myG.nodes)
    myPairs = [[] for x in myNodes ]
    mytuple = (list(myNodes),list(myG.edges))
    args  = [(mytuple[0], mytuple[1], x) for x in myNodes ]
    result = pool.starmap(fillMyMatrice, args)
    for i in result:
        myPairs.append(i[1])
    return myPairs


    
def min_max_doubles(query,projevents):
    doubles = getdoubles_k(projevents)
    leafs = map(lambda x: filter_numbers(x), query.leafs())
    for event in doubles.keys():
        if not doubles[event] == leafs.count(event):
            return False
    return True
 
    
def settoproj(evlist,query):
    """ take query and list of prim events and return projection"""
    leaflist = []
    evlist = sepnumbers(evlist)  
    evlist = list(map(lambda x: str(x), evlist))
    for i in evlist:   
        leaflist.append(PrimEvent(i))    
    newproj = query.getsubop(leaflist)  
    return newproj

def isBeneficial(projection, rate):
    """ determines for a projection based on the if it is beneficial """
    totalProjrate = rate * getNumETBs(projection)
    sumrates = sum(map(lambda x: rates[x] * float(len(nodes[x])), projection.leafs()))
    if sumrates > totalProjrate:
        return True
    else:
        return False

def totalRate(projection):
    if projection in projrates.keys(): # is complex event
       # print(projection, projrates[projection][1], getNumETBs(projection))
        return projrates[projection][1] * getNumETBs(projection)
    elif len(projection) == 1:
        return rates[str(projection)] * len(nodes[str(projection)])
    else:
        outrate = projection.evaluate() *  getNumETBs(projection)  
        selectivity =  return_selectivity(projection.leafs())
        myrate = outrate * selectivity  
        return myrate

    
def return_selectivity(proj):
    
    """ return selectivity for arbitrary projection """
    proj = list(map(lambda x: filter_numbers(x), proj))
    two_temp = sbs.printcombination(proj,2)    
    selectivity = 1
    for two_s in two_temp:       
        if two_s in selectivities.keys():           
           if selectivities[two_s]!= 1:
               selectivity *= selectivities[two_s]
    return selectivity

def generate_projections(query):  
    """ generates list of benecifical projection """    
    projections = []
    projrates = {}
    match = query.leafs()
    projlist = match
    for i in range(2, len(match)):
           iset =  sbs.boah(match, i) 
           for k in range(len(iset)):                   
                    curcom = list(iset[k].split(","))  
                    projevents = rename_without_numbers("".join(sorted(list(set(curcom))))) #A1BC becomes ABC and A1B1CA2 becomes A1BCA2                    
                    mysubop = settoproj(curcom, query) 
                    mysubop = mysubop.rename_leafs(sepnumbers(projevents)) #renaming on tree > A1BC becomes ABC and A1B1CA2 becomes A1BCA2                                                                  
                    outrate = mysubop.evaluate()                          
                    selectivity =  return_selectivity(curcom)
                    rate = outrate * selectivity                            
                    placement_options = isBeneficial(mysubop, rate)  
                    
                    if placement_options and min_max_doubles(query, projevents):  # if the projection is beneficial (yields a placement option) and minmax?                         
                                projrates[mysubop] = (selectivity, rate)                    
                                projections.append(mysubop) # do something to prevent a1a2b and a2a3b to be appended to dictionary
                                
    projections.append(query)
    outrate = query.evaluate()                          
    selectivity =  return_selectivity(query.leafs())
    rate = outrate * selectivity                            
    projrates[query] = (selectivity, rate) 

    return projections, projrates

def returnSubProjections(proj, projlist): # beware of primitive events with multiple occurrences!
    """ return list of projection keys that can be used in a combination of a given projection"""    
    myprojlist = [x for x in projlist if len(x.leafs()) <= len(proj.leafs()) and set(x.leafs()).issubset(set(proj.leafs()))]
    outputlist = []                          
    for i in myprojlist:
                if not proj == i:
                 if i.can_be_used(proj):    
                     outputlist.append(i)

    return outputlist

sharedProjectionsDict = {}
sharedProjectionsList = []
projsPerQuery = {}
#query = wl[0]
projlist = []
projrates = {}

for query in wl:
    result = generate_projections(query)
    for i in result[0]:        
        if not i in projlist:
            projlist.append(i)
            projrates[i] = result[1][i]
            sharedProjectionsDict[i] = [query]
        else:
            for mykey in sharedProjectionsDict.keys():
                if mykey == i:
                    sharedProjectionsDict[mykey].append(query)

for query in wl:
    projsPerQuery[query] = [x for x in projlist if query.can_be_used(x)]

for projection in sharedProjectionsDict.keys():
    if len(sharedProjectionsDict[projection]) > 1:
        sharedProjectionsList.append(projection) 

      
with open('projrates',  'wb') as projratesfile:
    pickle.dump(projrates, projratesfile)

