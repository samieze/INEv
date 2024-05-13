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

NN = []
SI = []

count = 0
count1 = 0

badn = 0
bads = 0
First = True

with open('res/out2.csv') as csvfile:
         countEx = 0
         countN = 0
         myvalues = []
         myreader = csv.reader(csvfile, delimiter=',', quotechar='|')
         for row in myreader:
             
             if First:
                 First = False
             else:    
                 if float(row[0]) < 0.9:
                     if int(row[2]) == 100 and float(row[3]) == 1.2:
                         NN.append(float(row[0]))
                         count += 1
                     else:
                         count1 +=1 

print(count)                     
print("N: " + str(np.median(NN)))


#print(count1/4) 
#print(myumNone/ countN ) 

#for j in data_dict.keys():
#    if len(data_dict[j]) < 30:
#         del data_dict[j]
       
#df = pd.DataFrame.from_dict(data_dict)
#print df
#median =  df.mean()
#print median.plot()
#print df.boxplot()

#def get_key(number):
#    return number // 5 
#
#for i in range(1,21):
#    with open('musecosts_'+str(i)) as csvfile:
#         count = 0
#         myvalues = []
#         myreader = csv.reader(csvfile, delimiter=',', quotechar='|')
#         for row in myreader:
#             if float(row[0]) < 0.2:
#                 key = get_key(int(row[1]))
#                 if not key in data_dict:
#                     data_dict[key] = [float(row[0])]
#                 else:
#                     data_dict[key].append(float(row[0]))
#                 
#for i in data_dict.keys():
#    if len(data_dict[i]) > 5:
#        data_dict[i] = [np.median(data_dict[i])]
#    else:
#        del data_dict[i]
#
#print data_dict
#    
#df2 = pd.DataFrame.from_dict(data_dict)
#print df2.boxplot()



    
         