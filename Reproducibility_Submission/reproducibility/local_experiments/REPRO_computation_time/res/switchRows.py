#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 13:15:09 2020

@author: samira
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 11:56:39 2020

@author: samira
"""

import pandas as pd 
import numpy as np
import csv
data_dict = {}

First = True
myRows = []


with open('lower+0.01.csv') as csvfile:           
         myreader = csv.reader(csvfile, delimiter=',', quotechar='|') 
         First = True
         for row in myreader: 
             if len(row[2])>4 and row[2]!= 'FilterUsed':
                 continue
             else:
                 if not First:
    		             newrow = row
    		             newrow[1] = newrow[17]
    		             myRows.append(newrow)               
                 if First:
                     myRows.append(row)
                     First = False
		                      
                 


               

with open("lower+0.01_real.csv", "w") as result:
      writer = csv.writer(result)        
      for i in myRows:
          writer.writerow(i)     
myRows = []

with open('lower+0.001.csv') as csvfile:           
         myreader = csv.reader(csvfile, delimiter=',', quotechar='|') 
         First = True
         for row in myreader: 
             if len(row[2])>4 and row[2]!= 'FilterUsed':
                 continue
             else:
                 if not First:
    		             newrow = row
    		             newrow[1] = newrow[17]
    		             myRows.append(newrow)               
                 if First:
                     myRows.append(row)
                     First = False                  
                 


               

with open("lower+0.001_real.csv", "w") as result:
      writer = csv.writer(result)        
      for i in myRows:
          writer.writerow(i)              
       



    
         
