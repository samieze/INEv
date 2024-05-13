#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 23:46:51 2023

@author: samira
"""
import csv
import sys

def get_row_by_line_number(file_path, line_number):
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            for i, row in enumerate(csv_reader, start=1):
                if i == line_number:
                    return row
    except FileNotFoundError:
        print("File not found at the given path.")
        return None

    return None

# take filename, take row entry, add result to ../res/table.csv

def centralizedCosts(dataset,partitioning,query):
    centralcosts = 0
    with open("result/Table_Data.csv", 'r') as file:
            csv_reader = csv.reader(file,delimiter=",")
            for row in csv_reader:
                if row[0]==dataset and row[1]==partitioning and row[2]==query:
                    centralcosts = row[3]
    return centralcosts

def main():
    resultpath = "result/result.csv"
    
    filename = "citibike_Q1_10"
    row = 1
    if len(sys.argv) > 1: #network size
        filename =sys.argv[1].split("/")[1]
    if len(sys.argv) > 2:
        row = float(sys.argv[2])+1 # event node ratio
    
    mycosts = get_row_by_line_number(resultpath,row)[1]
    approach = "PPoP"
    dataset = filename.split("_")[1]
    query = filename.split("_")[2][1]
    partitioning = filename.split("_")[3]
    mycosts = float(mycosts) / float(centralizedCosts(dataset,partitioning,query))
    myResult = (dataset, query, partitioning, mycosts, approach)
    print("adding " + str(myResult))
    with open("../res/table.csv", "a") as result:
        writer = csv.writer(result)  
        writer.writerow(myResult)

if __name__ == "__main__":
    main()