#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 12:54:23 2022

@author: samira
"""

import csv
import pandas as pd

dataframe_adaptivity = pd.read_csv('results_adaptivity.csv')

dataframe_inev = pd.read_csv('results_inev.csv')




# generate dict 1
# level 1 index = experiment name
# level 2 index = adaptivity / inev 
# level 3 index = #swaps
# level 4 a) adaptivity: costs, r1, r2
# level 4 b) Inev: broken (cc, ms), perfect (cc, ms)

# generate dict 1 from adaptivity_only file
# level 1 index = experiment name
# level 2 index = # swaps
# level 3  #broken ms placements,  #broken projections

