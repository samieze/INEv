#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 14:16:13 2021

@author: samira

Generate combination, initial output selectors for query workload and network.

"""
import sys
import random
from generate_projections import *
import time 
numberCombis = 0

projFilterDict =  {}  
    

for proj in projlist:
    projFilterDict.update(returnProjFilterDict(proj))    

def optimisticTotalRate(projection, *noFilterParam): # USE FILTERED RATE FOR ESTIMATION 
    noFilter = 0
    if noFilterParam:
        noFilter = noFilter[0]
    if projection in projlist: # is complex event        
        for i in projFilterDict.keys():
            if i  == projection: 
                myproj = i
               
                if getMaximalFilter(projFilterDict, myproj):                                                
                        return getDecomposedTotal(getMaximalFilter(projFilterDict, myproj, noFilter), myproj)    
                else:
                        #return projrates[myproj][1]
                        return projFilterDict[myproj][getMaximalFilter(projFilterDict, myproj, noFilter)][0] * getNumETBs(myproj) #TODO change
    else:
        return rates[projection.leafs()[0]] * len(nodes[projection.leafs()[0]])

def removeFilters():
    for i in projFilterDict.keys():
        toRemove = [x for x in projFilterDict[i].keys() if not x == '']
        for x in toRemove:
            del projFilterDict[i][x]
            
            
removeFilters()            
            
def cheapRest(upstreamprojection, projection, partEvent, restRate): # this is not correct -> all partitionings of cheap rest must be investigated! also remaining events muss in teillisten aufgeteilt werden etc. 
    ''' checks if the rest of primitve events that must be provided to match upstream projection with projection and a multisink placement of partEvent allows the multi-sink placement at partEvent '''
    remainingEvents = list(set(upstreamprojection.leafs()).difference(set(projection.leafs() + [partEvent])))
    remainingEventsQ = [PrimEvent(x) for x in remainingEvents]
    for event in remainingEvents: # problem -> primitive events    
       #print(list(map(lambda x: str(x), [x for x in (projlist + remainingEventsQ) if event in x.leafs() and len(x.leafs()) < len(upstreamprojection.leafs()) and set(x.leafs()).issubset(set(upstreamprojection.leafs()))]))) # and set(x.leafs()).issubset(set(upstreamprojection.leafs()))])
       #TODO: next line is highly critical...
       #cheapestProj =  sorted([x for x in (projlist + remainingEventsQ) if partEvent not in x.leafs() and not set(projection.leafs()).issubset(set(x.leafs())) and event in x.leafs() and len(x.leafs()) < len(upstreamprojection.leafs()) and set(x.leafs()).issubset(set(upstreamprojection.leafs()))], key = lambda x: optimisticTotalRate(x))[0]
       cheapestProj = PrimEvent(event[0]) # only MS combinations with exactly one complex event as input investigates
       remainingEvents = list(set(remainingEventsQ).difference(set(remainingEventsQ).intersection(set(cheapestProj.leafs()))))
       restRate -= optimisticTotalRate(cheapestProj)
    if restRate > 0 :
        return True
    else: 
        
        return False
       
def promisingChainProjection(projection):
    ''' outputs for a projection a dictionary having potential partitioning event types as keys and the potential multisink projections in which projection is part of the combination '''
    optimisticRate =  optimisticTotalRate(projection)
    combinationdict = {}
    
    cheapRests = {}
    for eventtype in query.leafs():   
        if not eventtype in projection.leafs():     
            for i in projFilterDict.keys():
                if i  == projection: 
                    myproj = i
                    filters = projFilterDict[myproj].keys() # here totalRate should also investigate "filtered rates"
                    break
            usingfilter = []
            for myfilter in filters:                
                if getDecomposedTotal(myfilter, projection) < rates[eventtype]:
                    usingfilter.append(myfilter)
            if usingfilter:     # always true...                
                    events = [x for x in projection.leafs()]
                    events.append(eventtype)   

                    curprojlist = [x for x in projlist if len(x.leafs())>=len(events) and set(events).issubset(x.leafs())] # get possible upstream projs   
                    
                    curprojlist = [x for x in curprojlist if cheapRest(x, projection, eventtype,  rates[eventtype] - optimisticRate)] #OLD and SLOW     
                    if curprojlist:                         
                        combinationdict[eventtype] = curprojlist + usingfilter  
                    #else:
                       # print("an cheap rest gescheitert "  + str(eventtype))
    
    return  combinationdict


def extractMsOptions(query):
    ''' returns all possible event types which can be partitioning input of a multisink projection '''
    MsOptions = []    
    #per query 
    myprojlist = [x for x in projsPerQuery[query]]
    for projection in myprojlist:
        dictionary = promisingChainProjection(projection)
        if dictionary.keys():
            for x in dictionary.keys():
                if not x in MsOptions:
                    MsOptions += x                
    return MsOptions
            

def estimatePC(projection):  # based on primitive inputs, here it should be taken into account that a projection may have a ms placement based on its primitive inputs
    pc = 0
    res = returnPartitioning(projection, projection.leafs(), criticalMSTypes)
    if res: #HAS MS
        partEvent = res[0]
        costs = res[1]        
        for event in [x for x in projection.leafs() if not x == partEvent]:
            pc += res[1] * rates[event]*len(nodes[event])  
    else:
        for event in projection.leafs():
            pc += longestPath * rates[event]*len(nodes[event])
    return pc
   


def MSoptionsPerEvent(query):
    events =  extractMsOptions(query) 
    MSOptionsDict = {}
    for event in events:
        MSOptionsDict[event] = []
        for proj in projlist:
            d = promisingChainProjection(proj)
            if event in d.keys():
                for upProj in [x for x in d[event] if len(x)>1]:
                    MSOptionsDict[event].append((proj, upProj))
    return MSOptionsDict

combiDict = {}
globalPartitioninInputTypes = {}
globalSiSInputTypes = {}

def getSavings(partType, combination, projection): #OPTIMISTIC TOTAL RATE

    myAllPairs = DistMatrices[MSTrees[partType]]      
    #bestNodeValue = min([sum(x) for x in myAllPairs if x]) #hier lieber average oder global average
    
    #TODO: it is not totalRate but only local Rate that we save for PartType
    if not projection.get_original(wl) in wl: #some intermediate projection
      #  return totalRate(partType) - (len(MSTrees[partType].edges())*  ((sum(list(map(lambda x: totalRate(x), [y for y in combination if not y == partType])))) + optimisticTotalRate(projection)))
         return longestPath * totalRate(partType) - (len(MSTrees[partType].edges())*  (sum(list(map(lambda x: totalRate(x), [y for y in combination if not y == partType])))) + longestPath * optimisticTotalRate(projection))
    
    elif projection.get_original(wl) in wl and not partType in list(map(lambda x: str(x), projection.get_original(wl).kleene_components())): #sink projection
        return  longestPath * totalRate(partType) - (len(MSTrees[partType].edges())*  sum(list(map(lambda x: totalRate(x), [y for y in combination if not y == partType])))) 
   
    elif projection.get_original(wl) in wl and partType in list(map(lambda x: str(x), projection.get_original(wl).kleene_components())): # ms sink query at kleene type 
        return longestPath * totalRate(partType) - (len(MSTrees[partType].edges())*  (sum(list(map(lambda x: totalRate(x), [y for y in combination if not y == partType])))) + longestPath * optimisticTotalRate(projection))

def getBestChainCombis(query, shared, criticalMSTypes, noFilter):         
    myMSDict = MSoptionsPerEvent(query)     
    myprojlist = [x for x in projsPerQuery[query]] # HERE WE NEED TO RESPECT OPERATOR SEMANTIC -> new function

    for projection in [x for x in myprojlist]: #trivial combination and ms placement for projections containing two prim events only
            partType = returnPartitioning(projection, projection.leafs(), criticalMSTypes)  
            if partType:                
                rest = [x for x in projection.leafs() if not x in partType]
                costs = getSavings(partType[0],[partType[0]] + rest, projection)
                combiDict[projection] = (projection.leafs(), partType, costs)
            else:
                costs = sum(list(map(lambda x: totalRate(x), projection.leafs()))) * longestPath
                combiDict[projection] = (projection.leafs(), [], 0 - costs)
                    
    
    for projection in sorted([x for x in myprojlist if len(x.leafs()) > 2], key = lambda x: len(x.leafs())):  # returns combination, that has only one input projection, the rest are primitive event types
            mycosts = 0
            for eventtype in myMSDict.keys():           
                for mytuple in myMSDict[eventtype]:
                    if projection == mytuple[1]: 
                        remainingEvents = list(set(mytuple[1].leafs()).difference(set(mytuple[0].leafs())))
                        mycombination = [mytuple[0]] + remainingEvents
                        res = returnPartitioning(projection, mycombination, criticalMSTypes)
                        curMSTypes = [eventtype]
                        if res:     
                            curcosts = getSavings(eventtype, mycombination, projection)                           
                            if mytuple[0] in combiDict.keys():   # upstream projection also has a ms placement such that we already saved something here
                                curcosts += combiDict[mytuple[0]][2]
                            if curcosts > mycosts: # update with new best chain combination
                                if not projection in combiDict.keys():
                                    combiDict[projection] = []
                                mycosts = curcosts
                                combiDict[projection] = (mycombination, [eventtype], mycosts)
                                # if a component of the combination is not in combidict, this means that it has no ms placement, however, we need to add it to combidict, to exclude bad combinations later
                                if not mytuple[0] in combiDict.keys():
                                    combiDict[mytuple[0]] = (mytuple[0].leafs(), [], 0)
                                           
           
            mylist = [x for x in myprojlist if len(x.leafs()) < len(projection.leafs()) and set(x.leafs()).issubset(projection.leafs())]     
            getBestTreeCombiRec(query, projection, mylist, [], 0, shared , criticalMSTypes)

    return combiDict

def getBestTreeCombiRec(query, projection, mylist, mycombi, mycosts, shared, criticalMSTypes): # atm combinations are generated redundantly and also performance could be improved with a hashtable [ -> the projections with which ABC could be combined in a combination for ABCDE are a subset of the projections AB can be combined...]
    if mylist:
        for i in range(len(sorted(mylist, key = lambda x: len(x.leafs())))): 
            proj = mylist[i]
            subProjections = sorted(mylist, key = lambda x: len(x.leafs()))[i:] #problematic
            
            combiBefore = [x for x in  mycombi]
            mycombi.append(proj)             
            
            ##### fill each intermediate combination with primitive events to generate new combination 
            _missingEvents =   list(set(projection.leafs()).difference(set(''.join(map(lambda x: ''.join(x.leafs()), mycombi)))))
            _missingEvents += mycombi 
            getBestTreeCombiRec(query, projection, [], _missingEvents, mycosts, shared, criticalMSTypes)
            
            #exclude redundant combinations
            mycombiEvents = ''.join(map(lambda x: ''.join(x.leafs()), mycombi))
            subProjections = [x for x in subProjections if not set(x.leafs()).issubset(set(list(mycombiEvents))) and not set(list(mycombiEvents)).issubset(set(x.leafs()))]
            
            #exclude the projections of the list in which the partitioning input type of proj is element of the leafs
            if proj in combiDict.keys() and  combiDict[proj][1]:
                 partProj = combiDict[proj][1][0]
                 subProjections = [x for x in subProjections if not partProj in x.leafs()]            
                 #exclude case in which part proj of other projection in the list is part of projs leafs
                 subProjections = [x for x in subProjections if not (x in combiDict.keys() and  combiDict[x][1] and  combiDict[x][1][0] in proj.leafs())]
            
            #TODO -> Check on Paper and check Implementation carefully
            # exclude subprojections in which the events covered by multi-sink placement are a subset of those events covered by the projections in the combination so far
            myMSTypes = sum([allMSTypes(x) for x in mycombi if x in combiDict.keys()],[])                  
            subProjections = [x for x in subProjections if not (x in combiDict.keys() and set(allMSTypes(x)).issubset(set(myMSTypes)))]
        
            
            # exclude the projection in which one of the partProjs of the combination so far is used as input of a single sink placement of an ancestor
            allSiSTypes = sum([allSiSEvents(x) for x in mycombi if x in combiDict.keys()],[])  #get SIS events, i e those that are covered by combi but not in MS types and remove all projections having ms events that intersect 
            subProjections = [x for x in subProjections if not (x in combiDict.keys() and set(allMSTypes(x)).intersection(set(allSiSTypes)))]
            subProjections = [x for x in subProjections if not (x in combiDict.keys() and set(allSiSEvents(x)).intersection(set(myMSTypes)))]   
            
            # NEW: exlude combinations with subprojections whichs parttypes would cause to exceed a parttype threshold, here it would be nice to keep a set of good candidates for each projection
            subProjections = [x for x in subProjections if not globalPartitioningOK(query, mycombi + [x])]
      
            getBestTreeCombiRec(query, projection, subProjections, mycombi, mycosts, shared, criticalMSTypes)
            mycombi =  combiBefore
            
    else:  
       if not mycombi or set(sum([[x] if len(x) == 1 else x.leafs() for x in mycombi],[])) != set(projection.leafs()):  #not even one ms placeable subprojection exists ?
           return
       
       else: # only correct combination which match the projection 
       
                       (mycosts, partEvent) = costsOfCombination(projection, mycombi, shared, criticalMSTypes)  
                       
                       if not projection in combiDict.keys():             # projection has only sis placement and thus was not in combidict before
                           combiDict[projection] = (mycombi, partEvent, mycosts)         
                       if mycosts > combiDict[projection][2]:
                           combiDict[projection] = (mycombi, partEvent, mycosts)
                       
       

def costsOfCombination(projection, mycombi, shared, criticalMSTypes): # here is a good spot to check the combinations that are actually enumerated during our algorithm
       
       mycosts = 0
       
       for proj in [x for x in mycombi if x in combiDict.keys()]: # add savings per input of combination
           mycosts += combiDict[proj][2]
   
       # check if it has a multi-sink placement and add costs/savings
       partEvent = returnPartitioning(projection, mycombi, criticalMSTypes)
       
       if partEvent:           
           mycosts += getSavings(partEvent[0], mycombi, projection)
       
       else: #projection has a single sink placement, such that we need to send th total rates of all inputs of the combination average path length at least once
          mycosts -= (sum(list(map(lambda x: totalRate(x), [y for y in mycombi if y in combiDict.keys() and not combiDict[y][1]])))) * longestPath 
           
       # reduce by primitive events and shared subprojection
       mycosts -= sharedAncestorsCost(projection, mycombi, partEvent)
                
       #if multiple projections share the same input, add a little bit of that inputs rate to simulate later sharing oportunities -> extend myMSTypes to dictionary   
       mycosts += eventSharing(projection, mycombi, mycosts, shared) # rates of event types input to multiple multi-sink placement in the combination are shared, which should be accounted for here
       
       #TODO: this might be stupid in the case of multiquery
       MSChildren = sum([combiDict[x][1] if len(x) > 1 else [x] for x in mycombi ],[])           
       if (len(MSChildren) != len(mycombi) and not partEvent):
               mycosts =  -np.inf
           
       
       return (mycosts, partEvent) 

# def eventSharing_old(projection, mycombi, mycosts, shared): 
#     # output costs of inputs of multi-sink placements that are shared between multiple projections of the combination
    
#     costs = 0
#     # for each projection in mycombi, get all SIS events and generate Dict
#     mySiSEvents =  sum([allSiSEvents(x) for x in mycombi if x in combiDict.keys()], [])
#     SiSDict =  {x : mySiSEvents.count(x) for x in set(mySiSEvents)}  
#     mySubProjections = sum([allAncestors(x, combiDict[x][0]) for x in mycombi if x in combiDict.keys()], [])
#     mySubProjections += [x for x in mycombi if x in combiDict.keys()]
#     SiSDict.update({x :  mySubProjections.count(x) for x in set(mySubProjections)})
    
#     #list containing all projections and primitive event types, that are input to single-sink placements for queries for which combination already computed
#     globalSiSEvents = []   
#     if shared:  
#         globalSiSEvents = sum([allSiSEvents(x) for x in wl if x!= projection and x in combiDict.keys()],[])  
#         globalSiSEvents += sum([allAncestors(x, combiDict[x][0]) for x in wl if x!= projection and x in combiDict.keys()],[]) #sharedSubprojections         
            
#     for event in SiSDict.keys():
#         if event in globalSiSEvents: # for multi-query scenario
#             costs += totalRate(event) * longestPath * SiSDict[event]
#         else:
#             costs += totalRate(event) * (SiSDict[event] - 1) * longestPath #TODO prefer something about the tree edges
   
#     return costs


def eventSharing(projection, mycombi, mycosts, shared): 
    # output costs of inputs of multi-sink placements that are shared between multiple projections of the combination
    costs = 0
    # get for the sub-graph representing the combination of each projection in mycombi the ms placed sub-projections
    myInputsMSProjs = {}
    for proj in [x for x in mycombi if len(x) > 1] + [y for y in wl if y in combiDict.keys()]: # check sharing with already processed other queries
        myInputsMSProjs[proj] = [x for x in allAncestors(proj, combiDict[proj][0]) if combiDict[x][1]] # list of ms ancestors
        myInputsMSProjs[proj] = list(set(sum([[y for y in combiDict[x][0] if not y == combiDict[x][1][0]] for x in myInputsMSProjs[proj]], [])))    
    myInputs = set(sum(list(myInputsMSProjs.values()),[]))
    totalInputs = sum(list(myInputsMSProjs.values()),[])
    for event in myInputs:
            costs += totalRate(event) * longestPath * totalInputs.count(event)   
    return costs


def sharedAncestorsCost(projection, mycombi, partEvent): #for each partitioning event type covered in the combi, we can only reduce its total rate once from the total savings provided by the combi   
    costs = 0

    if partEvent:
       partEvent = [partEvent[0]]       

    partTypes =  sum([allMSTypes(x) for x in mycombi if len(str(x)) > 1] + [partEvent] ,[])

    partTypeDict = {x : partTypes.count(x) for x in set(partTypes)}
    
    
    ancestorProjs = sum([allAncestors(x, combiDict[x][0]) for x in mycombi if x in combiDict.keys()], [])
    ancestorProjs += [x for x in mycombi if x in combiDict.keys()]
    ancestorDict = {x : ancestorProjs.count(x) for x in set(ancestorProjs)}  
    

    # this has two parts, first for shared subprojections, we reduce by the costs/savings of the shared projection (which is less than the rate of the primevents)   
    for anc in ancestorDict.keys():
        if ancestorDict[anc] > 1:
        
            costs += (ancestorDict[anc] - 1) * combiDict[anc][2]
            if combiDict[anc][1]: # ms ancestor
                partTypeDict[combiDict[anc][1][0]] -= ancestorDict[anc] - 1
                
    # then , we reduce by the savings for all partitioning primitive event types that are part of multiple different projections 
    for partProj in partTypeDict.keys():
        myAllPairs = DistMatrices[MSTrees[partProj]]      
        # bestNodeValue = min([sum(x) for x in myAllPairs if x])
        costs += (partTypeDict[partProj] - 1) * totalRate(partProj) * longestPath 
    
    return costs

    
def allSiSEvents(projection):    
    MSTypes = allMSTypes(projection)
    #return list(set(list(''.join(map(lambda x: ''.join(x.leafs()),  projections)))).difference(set(MSTypes)))
    return list(set(projection.leafs()).difference(set(MSTypes)))

def allMSTypes(projection):    
    if projection in combiDict.keys():
        MSTypes = [combiDict[x][1][0] for x in allAncestors(projection, combiDict[projection][0]) + [projection] if x in combiDict.keys() and combiDict[x][1]]
      
        return [x for x in list(set(MSTypes)) if len(str(x)) == 1] # quatsch, trees müssen aus output von partproj raus
    else:
        return []

def allAncestors(projection, mycombi):
    ancestors = []
    if len(projection.leafs()) == 2: # has no complex ancestors
        return ancestors   
    else:        
        for i in mycombi:   
            
            if len(i)>1: # is a complex event 
                ancestors.append(i)               
                if i in combiDict.keys(): # is something which has a combination
                    ancestors += allAncestors(i, combiDict[i][0])                
    return list(set(ancestors))  

 
def globalPartitioningOK(projection, combination):     #TODO: current version oversees the sharing potential with other projections with which the costs of those inputs are shared
    additionalCriticals = []
    myMSDict = {}
    ancestors = allAncestors(projection, combination)

    myMSTypes = sum([allMSTypes(x) for x in combination],[])
    myMSTypes = set([x for x in myMSTypes if myMSTypes.count(x) > 1]) # only partprojs used multiple times can be problematic
    for etype in set(myMSTypes):
        
        myMSDict[etype] = [x for x in ancestors if combiDict[x][1] and etype in combiDict[x][1]]
        myInputs = [x for x in list(set(sum([combiDict[y][0] for y in myMSDict[etype]],[]))) if not x == etype]
        mycosts = sum(map(lambda x: totalRate(x), myInputs)) * len(MSTrees[etype].edges())
        
        if longestPath * totalRate(etype) < mycosts:
            additionalCriticals.append(etype)
       
    return additionalCriticals        
    
    
    
   

def getExpensiveProjs(criticals):  # only on criticalTypes
    allProjs = sum([allAncestors(x.stripKL_simple(), combiDict[x.stripKL_simple()][0]) for x in wl], [])
    allMSProjs = [x for x in allProjs if combiDict[x][1] and combiDict[x][1][0] in criticals]
    
    #only if projection is input to single sink (or multisink?) 
    myMSProjs = [x for x in combiDict.keys() if set(allMSProjs).intersection(set(combiDict[x][0])).issubset(set(allMSProjs)) and combiDict[x][1] ]
    #the inputs are already part of other multi-sink placements (or if at least some of the inputs are already disseminated)
    for proj in allMSProjs:
        print(str(proj) +  " : " +  str(totalRate(proj)))
    print(list(map(lambda x: str(x), myMSProjs)))
    
    #
    #allExpensiveMSProjs = [outRateHigh(x) for x in allMSProjs]
    return #[combiDict[x][1][0] for x in allExpemensiveMSProjs if x in criticalTypes]

def outRateHigh(projection):
    combi = combiDict[projection][0]
    partType = returnPartitioning(projection, combiDict[projection][0])
    outRate = totalRate(projection) 
    return []

def unfold_combi(query, combination): #unfolds a combination, however in the new version we will have only one combination which is provided in the same format as the unfolded dict
    unfoldedDict = {}
    unfoldedDict[query] = combination    
    unfoldedDict.update(unfold_combiRec(combination, unfoldedDict))
    return unfoldedDict

def unfold_combiRec(combination, unfoldedDict): 
    
    for proj in combination:
        if len(proj) > 1:
            if proj in combiDict.keys():
                mycombination =  combiDict[proj][0]
            else:
                mycombination = proj.leafs() # this is the case if proj is a single sink projection, and we have to decide how to match it later
            unfoldedDict[proj] = mycombination
            unfoldedDict.update(unfold_combiRec(mycombination, unfoldedDict))
    return unfoldedDict 

 
def plotCombi(combi):
    G = nx.Graph()
    G.add_nodes_from(list(map(lambda x: str(x), combi.keys())))
    for query in wl:
        for e in query.leafs():
            if not e in G.nodes:
                G.add_node(e)
    for i in combi.keys():
        for k in combi[i]:
            G.add_edge(str(i),str(k))
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show() 
    

def main():
    criticalMSTypes= []
    noFilter = 0
    shared = 1
    if len(sys.argv) > 1: 
        noFilter = int(sys.argv[1])

        
    
    start_time = time.time()
    #random.shuffle(wl)
    for query in sorted(wl, key = (lambda x: len(projsPerQuery[x.stripKL_simple()])), reverse = True): #start with queries having the least projections, try other sortings...
 
        query = query.stripKL_simple()
        getBestChainCombis(query, shared, criticalMSTypes, noFilter)
        criticalMSTypes += allSiSEvents(query)# update sis placed projections here already
    end_time = time.time()
    
    combigenTime = round(end_time - start_time,2)
     
    globalMSTypes   = set(sum([allMSTypes(x.stripKL_simple()) for x in wl],[]))
    print("potentialMSTypes:  "  + str(globalMSTypes))
    globalSiSTypes  = set(sum([allSiSEvents(x.stripKL_simple()) for x in wl],[]))
    print("globalSiSTypes:  "  + str(globalSiSTypes))
    criticalMSTypes = list(set(globalMSTypes).intersection(set(globalSiSTypes)))
    
 #   criticalMSTypes += globalPartitioningOK(wl[0], wl) # add parttypes to ciritcalMSTypes that exceed global threshold
    
    # check if critical MSTypes share inputs with other MS placements in their SiS Projections

    print("critical Types " + str(criticalMSTypes))
   # print(globalPartitioningOK(wl[0], wl))
   
    # use globalPartitioningOK in order to identify more critical MS Types
    
    # use getExpensiveProjs to identify cases in which although critical an MS placement is superior over a Sis placement due to the outrate of a projection
    #getExpensiveProjs(criticalMSTypes) # get expensive projections and check if a ms placement exists at a criticaltype, weigh against estimated input costs and remove from criticals

    # check of each Projection which is SIS placed, if a multi-sink placement exists due to event sharing
    
    
    
    
    
    #print("globalMSTypes: " + str(set(globalMSTypes).difference(set(criticalMSTypes))))

    # EXPERIMENT -> Idea: If a combination of a query has no multi-sink placement (because its forbidden by criticalevents), just enforce primitive combination as it is probably even more expensive to match multiple sis projections and send around projections etc.
    # make this smarter by also removing parts of the combination treee that consist only of Single Sink Placements
    # TODO when is a chain of single sink better 
    
    # for query in wl:

    #     if set(allMSTypes(query)).issubset(set(criticalMSTypes)):
    #         combiDict[query] = (query.leafs(), [], 0)
            
    curcombi = {}
    
            
    for i in range(len(wl)):   
        query = wl[i].stripKL_simple()
        if query in combiDict.keys():
            curcombi.update(unfold_combi(query, combiDict[[query][0]][0]))    

 
    mycombi = curcombi
    criticalMSProjs = [x for x in mycombi.keys() if combiDict[x][1] and combiDict[x][1][0] in criticalMSTypes]

    #plotCombi(mycombi) # plot combination graph
    
    
    for pro in curcombi.keys():
        print(str(pro) + " " + str(list(map(lambda x: str(x), curcombi[pro]))))
    print("time: " + str(end_time - start_time))   
    print(numberCombis)
     
   # getExpensiveProjs(criticalMSTypes)
    
    with open('curcombi',  'wb') as newcombi:
        pickle.dump(mycombi, newcombi)
        
    with open('originalCombiDict', 'wb') as combidict:
        pickle.dump(combiDict, combidict)
        
    with open('criticalMSTypes',  'wb') as criticaltypes:
         pickle.dump([criticalMSTypes, criticalMSProjs], criticaltypes)
        
    with open('filterDict',  'wb') as filterDict_file:
        pickle.dump(projFilterDict , filterDict_file)  
    
    # export number of queries, computation time combination, maximal query length, TODO: maximal depth combination tree, portion of rates saved by multi-sink eventtypes
    combiExperimentData = [len(wl), combigenTime, max(len(x) for x in wl), len(projlist)] 
    with open('combiExperimentData',  'wb') as combiExperimentData_file:
        pickle.dump(combiExperimentData , combiExperimentData_file)  
        
if __name__ == "__main__":
    main()