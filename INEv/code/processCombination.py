#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 11:47:10 2021

@author: samira
"""
from functools import reduce
from generate_projections import *

with open('curcombi',  'rb') as  combi_file:
        mycombi = pickle.load(combi_file)
        
with open('originalCombiDict', 'rb') as combiDict_file:
        originalDict = pickle.load(combiDict_file)
        
with open('criticalMSTypes', 'rb') as critical:
      criticalMSTypes = pickle.load(critical)
        
with open('filterDict', 'rb') as filterDict_file:
        filterDict = pickle.load(filterDict_file)    

criticalMSProjections = criticalMSTypes[1]
criticalMSTypes = criticalMSTypes[0]

def compute_dependencies(combiDict):# has as input a final combination
    ''' outputs a dictionary which has as keys the projections of a final combination and as corresponding key the level of the projection in the muse graph, for sis and ms projections having the same level, level for msp is increased as placements can be exploited here'''         
    levels = {}
    for proj in combiDict.keys():
        if len(proj.leafs()) == 2 or set(combiDict[proj]) == set(proj.leafs()):
            levels[proj] = 0           
            
    for proj in sorted([x for x in combiDict.keys() if not x in levels.keys()], key= lambda z: len(z.leafs())): # mit vorsicht zu genießen
        mymax = max(list(map(lambda x: levels[x], [x for x in combiDict[proj] if x in combiDict.keys()])))
        levels[proj] = mymax + 1
    
    # increase level  of projections having msp          
    for proj in levels.keys():
        levels[proj] = levels[proj] * 2
    for proj in levels.keys():
        if not returnPartitioning(proj, combiDict[proj], criticalMSTypes):
            levels[proj] = levels[proj]  + 1

    return levels    


def copy_allAncestors(projection, mycombi):
    ancestors = []
    if len(projection.leafs()) == 2: # has no complex ancestors
        return ancestors   
    else:        
        for i in mycombi[projection]:               
            if len(i)>1: # is a complex event 
                ancestors.append(i)               
                if i in mycombi.keys(): # is something which has a combination
                    ancestors += copy_allAncestors(i, mycombi)                
    return list(set(ancestors))  
    

def compute_dependencies_alt(unfolded):
    myProjections = list(unfolded.keys())
    myMS = [x for x in myProjections if returnPartitioning(x, unfolded[x], criticalMSTypes)]
    mySiS = [x for x in myProjections if not x in myMS]
    Order = {x: copy_allAncestors(x, unfolded) for x in unfolded.keys()}
    preOrder = myMS + mySiS
    myCopy = copy.deepcopy(preOrder)
    for i in range(len(preOrder)):
         for subProj in [x for x in unfolded[preOrder[i]] if len(x) >1 ]:
            index2 = myCopy.index(subProj)
            if index2 > myCopy.index(preOrder[i]):
               myCopy =  prePone(myCopy, myCopy.index(preOrder[i]), index2)
    return myCopy
    
 
def prePone(mylist, index1, index2):
    toPop = mylist[index2]
    return [mylist[x] for x in range(len(mylist)) if x < index1] + [mylist[index2]] + [mylist[index1]] +[ x for x in  mylist[index1+1:] if not x == toPop]
    
    

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


def getSharedMSinput(combiDict, myProjFilters): 
    ''' for each ms projection in final combination, check if there is an input in the current combination, that is shared with another ms projection, output is shared dict, which is used for MS placements'''
    sharedInput = {}
    for proj in combiDict.keys():        
        part = returnPartitioning(proj, combiDict[proj], criticalMSTypes)                  
        if part: # only MS projections
            for event in combiDict[proj]:
            #for event in combiDict[proj] + list(getMaximalFilter(myProjFilters, proj)):
                if not event in sharedInput and not part[0] == event:
                    sharedInput[event] = [part[0]]
                elif not part[0] == event: 
                    sharedInput[event].append(part[0])
    return sharedInput
             
def makeUnredundant(combi):
    toRemove = []
    for i in combi:
            myset = set([x if len(x) == 1 else x.leafs() for x in [i]][0])
            for k in [x for x in combi if x != i]:
                outSet = set([x if len(x) == 1 else x.leafs() for x in [k]][0])
                if myset.issubset(outSet):
                    toRemove.append(i)
    return [x for x in combi if not x in toRemove]
            
def removeLayer(combiDict, layer): # make sure, that no query is removed from 
    levels = compute_dependencies_simple(combiDict)
    #levels = compute_dependencies(combiDict) 
    projections = [x for x in levels.keys() if levels[x] in layer and not x in wl]
    myCombination = copy.deepcopy(combiDict)    
    for l in sorted(layer):
        newCombination = {}
        for i in sorted([x for x in myCombination.keys() if not levels[x]==l], key = lambda y: len(y.leafs())): # change only for projs with layer
            newCombination[i] = sum([[x] if not (x in levels.keys() and levels[x]==l) else myCombination[x] for x in myCombination[i]],[])
        myCombination = copy.deepcopy(newCombination)
    newCombination = {x : makeUnredundant(list(set(newCombination[x]))) for x in list(newCombination.keys())}        
    return newCombination 


def removeProjection(combiDict, projection):
    combi = mycombi[projection]
    myCombination = copy.deepcopy(combiDict)
    newCombination = {}
    for i in [x for x  in combiDict.keys() if not x == projection]:
        newCombination[i] = sum([[x] if not (x==projection) else combi for x in myCombination[i]],[])
    return {x : makeUnredundant(list(set(newCombination[x]))) for x in list(newCombination.keys())}        

def hasMSParent(projection): # checks for a projection if it is input to a MS placement
     for i in mycombi.keys():
        if projection in mycombi[i]:
           if originalDict[i][1] and not i in criticalMSProjections:
               return True
     else:
         return False
     
def removeSisChains():    
    levels = compute_dependencies_simple(mycombi)
    newlevels = {}
    toRemove = []
    for x in levels.values():
        newlevels[x] = []
        for k in levels.keys():
            if x == levels[k]:
                newlevels[x].append(k)

    for i in [x for x in newlevels.keys() if not x == max(newlevels.keys())]:
        count = 0
        for proj in [x for x in newlevels[i] if not x in wl]:
            if originalDict[proj][1] or hasMSParent(proj): #has multisink placement
                break;
            elif proj in criticalMSProjections:
                count += 1
            else:
                count += 1
        if count == len(newlevels[i]):
            toRemove.append(i)
    newcombi = copy.deepcopy(mycombi)        
    if toRemove:       
        newcombi = removeLayer(mycombi,toRemove)        
    newcombi = removeSiSfamilies(newcombi)  
    return  newcombi    

def removeSiSfamilies(combi):
    toRemove = []
    for i in [x for x in combi.keys() if not x in wl]:
        if not originalDict[i][1] and not hasMSParent(i):
            toRemove.append(i)
        elif i in criticalMSProjections:
            toRemove.append(i)
    newcombi = combi    
    for i in toRemove:
        newcombi = removeProjection(newcombi,i)
    return newcombi    

def strToProj(subProj, projection):
    if isinstance(subProj, Tree):
        return subProj
    elif len(subProj) == 1:
        return subProj
    else:
        evlist = []
        for i in range(len(subProj)):            
            if not (i == 0 or i== len(subProj)-1): 
                if not subProj[i-1] in list(string.ascii_uppercase) and not subProj[i+1] in list(string.ascii_uppercase):
                    evlist.append(subProj[i])
        return(settoproj(evlist,projection))   

def getDiv(i, partType):
    if len(i)==1:
        if i == partType:
            return instances[partType]
        return 1
    elif partType in i.leafs():
        return instances[partType]
    return 1
        

def getFilteredRate(projection, diamond, filtered):
     if len(diamond) == 1:        
        if diamond in filtered:    
            return singleSelectivities[getKeySingleSelect(diamond, projection)] * totalRate(diamond)
        return totalRate(diamond)
    
     lst = [x for x in diamond.leafs() if x in filtered] #return list of filtered events contained in projection
     filter_lst = [x for x in diamond.leafs() if not x in lst]
     lst  = list(map(lambda x: singleSelectivities[getKeySingleSelect(x, projection)], lst))
     filter_lst = list(map(lambda x: singleSelectivities[getKeySingleSelect(x, diamond)], filter_lst))
     prod = 1
     for i in lst + filter_lst:
             prod *= i
     return diamond.evaluate() *  getNumETBs(diamond) * prod

    
    
def Diamond_costsFiltered(projection, diamonds, filtered):
    costs = 0 
    for diamond in diamonds:
        diamond1 = getFilteredRate(projection, diamond[0], filtered)
        diamond2 = getFilteredRate(projection, diamond[1], filtered)
        costs += diamond1 + diamond2 + diamond1 * diamond2
    return costs
    
def Diamond_costs(projection, diamonds, partType):
    costs = 0
    div = False
    for i in diamonds:
        div0 = getDiv(i[0], partType)
        div1 = getDiv(i[1], partType)    
        costs += totalRate(i[0])/div0 +  totalRate(i[1])/div1 +  totalRate(i[0])/div0 * totalRate(i[1])/div1
    return costs  

def getMiniDiamonds(projection, partType, combination, *args): #args is list of filtered events
    samplingSize = 1 #len(combination) * 25 # TODO adjust to length/number of possibilities
    costs = np.inf
    outDiamonds = []    
    diamonds = []
   
    if args:
        filteredEvents = args[0]
        if len(args) > 1:
            samplingSize = args[1]
    else:
        filteredEvents = ""
        
    for i in range(samplingSize):
        originalDiamonds = copy.deepcopy(diamonds)
        mycosts = 0
        myDiamonds = getMiniDiamonds_rec(projection, partType, combination, originalDiamonds)
        if filteredEvents:
            mycosts = Diamond_costsFiltered(projection, myDiamonds, filteredEvents)
        else:
            mycosts = Diamond_costs(projection, myDiamonds, partType)
        if mycosts < costs:
            outDiamonds = myDiamonds
            costs = mycosts
    return outDiamonds

def getMiniDiamonds_rec(projection, partType, combination, diamonds):
    combination = list(map(lambda x: strToProj(x, projection), combination))
    if len(combination) == 2:
        diamondTuple = combination
        diamonds.append(diamondTuple)
        return diamonds
    else:
        curMax =  int(np.random.uniform(0,len(combination)))
        curMin =  int(np.random.uniform(0,len(combination)))
        if curMax == curMin:
           if curMax < len(combination) - 1:
               curMax +=1
           else:
               curMax -= 1
        diamondTuple = [combination[curMax],combination[curMin]]
        diamonds.append(diamondTuple)
        combination = [x for x in combination if not x in diamondTuple]
        #print([x.leafs() if len(x)> 1 else [x] for x in diamondTuple])
        combination.append(settoproj(sum([x.leafs() if len(x)> 1 else [x] for x in diamondTuple],[]), projection))
        
        return getMiniDiamonds_rec(projection, partType, combination, diamonds)

def getMSInputs():
    out = []
    for proj in mycombi.keys():
        part = originalDict[proj][1]
        if part:
            myInputs = [x for x in mycombi[proj] if not x==part[0] and len(x)== 1 and not part[0] in criticalMSTypes]
            out.append(myInputs)
    return(sum(out,[]))

def augmentProjFilters(old, additional, mylist):
    for proj in mycombi.keys():
        additionalFilters = []
        for event in mylist:
            if event in additional[proj].keys():
                additionalFilters.append(event)                
        oldFilter =  getMaximalFilter(old, proj, 0)
        additionalFilters = [x for x in additionalFilters if not x in oldFilter]
        newFilter = "".join(additionalFilters)
        old[proj][newFilter] = getDecomposed(additionalFilters, proj)
    return old
        

### this is for removing layers to save hops
#mycombi = removeSisChains()

#mycombi = removeLayer(mycombi, [0])

projFilterDict =  {}      

for proj in projlist:
    projFilterDict.update(returnProjFilterDict(proj))   
    
additionalProjFilter = returnAdditionalFilterDict()
additionalInputs = getMSInputs()
       
projFilterDict = augmentProjFilters(projFilterDict, additionalProjFilter, additionalInputs)
