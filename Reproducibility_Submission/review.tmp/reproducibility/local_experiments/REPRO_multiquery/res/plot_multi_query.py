#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 12:54:23 2022

@author: samira
"""

import csv
import pandas as pd
import matplotlib.pyplot as plt

def get_dev(base_tr, tr):
    return (tr - base_tr) / (base_tr/100)

#adaptivity = list(pd.read_csv('results_adaptivity_sels.csv').columns)
dataframe_shared5= pd.read_csv('sharedCosts_5.csv')
dataframe_unshared5 = pd.read_csv('unsharedCosts_5.csv')
dataframe_shared10= pd.read_csv('sharedCosts_10.csv')
dataframe_unshared10 = pd.read_csv('unsharedCosts_10.csv')
dataframe_shared20= pd.read_csv('sharedCosts_20.csv')
dataframe_unshared20 = pd.read_csv('unsharedCosts_20.csv')


merged5 = dataframe_shared5.merge(dataframe_unshared20, on=["ID", "Skew", "Run"])
merged5 = merged5.assign(unsharedTR = lambda x: x.UnsharedRatio/x.CentralizedCosts)
merged5 = merged5.assign(dev = lambda x: x.SharedRatio/x.unsharedTR)
merged5 = merged5 .assign(dev2 = lambda x: x.TotalCosts/x.UnsharedRatio)

merged10 = dataframe_shared10.merge(dataframe_unshared20, on=["ID", "Skew", "Run"])
merged10= merged10.assign(unsharedTR = lambda x: x.UnsharedRatio/x.CentralizedCosts)
merged10= merged10.assign(dev = lambda x: x.SharedRatio/x.unsharedTR)
merged10= merged10.assign(dev2 = lambda x: x.TotalCosts/x.UnsharedRatio)


merged20 = dataframe_shared20.merge(dataframe_unshared20, on=["ID", "Skew", "Run"])
merged20 = merged20.assign(unsharedTR = lambda x: x.UnsharedRatio/x.CentralizedCosts)
merged20 = merged20.assign(dev = lambda x: x.SharedRatio/x.unsharedTR)
merged20 = merged20.assign(dev2 = lambda x: x.TotalCosts/x.UnsharedRatio)


   
   
plt.rcParams.update({'font.size':25})
plt.xlabel("Event Skew")
plt.ylabel("Diff. Transmission Ratio")
marks = ['x','o','^'] 
plt.yscale("log")

print(merged20.groupby('Skew')['dev'].min())
print(merged10.groupby('Skew')['dev'].min())
print(merged5.groupby('Skew')['dev'].min())

plt.plot(merged20.groupby('Skew')['dev'].median(),  marker = "x", markersize = 10, label = 'QWL5')
plt.plot(merged10.groupby('Skew')['dev'].median(), marker = "^", markersize = 10, label = 'QWL10')
plt.plot(merged5.groupby('Skew')['dev'].median(),  marker = "o", markersize = 10, label = 'QWL20')


plt.legend()
plt.savefig('figs/Fig_7c_multi_query.pdf', format = 'pdf',  bbox_inches='tight')
   
#plt.show()

