#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 10:51:56 2021

@author: samira
"""

import pandas as pd 
import numpy as np
import csv
#data_dict = {}


with open('low_selectivity.csv') as csvfile:
         count = 0
         myvalues = []
         myreader = csv.reader(csvfile, delimiter=',', quotechar='|')
         
         for row in myreader:
             print(row)
             if float(row[0]) <= 1:
                 count += 1
                 myvalues.append(float(row[0]))
             
print(np.median(myvalues))
print(count)