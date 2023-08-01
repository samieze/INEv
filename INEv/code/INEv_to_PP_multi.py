#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 16:54:12 2022

@author: samira
"""

from  EvaluationPlan import *
from generate_projections import *

singleSelectivities = {'E': 1.0, 'A': 1.0, 'B': 1.0, 'C': 1.0, 'D': 1.0, 'E|AE': 0.3131580818441003, 'A|AE': 0.09579826208967175, 'B|BE': 0.5864346008298966, 'E|BE': 0.05115659948704478, 'C|CE': 0.12325012142806144, 'E|CE': 0.24340746810144429, 'E|DE': 0.5079763461625174, 'D|DE': 0.059057868002385425, 'A|AB': 0.1716690596687993, 'B|AB': 0.17475484550261372, 'C|AC': 0.92238210092722, 'A|AC': 0.03252448195801138, 'A|AD': 0.31039315974878867, 'D|AD': 0.09665161443725107, 'B|BC': 0.9618299941746831, 'C|BC': 0.03119054321625942, 'D|BD': 0.057995989498980785, 'B|BD': 0.5172771472504528, 'D|CD': 0.26803560164348006, 'C|CD': 0.11192543011470411, 'A|ABE': 0.057722789586688986, 'B|ABE': 0.1709627343626262, 'E|ABE': 0.0027359930992738473, 'A|ACE': 0.022369024139961727, 'E|ACE': 0.008886426887811905, 'C|ACE': 0.13582807752393786, 'E|ADE': 0.17270697108927968, 'D|ADE': 0.020346153043090467, 'A|ADE': 0.0076837210456193175, 'E|BCE': 0.02900280939990806, 'C|BCE': 0.02827191759461851, 'B|BCE': 0.03292823324115415, 'B|BDE': 0.016587721627565766, 'D|BDE': 0.015923414542488724, 'E|BDE': 0.10222116452012711, 'C|CDE': 0.11023330354857507, 'D|CDE': 0.05659831127909154, 'E|CDE': 0.004327603545722656, 'C|ABC': 0.01929454314768564, 'A|ABC': 0.01568184836472378, 'B|ABC': 0.08923433964821727, 'B|ABD': 0.049416115067419, 'D|ABD': 0.02374075987804312, 'A|ABD': 0.023014447273084073, 'D|ACD': 0.07857568651163455, 'C|ACD': 0.1039794242136942, 'A|ACD': 0.0033046705626016692, 'B|BCD': 0.11179452862285362, 'C|BCD': 0.02557125757315075, 'D|BCD': 0.009444764386104773, 'B|ABCE': 0.028259829739811084, 'A|ABCE': 0.01034603696112096, 'C|ABCE': 0.0014334833554618851, 'E|ABCE': 0.001739367324181347, 'A|ABDE': 0.0001898535785926823, 'E|ABDE': 0.0014203274129073074, 'D|ABDE': 0.00926990321899061, 'B|ABDE': 0.2916386448053065, 'D|ACDE': 0.014625107011627059, 'E|ACDE': 0.00015328796921087353, 'A|ACDE': 0.0011627469636021396, 'C|ACDE': 0.27966311527822235, 'D|BCDE': 0.0047683519916598026, 'E|BCDE': 0.0010350865529234032, 'B|BCDE': 0.014491818209189534, 'C|BCDE': 0.010192006160217232, 'D|ABCD': 0.002938291041948441, 'B|ABCD': 0.009742044130462492, 'C|ABCD': 0.013903905240370575, 'A|ABCD': 0.0018316640660926806, 'B|ABCDE': 0.0034627797164369757, 'A|ABCDE': 5.360456783606757e-05, 'D|ABCDE': 0.0017231503085193638, 'E|ABCDE': 0.00010856657379847269, 'C|ABCDE': 0.017004606588733054}
query = SEQ(PrimEvent('E'),PrimEvent('A'), PrimEvent('B'), PrimEvent('C'),PrimEvent('D'))

qwl = [query]
#plan = {('B',''): [], ('A','B'):[('B','')], ('K','B'):[('B','')],('C','B'):[('A','B')], ('E','BK'):[('K','B')], ('EF','AB'):[('A','B')], ('D','C'):[('C','B')], ('K', 'C'):[('EF','AB'),('D','C')], }


# for each key, traverse all predecessors and merge acquisition steps, to generate acquisition sets and projections to match from evaluator
def get_projection(step):
    
    if step[1]:        
        acquired = getAcquired(step, [])
        acquired = sorted(list(set(acquired)))
        myproj = settoproj(acquired, step[2][0])
    elif not step[1] and len(step[0]) == 1:
       myproj = SEQ(step[0])
    elif not step[1] and len(step[0]) >1:
        myproj = settoproj(step[0], step[2][0])
    return myproj


# add merged projections for steps having two predecesor steps, evaluators

def get_acquired(step, mylist):   
    if step[1]:
        mylist += step[0]
        for predecessor in plan(step):
            return get_projection(predecessor, mylist)
    else:
        return 


# for each step, generate combidict -> this is for combis at evaluator
def getCombi(step):
    mycombi = []
    for i in plan[step]:
        mycombi.append(get_projection(i))
    for pull_projection in get_pull_projection(step) :
        mycombi += pull_projection # keep filter for pull_projection
    return step


# for each step, generate pull_projection
def get_pull_projection(step):
    pull_projections = []
    for acquisition_event in step[0]:
        for pull_event in step[1]:
            myEvents = sorted(acquisition_event + pull_event)
            pull_projections.append((settoproj(myEvents, step[2][0])),acquisition_event)
    return pull_projection        

# for each eventtype pulled, generate dict with pull_projection

def generate_pull_dict():
    pull_dict = {}
    for step in plan.keys():
        if step[1]:
            pull_dict[1] = get_pull_projection(step)
    return pull_dict

#get combination of pull_projection which has as input the projection at the evaluator from last step, for two projections add merged projection

def get_string(projection):
    