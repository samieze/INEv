#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 15:26:50 2021

@author: samira
"""
import pickle
from tree import *

with open('network',  'rb') as  nw_file:
        nw = pickle.load(nw_file)

with open('current_wl',  'rb') as  wl_file:
    wl = pickle.load(wl_file)

with open('selectivities', 'rb') as selectivity_file:
    selectivities = pickle.load(selectivity_file)             
        
f = open("config_single_selectivities.txt", "w")
f.write("network\n")
for i in range(len(nw)):
    mystring = "Node " + str(i) + " " + str(nw[i]) + "\n"
    f.write(mystring)
f.write("\nqueries\n")
for query in wl:
    f.write(str(query)+"\n")
f.write("\nmuse graph\n")
f.write("SELECT SEQ(A, B, C, D, E) FROM AND(B, SEQ(A, E, F)); I ON {1, 2, 4, 6, 7, 8, 9}/n(I)\n")
f.write("\nselectivities\n")
f.write(str(selectivities))

f.close()

# #open and read the file after the appending:
# f = open("config_single_selectivities.txt", "r")
# print(f.read()) 