# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 15:25:26 2023

@author: avery
"""


import pandas as pd
import os

# Set the path to the folder containing the text files
folder_path = "C://Users//avery//Documents//Snow Data Science Consulting//Z//Refinery//data (2)//column_data"

# Get a list of all the text files in the folder
file_list = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

# Create an empty DataFrame to store the text data
df = pd.DataFrame()

# Loop through the list of text files and create a series for each file
for file_name in file_list:
    
    # Find the file 
    print(file_name + ' has started ')
    absolute_path = 'C://Users//avery//Documents//Snow Data Science Consulting//Z//Refinery//data (2)//column_data/' + file_name
    
    # Get the lines for that file 
    with open(absolute_path) as f:
        lines = [line.rstrip('\n') for line in f]
    
    
    
    
    column = []
    print('# of lines: ' + str(len(lines)))
    dummy = lines[0].split('\t')
    print('-----' + str(len(dummy)))
    
    # For loop for all lines inside file 
    for i in range(0,len(lines)):
            
        # Logic to fix sampling differences
        first_letter = file_name[0]
        
        if first_letter == 'P' or first_letter == 'E':
            
            line_temp  = [float(x) for x in lines[i].split('\t')[::100]]
            column = column + line_temp
            
            
        elif first_letter == 'F':
            line_temp  = [float(x) for x in lines[i].split('\t')[::10]]
            column = column + line_temp
            
            
        else:
            line_temp  = [float(x) for x in lines[i].split('\t')][::1]
            column = column + line_temp
           


        
    
    # Append the series to the DataFrame
    df[file_name] = column
    print(file_name + ' is done')

# Print the resulting DataFrame
print(df)
df.to_csv('eng_data.csv')


df2 = pd.read_csv("C:\\Users\\avery\\Documents\\Snow Data Science Consulting\\Z\\Refinery\\data (2)\\profile.txt",
                  lineterminator=r'\n', delimiter=r'\t', header = None)