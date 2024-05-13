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

#import pandas as pd 
#import numpy as np
import csv
import sys


def filtered(filename):
    myOut = []
    First = True
    with open('res/eventskew/res/' + str(filename) +'.csv') as csvfile:
             count = 0
             countBad = 0
             myvalues = []
             myreader = csv.reader(csvfile, delimiter=',', quotechar='|')
             for row in myreader: 
                 count += 1
                 if First:
                     myrow = []
                     myrow.append(row[1])
                     myrow.append(row[4])
                     myOut.append(myrow)
                     First = False
                 else:    
                     if float(row[1]) > 0.9:
                             countBad += 1
                     else: 
                             myrow = []
                             myrow.append(row[1])
                             myrow.append(row[4])
                             myOut.append(myrow)
    return(myOut, countBad/count)                         
                         
                         
def main():
 filename = "basicFilter"
 if len(sys.argv) > 1:
         filename=str(sys.argv[1])   
         
 output = filtered(filename)
 print("Bad MuSE Ratio " + str(output[1]))
 with open(str(filename)+"_filtered.csv", "w") as result:
      writer = csv.writer(result)  
      for i in output[0]:
               print(i)
               writer.writerow(i)
 
 

if __name__ == "__main__":
    main()
 