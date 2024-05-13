#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 12:47:03 2022

@author: samira
"""
from generate_projections import *

projFilterDict =  {}  
    

for proj in projlist:
    projFilterDict.update(returnProjFilterDict(proj))    
    
for i in projFilterDict.keys():
    print(i)
    print(projFilterDict[i])
    print("....")
def printFilter():
    f = open("out.txt", "w")
    for proj in projlist:
        if getMaximalFilter(projFilterDict, proj):
            f.write("VAR=false")
            f.close()
            return
        else:
            f.write("VAR=true")
            f.close()
            return    
        
printFilter()
        