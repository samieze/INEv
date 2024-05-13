#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 21:33:50 2024

@author: samira
"""
import pandas as pd

def generate_latex_document(csv_path, latex_file_path):    # Load CSV file
    df = pd.read_csv(csv_path)
    
    # Define the structure of the table
    outer_columns = ['citibike', 'google']
    inner_columns = [1, 2, 3, 4]
    outer_rows = [5,10, 20, 30, 50]
    inner_rows = ['inev', 'muse', 'PPoP', 'Flink']
    
    # Initialize a dictionary to hold the data
    table_data = {oc: {ic: {orow: {irow: "" for irow in inner_rows} for orow in outer_rows} for ic in inner_columns} for oc in outer_columns}

    # Populate the dictionary with values from the dataframe
    for _, row in df.iterrows():
        outer_col = row[0]
        inner_col = row[1]
        outer_row = row[2]
        inner_row = row[5]
        value = row[3]
        print(row[5])
        if not table_data[outer_col][inner_col][outer_row][inner_row]:
            if  row[4] == False:
                  table_data[outer_col][inner_col][outer_row][inner_row] = "$ > "+ str("{:.4f}".format(value)) + "$"
            else: 
                 table_data[outer_col][inner_col][outer_row][inner_row] ="{:.4f}".format(value) 
    # Start writing the LaTeX code
    latex_code = "\\documentclass{article}\n\\usepackage{geometry}\n\\geometry{a4paper, margin=1in}\n"
    latex_code += "\\usepackage{graphicx}\n\\begin{document}\n"
    latex_code += "\\begin{table}[h!]\n\\centering\n"
    latex_code += "\\begin{tabular}{|c|c|c|c|c|c|c|c|c|}\n\\hline\n"
    latex_code += " & \\multicolumn{4}{c|}{citibike} & \\multicolumn{4}{c|}{google} \\\\\n\\cline{2-9}\n"
    latex_code += " & 1 & 2 & 3 & 4 & 1 & 2 & 3 & 4 \\\\\n\\hline\n"

    # Generate table content
    for orow in outer_rows:
        for irow in inner_rows:
            latex_code += f"{orow} {irow}"
            for ocol in outer_columns:
                for icol in inner_columns:
                    latex_code += f" & {table_data[ocol][icol][orow][irow]}"
            latex_code += " \\\\\n"
        latex_code += "\\hline\n"
    
    latex_code += "\\end{tabular}\n"
    latex_code += "\\caption{Comparison against the state of the art in terms of the transmission ratio using real-world datasets..}\n"
    latex_code += "\\label{tab:my_label}\n"
    latex_code += "\\end{table}\n"
    latex_code += "\\end{document}\n"

    # Write the output LaTeX code to a file
    with open(latex_file_path, 'w') as file:
        file.write(latex_code)
    
    print(f"LaTeX document generated at {latex_file_path}")

# Provide the path to your CSV file and the output LaTeX file path
csv_path = "table.csv"
latex_file_path = "table_3.tex"
generate_latex_document(csv_path, latex_file_path)