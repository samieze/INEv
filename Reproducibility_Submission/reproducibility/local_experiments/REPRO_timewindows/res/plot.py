#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 12:54:23 2022

@author: samira
"""

import csv
import pandas as pd
import matplotlib.pyplot as plt
import sys

def get_dev(base_tr, tr):
    return (tr - base_tr) / (base_tr/100)

def main():
    dif = 10
    if len(sys.argv) > 1:
         dif = sys.argv[1]
    dataframe_windowsize = pd.read_csv('window_size'+str(dif)+'.csv')
    
    dataframe_windowsize = dataframe_windowsize.assign(ratio = lambda x: x.SharedCosts/x.UnsharedRatio)
    
       
    plt.rcParams.update({'font.size':17})
    plt.xlabel("WL Size")
    plt.ylabel("Rel. Network Costs")
    labels = ['ratioBrokenProjs', 'ratioBrokenPlacements']  
        
    # arrange x-Ticks
          
    myX = sorted(list(set(dataframe_windowsize['wl_Size'].tolist()))) # to extract x-ticks use values of "X"- column -> normalize X values ? 
    #todo, relative x achse
    
    plt.yscale("log")
    listT = dataframe_windowsize.groupby('wl_Size')['ratio'].apply(list)
    dfBox = listT.reset_index(name = "Lists")
    myLists = list(dfBox["Lists"])
    plt.boxplot(myLists, positions = myX)
    
    plt.legend()   
    
    plt.savefig("figs/Fig_9_timewindow"+str(dif)+".pdf", format = 'pdf',  bbox_inches='tight')
      
    #plt.show()


if __name__ == "__main__":
    main()       
