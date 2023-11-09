#!/usr/bin/env python3

'''

This file contain the getters and setters for the Seagull class.

This only contain functions affecting only the attributes of the class.
Other functions that might change the attributes must use this attributes only.

'''
    
    
# Get the panda object alone
def getPanda(self):
    return self.data

# Get total columns
def ncol(self):
    return self.totalColumns

def getTotalColumns(self):
    return self.totalColumns

# Get total Rows
def nrow(self):
    return self.totalRows

def getTotalRows(self):
    return self.totalRows
