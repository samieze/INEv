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
    suffix = 0.01
    if len(sys.argv) > 1:
        suffix = sys.argv[1]
    inputfile = 'results_adaptivity_'+str(suffix)+'.csv'
    inputfile2 = 'results_inev_'+str(suffix)+'.csv'

    adaptivity = list(pd.read_csv(inputfile).columns)
    dataframe_adaptivity = pd.read_csv(inputfile)
    merged = dataframe_adaptivity
    dataframe_inev = pd.read_csv(inputfile2)
    
    merged = dataframe_adaptivity.merge(dataframe_inev, on=["ID","Swaps"])
    merged = merged.assign(Percentage = lambda x: x.Swaps/12)
    
    merged = merged.assign(ratioBrokenProjs = lambda x: x.brokenProjections/x.NumberProjections)
    merged = merged.assign(ratioBrokenPlacements = lambda x: x.brokenPlacements/x.NumberPlacements) 
       
    plt.rcParams.update({'font.size':23})
    plt.xlabel("Swaps")
    plt.ylabel("broken stuff")
    markers = ["o","x","o"]
        
    # arrange x-Ticks
          
    myX_o = sorted(list(set(merged['Swaps'].tolist()))) # to extract x-ticks use values of "X"- column -> normalize X values ? 
    myX = list((map(lambda x: x/len(list(set(merged['Swaps'].tolist()))), list(set(merged['Swaps'].tolist()))))) # counting of x ticks
    
    
    plt.yscale("log")
    merged =  merged.assign(Broken = lambda x: x.costs/x.CentralizeCosts)
    merged =  merged.assign(Repair = lambda x: x.costs_rep2/x.CentralizeCosts)
    plt.ylabel("Transmission Ratio")
    
    for i in ['Broken','Repair']:
             plt.plot(merged.groupby('Percentage')[i].median(),marker="x",  label = i)
    plt.legend()   
    #plt.show()

    plt.savefig("../res/figs/Fig_10_adaptivity_repaircosts_" + str(inputfile[:-4]), format = 'pdf',  bbox_inches='tight')
            
if __name__ == "__main__":
    main()


