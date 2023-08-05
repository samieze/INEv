#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 23:21:43 2022

@author: samira
"""

from tree import *
import random as rd
import sys
import pickle



def main():
    
    with open('original_network', 'rb') as original_network_file:
       nw = pickle.load(original_network_file)  


    with open('wl_windows', 'rb') as wl_windows_file:
        wl_windows = pickle.load(wl_windows_file)                   

    with open('original_wl',  'rb') as  wl_file: # change to ORIGINAL WL
        wl = pickle.load(wl_file)    
        
        
    query_index = 1

    if len(sys.argv) > 1: 
      query_index = int(sys.argv[1])      
    
    # overwrite current rates + current query workload  
    myquery_window = wl_windows[query_index][1]
    for i in range(len(nw)):  
        for rate in range(len(nw[i])):
            nw[i][rate] = myquery_window * nw[i][rate]
            
    wl = [wl[query_index]] # original_wl
        
    print(wl)
    with open('network', 'wb') as network_file:
        pickle.dump(nw, network_file)  
        
    with open('current_wl', 'wb') as wl_file:
        pickle.dump(wl, wl_file)    

if __name__ == "__main__":
    main()        