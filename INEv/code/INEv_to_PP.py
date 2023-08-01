#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 10:02:41 2022

@author: samira
"""
from  EvaluationPlan import *
from generate_projections import *


singleSelectivities = {'D|D': 1.0, 'D': 1.0, 'F|F': 1.0, 'F': 1.0, 'G|G': 1.0, 'G': 1.0, 'I|I': 1.0, 'I': 1.0, 'D|DF': 0.5838496117160746, 'F|DF': 0.05138309488949179, 'G|DG': 0.7819436392161438, 'D|DG': 0.038365936488815706, 'D|DI': 0.4021936643557824, 'I|DI': 0.07459093133168268, 'F|FG': 0.40980480516314244, 'G|FG': 0.07320558378532692, 'I|FI': 0.7686902231468953, 'F|FI': 0.03902742495824232, 'G|GI': 0.13600974569263324, 'I|GI': 0.22057242918310158, 'F|DFG': 0.2849451418115158, 'G|DFG': 0.45234299037788883, 'D|DFG': 0.00020947617856471033, 'F|DFI': 0.775327368609418, 'I|DFI': 0.0504598606937951, 'D|DFI': 0.0006901326946667389, 'G|DGI': 0.31606327288306496, 'I|DGI': 0.07845061916983358, 'D|DGI': 0.001088913433560954, 'I|FGI': 0.34731790933760937, 'G|FGI': 0.06843441113994904, 'F|FGI': 0.0011359574166586253, 'D|DFGI': 1.0, 'F|DFGI': 1.0, 'G|DFGI': 1.0, 'I|DFGI': 1.0}
query = AND(PrimEvent('G'),PrimEvent('I'),SEQ(PrimEvent('F'),PrimEvent('D')))
plan = [['G', 'I'], ['F'], ['D']], [[], ['G', 'I'], ['G', 'F']]


selectionRates = {}

evaluator = 0
steps_evaluator = {}
projections = []
events = ''

for k in plan[0]:
    events += ''.join(k)
    newproj = settoproj(events,query) 
    if len(events) == 1:
        newproj = SEQ(events)

    #for acquired_event in k:
    projections.append((newproj, [evaluator], []))

for i in range(len(projections)):
    steps_evaluator[i] = projections[i]

pull_steps = {}
projections_to_pull = []

for k in range(1,len(plan[0])):
        for event_to_pull in plan[0][k]:
            pullset = "".join(plan[1][k])
            newproj = settoproj(pullset+event_to_pull,query)
            projections_to_pull.append((newproj, nodes[event_to_pull], event_to_pull))
            if not k in pull_steps.keys():
                pull_steps[k] = [(newproj, nodes[event_to_pull], event_to_pull)]
            else:
                pull_steps[k].append((newproj, nodes[event_to_pull], event_to_pull))

        
    
combiDict = {}

for k in range(len(projections)): # each projection at evaluator takes as input to combi predecessor projection and miniprojections/filtered by pulled event
    if k == 0:
        combiDict[steps_evaluator[0][0]] = [steps_evaluator[0]]
    else:
        combiDict[steps_evaluator[k][0]] = [steps_evaluator[k-1]] + pull_steps[k]# + # projections with pullsets

pull_combiDict = {}

for k in pull_steps.keys():

    for j in pull_steps[k]:
       pull_combiDict[j[0]] =   [steps_evaluator[k-1]] + [j]


def getSelectivity(proj):
    for steps in steps_evaluator.keys():
        if proj == steps_evaluator[steps][0]:
            step = steps
    
    base =  return_selectivity(proj.leafs())
    localInput = [x for x in combiDict[proj] if not x[2]][0][0]
    if not proj == localInput: # case for pushsteps  divide by selectivity of localprojection
       base = base / return_selectivity(localInput.leafs())   
       
    # build pairs from each event in pull set of step and single inputs in combination
    for singleInput in [x[2] for x in combiDict[proj] if x[2]]:
        for pullEvent in plan[1][step]:
           # print(proj, settoproj([singleInput, pullEvent], query))
            base = base / return_selectivity(settoproj([singleInput, pullEvent], query).leafs())
    
    return str(base)

stringDict = {}        
for i in combiDict.keys(): #evaluator selectivities

    stringDict[i] = "SELECT " + str(i) + " FROM "
    if not i ==  steps_evaluator[0][0]:
        for j in combiDict[i]:
            
            if not j[2]:
                stringDict[i] += str(j[0]) + "; "
            else:
                 stringDict[i] +=  j[2] + "|" + ''.join(j[0].leafs()) +"; "
         
    else:
        for prim in i.leafs():
         stringDict[i] += str(prim) + "; "
    stringDict[i] = stringDict[i][:-2]             
    
    stringDict[i] += " WITH selectionRate =" +  getSelectivity(i)
    
        
for k in pull_steps.keys(): # pull_answers
        print(k)
        for j in pull_steps[k]:
            mySel = singleSelectivities[j[2] + "|" + ''.join(sorted(steps_evaluator[k-1][0].leafs()+[j[2]]))]
            stringDict[j[2]] = "SELECT " + str(j[0]) + " FROM " + j[2] + ";"
            print("match "+ str(j[0]), "checked: " + str(steps_evaluator[k-1][0]) + "inputs " + str(plan[1][k]))
            if len(str(steps_evaluator[k-1][0])) == 1:
                stringDict[j[2]] += str(steps_evaluator[k-1][0])
            else:
                for filteredEvent in plan[1][k][0]:
                    stringDict[j[2]] +=  filteredEvent  + "|" + ''.join(steps_evaluator[k-1][0].leafs())+ ";"
                stringDict[j[2]]  = stringDict[j[2]][:-1]   
               # stringDict[j[2]] +=  str(settoproj(''.join(plan[1][k]), query))  + "|" + ''.join(steps_evaluator[k-1][0].leafs())
       # print(''.join(plan[1][k]) + "|" + str(steps_evaluator[k-1][0]))
            stringDict[j[2]] += " WITH selectionRate= " +str(mySel)


# write new evaluation plan:
# projections for evaluator based on combidict
# forwarding: to nodes of each event to pull with current projection filtered by pullset

# for each node, if node generates events to pull: add projection with based on events to pull, currentprojection from evaluator from last step,
# filtered by pullset
# forwarding, send each projection filtered by pullset to evaluator

def processingRules(node):
    mytext = "Projections to process:\n"
    for event in stringDict.keys():
        if len(event) == 1 and isinstance(event, str):
            if node in nodes[event]:
                mytext += stringDict[event] + "\n"
        elif node == evaluator:
             mytext += stringDict[event] + "\n"
    return mytext

def toETB(projection):
    text = ""
    parts = list(map(lambda x: str(x), projection.leafs()))
    for ev in parts:
            text += "("+str(ev)+": ANY);"        
    text = text[:-1]
    return text


def forwardingRule(node):
    text = "Forward rules:\n"
    if node == evaluator:   
    #pullrequests
           for step in range(1,len(plan[0])):
               for event_to_pull in plan[0][step]:
                   for generating_node in [x for x in nodes[event_to_pull] if not x==evaluator]:
                       for j in plan[1][step][0]:           
                          mytext = j +"|"+str(steps_evaluator[step-1][0]) + " - [ETB:" + toETB(steps_evaluator[step][0]) + " FROM:[node"+ str(node) + "] TO:[node" + str(generating_node) + "]] \n"
                          if not mytext in text:
                              text+=  mytext
    #pullanswers
    else:
        for step in range(1,len(plan[0])):
            for event_to_pull in plan[0][step]:
                if node in nodes[event_to_pull]:
                   for mytuple in pull_steps[step]:
                       if event_to_pull == mytuple[2]:
                          text +=  event_to_pull +"|"+str(mytuple[0]) + " - [ETB:" + toETB(projection) + " FROM:[node"+ str(node) +"] TO:[node" + str(evaluator) +"]]\n"
        for pushed_events in plan[0][0][0]:# send all prim events from pushstep 
            if node in nodes[pushed_events]:
                text +=  pushed_events + " - [ETB:" + toETB(settoproj(pushed_events, query)) + " FROM:[node"+ str(node) +"] TO:[node" + str(evaluator) +"]]\n"
    return text  

def networkText():
    #myTypes = list(set(sum([x.leafs() for x in wl], [])))
    myTypes = query.leafs()
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

def generatePlan():
    text  = ""
    text +=networkText() + "\n"
    text +="-----------\n"
    text +="Randomized Rate-Based Primitive Event Generation\n"
    #text +="Dataset-Based Primitive Event Generation \n"
    #text +="hm_input_%NodeName%.txt \n"
    text +="-----------\n"
    text += singleSelecText() + "\n"
    text +="-----------\n"
    for node in network.keys():
        text += "~~\n"
        text += "node" + str(node) +"\n"
        text += "--\n" 
        text += forwardingRule(node) + "\n"
        text += "--\n" 
        text += processingRules(node) + "\n"
        #processingRules = processingRules_Diamonds(node)
        #text += processingRules + "\n"
        #print(processingRules)
    return text


#generatePlan()
print(generatePlan())

# selectionRate for pullanswers -> single selectivity for pulled event| proj on all events in pull set
# selectionRate for evaluator -> only those selectivities for events that were not in pullset before