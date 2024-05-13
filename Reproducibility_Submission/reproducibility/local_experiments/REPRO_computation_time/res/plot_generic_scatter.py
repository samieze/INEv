#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 16:43:03 2021

@author: samira
"""
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import csv
import sys
import argparse

# input should contanin name of -i files, -box showBoxes as boolean, -x -y x and y axis, -l labels, -o outputname
# read schema from first line of input files and throw exception if input files dont have the same schema

def main():
    parser = argparse.ArgumentParser(description='Generate Plots')
    myargs = myparse_args(parser)
    mydata = []
    
  #  if len(myargs.labels) != len(myargs.inputs):
   #     print("Number of input paths and labels must be the same.")
    #    return 
    
    
   # labels = myargs.labels
    
    mycolumns = list(pd.read_csv(myargs.inputs[0]).columns)
    
    for path in myargs.inputs: # schemas are  equal or overlap
        df = pd.read_csv(path)
        mycolumns = list(set(mycolumns).intersection(set(list(df.columns))))
        mydata.append(df)
        
    
    
    ###  use specfied columnnames for x and y axis
    if not mycolumns:
        print("Mismatch of schemes")
        return
    
    if myargs.xC in list(mycolumns):
        X_Column = myargs.xC
    else: 
        print("Wrong Column Name")
        print("Schema " + str(mycolumns))
        return
        
    if myargs.yC in list(mycolumns):
        Y_Column = myargs.yC
    else: 
        print("Wrong Column Name")
        print("Schema " + str(mycolumns))
        return
    
    
    
    plt.rcParams.update({'font.size':20})
    

    for i in range(len(mydata)):
        mydata[i].plot.scatter(x= X_Column , y=Y_Column, c='DarkBlue')
    plt.xlabel("Projections")
    plt.ylabel("Computation Time in s")   
    plt.savefig("figs/"+str(myargs.outname), format = 'pdf',  bbox_inches='tight')
    #plt.show()

def myparse_args(parser):
     
     parser.add_argument('-i','--inputs',  nargs='+', help='input files', required=True)
   #  parser.add_argument('-l', '--labels', nargs='+', required=True)
     parser.add_argument('-x', '--xC', help='x axis identifier', required=True)
     parser.add_argument('-y', '--yC', help='y axis identifier', required=True)
     parser.add_argument('-box', '--boxplot', action='store_true', required=False, default= False)
     parser.add_argument('-o', '--outname', required=False, default= "plot")
     args = parser.parse_args()
     return args
     
if __name__ == "__main__":
    main()