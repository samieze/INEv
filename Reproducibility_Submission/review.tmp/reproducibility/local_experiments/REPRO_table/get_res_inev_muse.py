#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 20:46:59 2023

@author: samira
"""

import os
import csv
from getPairs import *

directory_path = "."

def iterate_files_in_directory(directory_path):
    table_results = {"inev":{"citibike":{1:{5:0,10:0,20:0,30:0,50:0},2:{5:0,10:0,20:0,30:0,50:0},3:{5:0,10:0,20:0,30:0,50:0},4:{5:0,10:0,20:0,30:0,50:0}}, "google":{1:{5:0,10:0,20:0,30:0,50:0},2:{5:0,10:0,20:0,30:0,50:0},3:{5:0,10:0,20:0,30:0,50:0},4:{5:0,10:0,20:0,30:0,50:0}}},"muse":{"citibike":{1:{5:0,10:0,20:0,30:0,50:0},2:{5:0,10:0,20:0,30:0,50:0},3:{5:0,10:0,20:0,30:0,50:0},4:{5:0,10:0,20:0,30:0,50:0}}, "google":{1:{5:0,10:0,20:0,30:0,50:0},2:{5:0,10:0,20:0,30:0,50:0},3:{5:0,10:0,20:0,30:0,50:0},4:{5:0,10:0,20:0,30:0,50:0}}}}
    terminated = {"inev":{"citibike":{1:{5:0,10:0,20:0,30:0,50:0},2:{5:0,10:0,20:0,30:0,50:0},3:{5:0,10:0,20:0,30:0,50:0},4:{5:0,10:0,20:0,30:0,50:0}}, "google":{1:{5:0,10:0,20:0,30:0,50:0},2:{5:0,10:0,20:0,30:0,50:0},3:{5:0,10:0,20:0,30:0,50:0},4:{5:0,10:0,20:0,30:0,50:0}}},"muse":{"citibike":{1:{5:0,10:0,20:0,30:0,50:0},2:{5:0,10:0,20:0,30:0,50:0},3:{5:0,10:0,20:0,30:0,50:0},4:{5:0,10:0,20:0,30:0,50:0}}, "google":{1:{5:0,10:0,20:0,30:0,50:0},2:{5:0,10:0,20:0,30:0,50:0},3:{5:0,10:0,20:0,30:0,50:0},4:{5:0,10:0,20:0,30:0,50:0}}}}

    try:
        # Get a list of all files and subdirectories in the given directory
        files_and_subdirs = os.listdir(directory_path)
        
        # Iterate over each item in the list
        for item in files_and_subdirs:
            # Construct the full path of the item
            item_path = os.path.join(directory_path, item)
            if ("muse" in item or "inev" in item) and ".txt" in item and os.path.isfile(item_path):
                print(item)
                key1 = item.split("_")[0]
                key2 = item.split("_")[1]
                key3 = int(item.split("_")[2][1])
                key4 = int(item.split("_")[3])
                results=  count_lines_containing_sending(item_path)
                table_results[key1][key2][key3][key4] = results[0]
                terminated[key1][key2][key3][key4] = results[1]
    except FileNotFoundError:
        print("Directory not found at the given path.")
    return table_results,terminated
# Example usage:


def count_lines_containing_sending(file_path):
    count = 0
    terminated = False
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if "Sending" in line:
                    count += 1
                if "Total number of events sent over network:" in line:
                    terminated = True
    except FileNotFoundError:
        print("File not found at the given path.")
        return None

    return count, terminated

# Example usage:
results = iterate_files_in_directory(directory_path)
table_results = results[0]
terminated = results[1]

for approach in table_results.keys():
    for dataset in table_results[approach].keys():
        for query in table_results[approach][dataset].keys():
            for partitioning in table_results[approach][dataset][query]:
                table_results[approach][dataset][query][partitioning] = table_results[approach][dataset][query][partitioning] / CC_table[dataset][query][partitioning]
                myResult = (dataset, query, partitioning,table_results[approach][dataset][query][partitioning],terminated[approach][dataset][query][partitioning], approach )
                with open("res/table.csv", "a") as result:
                          writer = csv.writer(result)  
                          writer.writerow(myResult)
