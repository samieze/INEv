#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 12:33:55 2021

@author: samira
"""

def column(matrix, i):
    return [row[i] for row in matrix]



def column1s(mylist):    
    return [x for x in range(len(mylist)) if mylist[x] == 1]
 
    
def reverseDict(myDict):
    MyReversed = {}
    for i in myDict.keys():
        if not myDict[i] in MyReversed.keys():
            MyReversed[myDict[i]] = [i]
        else:
            MyReversed[myDict[i]].append(i)
    
    return MyReversed 