#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 15:59:44 2022

@author: samira
"""
import time

start_time = time.time()

k = 10 

for i in range(10000):
    if i == k^10:
           k+=1         
    elif i == k * 39:
           k-=1
    elif i == 4*10:
           k-=1
    if i == k^10:
           k+=1         
    elif i == k * 39:
           k-=1
    elif i == 4*10:
           k-=1  
    if i == k^10:
           k+=1         
    elif i == k * 39:
           k-=1
    elif i == 4*10:
           k-=1
    if i == k^10:
           k+=1         
    elif i == k * 39:
           k-=1
    elif i == 4*10:
           k-=1         

    
print(str(round(time.time() - start_time, 10)))