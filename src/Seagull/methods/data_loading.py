#!/usr/bin/env python3

'''

This file contain the methods that read information from a file.

Valid reading files are:

csv
txt
fastq

These methods will return an object according to the data that was inside

'''

# General libraries
import pandas as pd

#import constants

# ---------------------------------
# Columns
# ---------------------------------

# Get the columns names
def loadFromCSV(self, csv_path, encoding='utf-8', header = "infer"):
    
    # Load the data from the csv file
    completeData = pd.read_csv(csv_path, encoding = encoding, header = header)
    completeData_totalRows    = len(completeData.index)
    completeData_totalColumns = len(completeData.columns)
    completeData_columnNames  = completeData.columns

    # Modify self with the new info
    self.setData(completeData)
    self.setTotalRows(completeData_totalRows)
    self.setTotalColumns(completeData_totalColumns)
    self.renameColumns(completeData_columnNames)

    # Return error code?
    return 0