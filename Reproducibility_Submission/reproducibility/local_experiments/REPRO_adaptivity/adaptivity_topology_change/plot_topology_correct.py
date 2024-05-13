#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 12:54:23 2022

@author: samira
"""

import csv
import pandas as pd
import matplotlib.pyplot as plt



dataframe_add = pd.read_csv('add.csv')
dataframe_remove = pd.read_csv('remove.csv')
dataframe_permute = pd.read_csv('permute.csv')
# spalte adden, die median pro id enthält und csv zurück

d = {'TransmissionRatioChange': 'median', 'TransmissionRatioINEV': 'mean'}
mydfs = [dataframe_add, dataframe_remove, dataframe_permute]
mylabels = ['add', 'remove', 'permute']
markers = [".", "o", "x"]
for i in range(len(mydfs)):
    mygroup = mydfs[i].groupby(['ID', 'Change'], as_index = False).aggregate(d).reindex(columns = mydfs[i].columns)
    plt.plot(mygroup.groupby(['Change'])['TransmissionRatioChange'].median(), marker=markers[i] , label = mylabels[i])


plt.plot(mygroup.groupby(['Change'])['TransmissionRatioINEV'].median(), marker="^" , label = "INEv")

plt.yscale("log")
plt.legend()   

plt.savefig("../res/figs/Fig_11c_changing_topology.pdf", format = 'pdf',  bbox_inches='tight')

plt.rcParams.update({'font.size':17})
plt.xlabel("% Changed Edges")
plt.ylabel("TransmissionRatio")
# labels = ['ratioBrokenProjs', 'ratioBrokenPlacements']  
    
# # arrange x-Ticks
      
# myX_o = sorted(list(set(merged['Percentage'].tolist()))) # to extract x-ticks use values of "X"- column -> normalize X values ? 
# myX = list((map(lambda x: x/len(list(set(merged['Percentage'].tolist()))), list(set(merged['Percentage'].tolist()))))) # counting of x ticks
# #todo, relative x achse

# for i in ['ratioBrokenProjs', 'ratioBrokenPlacements']:
#            print(merged.groupby('Percentage')[i].median())
#            plt.plot(merged.groupby('Percentage')[i].median(),marker="x",  label = i)


  
# plt.show()

