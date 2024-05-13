#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 13:18:01 2021

@author: samira

Generate evaluation plan that can be processed by DCEP Engine from encoding of INEv graph and centralized evaluation, including routing information, output selectors etc.

"""
from EvaluationPlan import *
import pickle
import string
import subsets as sbs 
import math
import sys
import json
from processCombination import *





with open('network',  'rb') as  nw_file:
        nw = pickle.load(nw_file)

with open('selectivities', 'rb') as selectivity_file:
    selectivities = pickle.load(selectivity_file) 
    
with open('EvaluationPlan', 'rb') as EvaluationPlan_file: 
          myplan = pickle.load(EvaluationPlan_file)
          
with open('CentralEvaluationPlan', 'rb') as CentralEvaluationPlan_file: 
          centralPlan = pickle.load(CentralEvaluationPlan_file)

ID = myplan[1]
MSPlacements = myplan[2]
myplan = myplan[0]
          
cdict = centralPlan[1]
csource = centralPlan[0]
wl = centralPlan[2]
evaluationDict = {}
combinationDict = {}
evaluationDict = {x: [] for x in range(len(nw))}
forwardingDict = {}       
selectionRate = {}
filterDict = {}



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
    print(instance, routingTuples)    # -> [entry of routingdict]   
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
    return math.prod([selectivities[x] for x in subsProj])


projection_strings = {}

for i in myplan.projections: 
    myproj = i.name
    for filterTuple in myproj.Filters:
        filterDict[filterTuple[0]] = filterTuple[1]     
    for node in myproj.sinks:
            evaluationDict[node].append(str(myproj.name))
            if not str(myproj.name) in projection_strings.keys():
                projection_strings[str(myproj.name)] = myproj.name
                  
    
    combinationDict[str(myproj.name)] = list(map(lambda x: str(x), myproj.combination.keys()))    # remove events used as filters
    selectionRate[str(myproj.name)] = getSelectionRate(myproj.name, myproj.combination.keys())
    
    for instancelist in myproj.combination.keys():
        for instance in myproj.combination[instancelist]: 
                if not instance.projname in forwardingDict.keys():
                    forwardingDict[instance.projname] = {}
                if instance.projname in forwardingDict.keys() and not instance.name in forwardingDict[instance.projname].keys():   
                    forwardingDict[instance.projname][instance.name] = {}
                if list(instance.routingDict.keys()):    
                    forwardingDict[instance.projname][instance.name] = processInstance(instance)
                    

# filterdict: proj: [filter, remainingproj, resultingcombination]
def newFilterDict():
    newDict = {}
    for proj in filterDict.keys():
        myfilter = filterDict[proj]        
        # subproj = settoproj(list(set(proj.leafs()).difference(set(list(myfilter)))), proj)
        subproj = list(set(proj.leafs()).difference(set(list(myfilter))))# atm only single events send for filters
        newDict[str(proj)] = [myfilter,subproj,[subproj]+list(myfilter)]
    return newDict

def getQuery(i):
    for k in projsPerQuery.keys():
        if i in list(map(lambda x: str(x), projsPerQuery[k])):
            return k

filterDict = newFilterDict()
myFilteredInputs  = {}
for i in evaluationDict.keys(): #add filtered projections to evaluation Dict of nodes processing filtered inputs     
     projectionsToAdd = []
     for projection in evaluationDict[i]:         
            for subproj in combinationDict[projection]:
                if subproj in filterDict.keys():
                    projectionsToAdd.append(subproj)     
     myFilteredInputs[i] = list(set(projectionsToAdd))        
     
for i in combinationDict.keys():
    myquery = getQuery(i)
    newCombi = [strToProj(x, strToProj(i, myquery)) if len(x) > 1 else x for x in combinationDict[i]]     # TODO, find query of projection
    newCombi = makeUnredundant(newCombi)
    combinationDict[i] = list(map(lambda x: str(x), newCombi))
      
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
        text+= str(i) +","
    text= text[:-1]
    text += "]"
    return  list(set(mylist)) 

def listStr(mylist):
    text = ""
    for i in mylist:
        text += str(i) + ","
    return text[:-1]


def forwardingRule(i):
    text = "Forward rules:\n"
    routing_tuples = []
    routing_keys = []
    for projection in forwardingDict.keys():
        for instance in forwardingDict[projection].keys():
            routing_tuple = []
            post = []
            instanceText = ""
            if str(projection) in filterDict.keys(): #FILTER HELLO! USE FOR OUTPUTSELECTION
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
                #instanceText += nodelist(pre) + " TO:" + nodelist(post) + "] \n"
                #text += instanceText
 
            if post:
                routing_tuple =  [str(projection),nodelist(pre),nodelist(post)]
                
                if routing_tuple:
                    if not [str(projection),nodelist(pre)] in routing_keys:
                        routing_keys.append([str(projection),nodelist(pre)])
                        routing_tuples.append(routing_tuple) # make dict, dont append doubles, add my id and only node ids, send cavan

    return routing_tuples  


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

   
 

def processingRules(i):
    text = ""
    if evaluationDict[node]:
        text = "Projections to process:\n"
        for projection in evaluationDict[i]:
            text += "SELECT " + projection + " FROM "
            for i in combinationDict[projection]:
                if i in filterDict.keys():
                    
                        text += str(filterDict[i][1]) +"; "
                else:
                        text += i +"; "
            text = text[:-2]    
            text += " WITH selectionRate= " + str(selectionRate[projection]) + "\n"    
    return text  


def getSequenceTuples(sequenceDict):
    sequences = []
    for event in sequenceDict.keys():
        if sequenceDict[event]:
            for second in sequenceDict[event]:
                sequences.append((event,second))

    return sequences
def getIDConstraint(combination, query): # enrich with osdict
    if len(combination)>1:
        combi = [x.leafs() if len(x) > 1 else [x] for x in combination]
        return list(set(combi[0]).intersection(set(combi[1])))  
    elif query.hasKleene():
        return [x for x in query.leafs() if not x == query.kleene_components()[0]]
  #  return []   

def getSequenceCostraints(combination, query):
    querySequences = getSequenceTuples(query.getsequences())
    firstSequences = []
    secondSequences=[]
    if len(combination) > 1:
        if len(combination[0])>1:
            firstSequences = getSequenceTuples(combination[0].getsequences())
        else:
            firstSequences = []
    
        if len(combination[1])>1:
            secondSequences = getSequenceTuples(combination[1].getsequences())
        else:
            secondSequences = []
    totalSequences = [x for x in querySequences if not x in firstSequences + secondSequences]     
    return totalSequences

def processingRules_Diamonds(i,tw):  
    if evaluationDict[i]:
        queries = []
        for projection in evaluationDict[i]:                  
                subqueries = []
                inputs = []
                selectivties = []
                sequence_constraints = []
                id_constraints = []
                myquery = getQuery(projection)             
                if projection in MSPlacements.keys():
                    partType = MSPlacements[projection] # TODO get parttype from combi/proj 
                else:
                    partType =  ""
                mycombination = combinationDict[projection]
                    #mySelRate = selectionRate[projection]
                    #mySelRate = return_selectivity(projection.leafs())
                #TODO: appropriate Rate for filter case    
                myDiamonds = getMiniDiamonds(strToProj(projection,myquery), partType, mycombination, "", 1000)              
                for diamond in myDiamonds:
                    mySelRate =  return_selectivity(settoproj(sum([x.leafs() if len(x)> 1 else [x] for x in diamond],[]), myquery).leafs())
                    for sub in diamond:
                        if len(sub) > 1:
                            mySelRate = mySelRate / return_selectivity(sub.leafs()) #Correct?
                    #JSON FIELDS
                    subqueries.append(str(settoproj(sum([x.leafs() if len(x)> 1 else [x] for x in diamond],[]), query)))
                    inputs.append([str(x) for x in diamond])
                    sequence_constraints.append(getSequenceCostraints(diamond,settoproj(sum([x.leafs() if len(x)> 1 else [x] for x in diamond],[]), myquery))) # call sequence constraints for dimaondquery, diamond
                    id_constraints.append(getIDConstraint(diamond,settoproj(sum([x.leafs() if len(x)> 1 else [x] for x in diamond],[]), myquery)))              
                    selectivties.append(mySelRate)
                json_subquery =  {"query_length": len(projection_strings[projection].leafs()), # problem projection is no query
                "predicate_checks": 1,
                "query_name": str(projection),
                "output_selection": projection_strings[projection].leafs(), #TODO, parse filter dict
                "subqueries": subqueries,
                "inputs": inputs,
                "selectivities": selectivties,
                "sequence_constraints": sequence_constraints,
                "is_negated": 0,
                "kleene_type": 0,
                "context": [],
                "id_constraints": id_constraints,
                "time_window_size": 60 * tw}    
                queries += [json_subquery]    
                 
                   
                # name = projection, output_selection = filters, rest = rest    
                
    # if myFilteredInputs[i]:    
    #     for projection in myFilteredInputs[i]:
    #             myquery = getQuery(projection)          
    #             mycombination = strToProj(projection,myquery).leafs()     
    #             partType = ""
    #             myFilter = filterDict[projection][0]
    #             myDiamonds = getMiniDiamonds(strToProj(projection,myquery), partType, mycombination, filterDict[projection][1])   
    #             filterstring = ''.join(mycombination)
    #             mySelRate = 1
    #             for diamond in myDiamonds:
    #                  diamondProj = settoproj(sum([x.leafs() if len(x)> 1 else [x] for x in diamond],[]), myquery)
    #                  if myFilter in diamondProj.leafs():
    #                      mySelRate = singleSelectivities[getKeySingleSelect(myFilter,  diamondProj)]
    #                  if not str(diamondProj) == (projection):
    #                      text += "SELECT " + str(diamondProj) + "|" + filterstring + " FROM "
    #                  else: 
    #                      text += "SELECT " + str(diamondProj) + " FROM "
    #                  for sub in diamond:
    #                     if not sub == myFilter:
    #                         text += str(sub) + "|" + filterstring + "; "    
    #                     else:
    #                          text += str(sub) +"; "
    #                  text = text[:-2]        
    #                  text += " WITH selectionRate= " + str(mySelRate) + "\n"  
   
    return queries

def processingRulesCentral_Diamonds(i):
    text = ""
    if evaluationDict[node]:
        text = "Projections to process:\n"
        if i == csource:
            for query in wl:
                myDiamonds = getMiniDiamonds(query, "", query.leafs(), "", 2000)
                # for diamond in myDiamonds:
                #     print(list(map(lambda x: str(x), diamond)))
                #     print(list(map(lambda x: totalRate(x), diamond)))
                #print(Diamond_costs(myDiamonds, "E"))    
                #selRate = projrates[query][0] ** float((1/len(myDiamonds)))
                for diamond in myDiamonds:
                    selRate = return_selectivity(settoproj(sum([x.leafs() if len(x)> 1 else [x] for x in diamond],[]), query).leafs())
                    text += "SELECT " + str(settoproj(sum([x.leafs() if len(x)> 1 else [x] for x in diamond],[]), query)) + " FROM "
                    for i in diamond:
                        text += str(i) +"; "
                        if len(i) > 1:
                            selRate = selRate / return_selectivity(i.leafs())
                    text = text[:-2]    
                    text += " WITH selectionRate= " + str(selRate) + "\n"    
    return text  



def processingRulesCentral(i):
    text = ""
    if evaluationDict[node]:
        text = "Projections to process:\n"
        if i == csource:
            for query in wl:
                text += "SELECT " + str(query) + " FROM "
                for i in query.leafs():
                    text += str(i) +"; "
                text = text[:-2]    
                text += " WITH selectionRate= " + str(projrates[query][0]) + "\n"    
    return text  


def networkText():
    myTypes = list(set(sum([x.leafs() for x in wl], [])))
    #mystr = "network \n"
    mystr = ""
    for i in nw:        
        for j in range(len(i)):
           if string.ascii_uppercase[j] in myTypes:
              mystr += str(i[j]) + " "
              #mystr += str(1) + " "
           else:
                mystr += "0" + " "   
        mystr +="\n"
    return mystr[:-1]

def singleSelecText():
    return "Single Selectivities:" + str(singleSelectivities)

def generatePlan(tw,path):
   
    for node in evaluationDict.keys(): # FOR EACH NODE        
        forwarding = forwardingRule(node)        
        queries = processingRules_Diamonds(node,tw)
        config = {"forwarding": {"node_id": node, "forwarding_table": forwarding} ,"processing":queries}
        with open('../plans/'+ path +'/config_' + str(node) +'.json', 'w') as f:
            json.dump(config, f)   


def generateCentralPlan():
    text  = ""
    text +=networkText() + "\n"
    text +="-----------\n"
    #text +="Randomized Rate-Based Primitive Event Generation\n"
    text +="Dataset-Based Primitive Event Generation \n"
    text +="hm_input_%NodeName%.txt \n"
    text +="-----------\n"
    text += singleSelecText() + "\n"
    text +="-----------\n"
    myforwardingDict = adjustRoutingCentral(cdict,csource)
    for node in evaluationDict.keys():
        text += "~~\n"
        text += "node" + str(node) +"\n"
        text += "--\n" 
        text += forwardingRuleCentral(node,myforwardingDict) + "\n"
        text += "--\n" 
        text += processingRulesCentral_Diamonds(node) + "\n"
        #text += processingRulesCentral(node) + "\n"
    return text    
    
def filterUsed():
    if filterDict.keys():
        return "_filter"
    else:
        return ""
    
def main():
    path = ""
    stretch =1
    tw = 1
    if len(sys.argv) > 1: 
            path = str(sys.argv[1])
    
    if len(sys.argv) >2:
        tw = int(sys.argv[2])    
   
    generatePlan(tw,path)
        
if __name__ == "__main__":
    main()