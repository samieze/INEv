#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 13:18:01 2021

@author: samira
"""
#from EvaluationPlan import *
import pickle
import string
import subsets as sbs 
import math
import sys
import numpy as np
#from processCombination import *





with open('network',  'rb') as  nw_file:
        nw = pickle.load(nw_file)

with open('selectivities', 'rb') as selectivity_file:
    selectivities = pickle.load(selectivity_file) 
    
with open('current_wl', 'rb') as wl_file:
    wl = pickle.load(wl_file)     
    
#with open('EvaluationPlan', 'rb') as EvaluationPlan_file: 
 #         myplan = pickle.load(EvaluationPlan_file)
          
#with open('CentralEvaluationPlan', 'rb') as CentralEvaluationPlan_file: 
 #         centralPlan = pickle.load(CentralEvaluationPlan_file)

# ID = myplan[1]
# MSPlacements = myplan[2]
# myplan = myplan[0]
          
# cdict = centralPlan[1]
# csource = centralPlan[0]
# wl = centralPlan[2]
# evaluationDict = {}
# combinationDict = {}
# evaluationDict = {x: [] for x in range(len(nw))}
# forwardingDict = {}       
# selectionRate = {}
# filterDict = {}
# sinkDict = {}


def getCom(mylist):
    return [(mylist[i],mylist[i+1]) for i in range(len(mylist)) if i < len(mylist) -1 ]    

def traverseList(source, mylist): 

    for i in range(len(mylist)):

        if mylist[i]==source[0]:
            myindex = i
    firstpart = mylist[:myindex+1]
    firstpart.reverse()
    secondpart = mylist[myindex:]    
    mytuples = getCom(firstpart)
    mytuples += getCom(secondpart)
    return mytuples

def traverseListTuples(source, mytuples): 
    sources = source
    myPairs = []
    while mytuples:
        toRemove = []
        for i in mytuples:
            curSource = list(set(sources).intersection(set(i)))            
            if curSource:
               newInd = i.index(curSource[0])
               newInd = not newInd               
               pair = (curSource[0],i[int(newInd)])
               myPairs.append(pair)            
               sources.append(pair[1])
               toRemove.append(i)
        mytuples = [x for x in mytuples if not x in toRemove]
    return myPairs  
   
def processInstance(instance):
    
    routingTuples = []
    instanceDict = forwardingDict[instance.projname][instance.name]

   
    for path in instance.routingDict.values():
        if type(path[0]) == list:
            for mypath in path:
                routingTuples.append(traverseList([mypath[len(mypath)-1]], mypath))
        elif type(path[0]) == int:
            routingTuples.append(traverseList(instance.sources, path))
        else:
            routingTuples.append(traverseListTuples(instance.sources,  path))           
    for path in routingTuples:
        for mytuple in path:
            if not mytuple[0] in instanceDict.keys():
                 instanceDict[mytuple[0]] = []
            instanceDict[mytuple[0]].append(mytuple[1])        
    return instanceDict        

def getSelectionRate(projection, combination):
    
    subsProj = set(sbs.printcombination(projection.leafs(),2))
    subsCombi = set(sum([sbs.printcombination(x.leafs(), 2) for x in combination if len(x)>1],[]))
    subsProj = subsProj.difference(subsCombi)    
    res = 1
    for i in [selectivities[x] for x in subsProj]:
        res *= i
    return res

# for i in myplan.projections: 
#     myproj = i.name
#     for filterTuple in myproj.Filters:
#         filterDict[filterTuple[0]] = filterTuple[1]     
#     for node in myproj.sinks:
#             evaluationDict[node].append(str(myproj.name))
                  
#     combinationDict[str(myproj.name)] = list(map(lambda x: str(x), myproj.combination.keys()))    # remove events used as filters
#     selectionRate[str(myproj.name)] = getSelectionRate(myproj.name, myproj.combination.keys())
#     sinkDict[str(myproj.name)] = [myproj.sinks,""]
#     if len(myproj.sinks):
#         for proj in myproj.combination.keys():
#              for instance in myproj.combination[proj]:                  
#                  if instance.sources == myproj.sinks:
#                      sinkDict[str(myproj.name)][1] = instance.projname
#     for instancelist in myproj.combination.keys():
#         for instance in myproj.combination[instancelist]: 
#                 if not instance.projname in forwardingDict.keys():
#                     forwardingDict[instance.projname] = {}
#                 if instance.projname in forwardingDict.keys() and not instance.name in forwardingDict[instance.projname].keys():   
#                     forwardingDict[instance.projname][instance.name] = {}
#                 if list(instance.routingDict.keys()):    
#                     forwardingDict[instance.projname][instance.name] = processInstance(instance)
                    
                    

# filterdict: proj: [filter, remainingproj, resultingcombination]
def newFilterDict():
    newDict = {}
    for proj in filterDict.keys():
        myfilter = filterDict[proj]        
        # subproj = settoproj(list(set(proj.leafs()).difference(set(list(myfilter)))), proj)
        subproj = list(set(proj.leafs()).difference(set(list(myfilter))))# atm only single events send for filters
        newDict[str(proj)] = [myfilter,subproj,[subproj]+list(myfilter)]
    return newDict


      
def sepnumbers(evlist):
    """ "A1B" -> [A1,B] """   
    newevlist = []
    if (len(evlist) > len(filter_numbers(evlist))):            
        for i in range(len(evlist)):   
            if  evlist[i] in list(string.ascii_uppercase):
                newevlist.append(evlist[i])
            else:                 
                newevlist[len(newevlist)-1] = newevlist[len(newevlist)-1] + str(evlist[i])               
    else:
        newevlist = evlist
    return newevlist

def filter_numbers(in_string):
    x = list(filter(lambda c: not c.isdigit(), in_string))    
    return "".join(x)

def filter_literals(in_string):
    x = list(filter(lambda c: c.isdigit(), in_string))    
    return "".join(x)

def toETB(instance):
    text = ""
    parts = sepnumbers(instance)
    for ev in parts:
        mytype = filter_numbers(ev)
        mynode = filter_literals(ev)
        if mynode:
            text += "("+str(mytype)+": node" + str(mynode) +");"
        else:
            text += "("+str(mytype)+": ANY);"
        
    text = text[:-1]
    return text

def nodelist(mylist):
    mylist = list(set(mylist)) 
    text = "["
    for i in mylist:
        text+= "node"+ str(i) +";"
    text= text[:-1]
    text += "]"
    return text

def listStr(mylist):
    text = ""
    for i in mylist:
        text += str(i) + ","
    return text[:-1]


def forwardingRule(i):
    text = "Forward rules:\n"
    for projection in forwardingDict.keys():
        for instance in forwardingDict[projection].keys():  
            post = []
            instanceText = ""
            if str(projection) in filterDict.keys():
                    instanceText += listStr((filterDict[str(projection)][1]))+"|"+str(projection) + " - [ETB:" + toETB(instance) + " FROM:"
            else:    
                    instanceText += str(projection) + " - [ETB:" + toETB(instance) + " FROM:"
            for node in forwardingDict[projection][instance].values():    
                     pre = [p for p in forwardingDict[projection][instance].keys() if i in forwardingDict[projection][instance][p]]
                     if i in forwardingDict[projection][instance].keys():                        
                         post = forwardingDict[projection][instance][i]  
                     else:
                         post = []
                         
            if post:
                if not pre:
                    pre = [i]
                instanceText += nodelist(pre) + " TO:" + nodelist(post) + "] \n"
                text += instanceText
    return text  


def forwardingRuleCentral(i, myForwardingDict):
    text = "Forward rules:\n"
    
    for projection in myForwardingDict.keys():
        for instance in myForwardingDict[projection].keys():  
            post = []
            instanceText = ""
            instanceText += str(projection) + " - [ETB:" + toETB(instance) + " FROM:"
            for node in myForwardingDict[projection][instance].values():    
                     pre = [p for p in myForwardingDict[projection][instance].keys() if i in myForwardingDict[projection][instance][p]]
                     if i in myForwardingDict[projection][instance].keys():
                         post = myForwardingDict[projection][instance][i]
                     else:
                         post = []
            if post:
                if not pre:
                    pre = [i]
                instanceText += nodelist(pre) + " TO:" + nodelist(post) + "] \n"
                text += instanceText
    return text  

def adjustRoutingCentral(mydict, source):
    outdict = {}
    for proj in mydict.keys():
        outdict[proj] = {}
        for instance in mydict[proj]:
            outdict[proj][instance] = {}
            mysource = int(filter_literals(instance))
            routingTuples = traverseList([mysource], mydict[proj][instance])
            for mytuple in routingTuples:
                    if not mytuple[0] in outdict[proj][instance].keys():
                            outdict[proj][instance][mytuple[0]] = []
                    outdict[proj][instance][mytuple[0]].append(mytuple[1])
    return outdict    

   
 

def processingText():
    text = "muse graph \n"
    for q in wl:
         text += "SELECT " + str(q) + " FROM "
         for l in q.leafs():
            text += l +"; "
         text = text[:-2]  
         text += " ON {0}/n(A)"
         text += "\n"    
    return text  


def networkText():
    myTypes = list(set(sum([x.leafs() for x in wl], [])))
    mystr = "network \n"
    for i in range(len(nw)):    
        mystr += "Node " + str(i) + " " + str(nw[i])   +"\n"
        
    return mystr


def selectivitiesText():
    return "selectivities \n" + str(selectivities) + " \n"

def queriesText():
    mystr = "queries \n"
    for i in wl:
        mystr += str(i) + "\n"
    return mystr

def generatePlan():
    text  = ""
    text += networkText() + "\n"
    text += "\n"
    text += selectivitiesText() + "\n"
    text += queriesText() + "\n"
#    text +="Randomized Rate-Based Primitive Event Generation\n"
#    text +="-----------\n"
    text += processingText()
    return text
def main():
    if len(sys.argv) > 1: 
        ID = sys.argv[1]
    else:
        ID = int(np.random.uniform(0,10000000))
    f = open("plans/" + str(ID) +".txt", "w")   
    f.write(generatePlan()) 
    f.close()
            

if __name__ == "__main__":
    main()
