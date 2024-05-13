#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 16:35:58 2021

@author: samira
"""
import random as rd
import time
maxcosts = 0 
mylist = [["ABC", "C"], ["AB","B"], ["ABD","D"],["DE","E"],["CBE","E"],["ACE", "E"],["AC","C"],["CDE","D"],["CE","C"]]

mydict = {}
for j in mylist:
    mydict[j[0]] = [j[1],  rd.uniform(10,100)]


mydict = {'ABC': ['C', 12.55295557406285], 'AB': ['B', 40.11206201350895], 'ABD': ['D', 29.66992167267427], 'DE': ['E', 64.26944798906702], 'CBE': ['E', 10.102052900165866], 'ACE': ['E', 14.044211480048787], 'AC': ['C', 67.32913879786628], 'CDE': ['D', 29.51370616403848], 'CE': ['C', 58.84731197464553]}    
projection = "ABCDE"

#Optimize with hashtable and not enumerating duplicates
maxvalue = {}

def stupidFunc():
    
    maxvalue["ABCDE"] = [10, []]
    recCombi(projection, [], 0, mylist)

allcombis = []    
    
def recCombi(projection, combi, costs, mvlist):
    if mvlist:
        for i in range(len(sorted(mvlist))):
            proj = mvlist[i]
            realproj = proj[0]
            
            combiBefore = [x for x in combi]
            
            combi.append(realproj)
            costs += mydict[realproj][1]
            curlist = sorted(mvlist)[i+1:]
            
            curlist = [x for x in curlist if not x[0] == realproj and not set(x[0]).issubset(set(realproj)) and not set(realproj).issubset(set(x[0]))]
            
            partTypes = [x[1] for x in mylist if x[0] in combi]   
            for i in partTypes:
               curlist= [x for x in curlist if not i in x]               
            recCombi(projection, combi, costs, curlist)
            
            combi =  combiBefore
            costs -= mydict[realproj][1]
    else:      
       allcombis.append(combi)
       if costs > maxvalue[projection][0]:
           maxvalue[projection][0] = costs
           maxvalue[projection][1] = combi
         
       
start = time.time()   
stupidFunc()
end = time.time()

print(end-start)
print(maxvalue)
print(len(allcombis))
