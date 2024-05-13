#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 18:52:09 2023

@author: samira
"""

def initialize_dict(filename):
      adressDict = {}
      with open(filename, 'r') as file:
            for line in file:
                adressDict[line.split(",")[0]] = line.split(",")[1].strip()
      print(adressDict)
      return adressDict

def substitute(content, dictionary):
    for k in dictionary.keys():
        content = content.replace("node"+str(k), "[" + dictionary[k] + "]" )
    return content

def substitute_in_file(input_file_path, dictionary, output_file_path):
    with open(input_file_path, 'r') as file:
        content = file.read()
    modified_content = substitute(content, dictionary)
    with open(output_file_path, 'w') as file:
        file.write(modified_content)

addressDict = initialize_dict("IPs.txt")
substitute_in_file("IPCONFIG/config.template.json", addressDict, "IPCONFIG/config.json")