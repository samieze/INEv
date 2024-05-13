#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 12:54:23 2022

@author: samira
"""

import csv
import pandas as pd
import matplotlib.pyplot as plt


inputfile = 'selectivity_change.csv'
def get_dev(base_tr, tr):
    return (tr - base_tr) / (base_tr/100)

adaptivity = list(pd.read_csv(inputfile).columns)
merged = pd.read_csv(inputfile)

#merged = merged.assign(Percentage = lambda x: x.Swaps/12)

merged = merged.assign(ratioBrokenProjs = lambda x: x.brokenProjections/x.NumberProjections)
merged = merged.assign(ratioBrokenPlacements = lambda x: x.brokenPlacements/x.NumberPlacements) 
   
plt.rcParams.update({'font.size':23})
plt.xlabel("%Changed Selectivities")
plt.ylabel("Invalidity")
#plt.yscale("log")
labels = ['Projections', 'MNPlacements']  
markers = ["x","o","o"]
    
# arrange x-Ticks
      
myX_o = sorted(list(set(merged['Percentage'].tolist()))) # to extract x-ticks use values of "X"- column -> normalize X values ? 
myX = list((map(lambda x: x/len(list(set(merged['Percentage'].tolist()))), list(set(merged['Percentage'].tolist()))))) # counting of x ticks
#todo, relative x achse
k = 0
for i in ['ratioBrokenPlacements','ratioBrokenProjs']:
           print(merged.groupby('Percentage')[i].median())
           plt.plot(merged.groupby('Percentage')[i].median(),  label = labels[k], marker = markers[k], markersize = 10)
           k+=1

plt.legend()   

plt.savefig("../res/figs/Fig_11b_adaptivity_brokenprojections_" + str(inputfile[:-4]), format = 'pdf',  bbox_inches='tight')
  
