#!/usr/bin/env python3

'''

This file contain the methods that read information from the dataframe

Non of these methods should change the dataframe in any way.

'''

# ---------------------------------
# Columns
# ---------------------------------

# Get the columns names
def getColumnNames(self):
    return(self.data.columns).to_list()

# Get ONE column names
def getColumnName(self, columnIndex):
    return(self.data.columns).to_list()[columnIndex]

# Return the whole column
def getColumn(self, index):
    return self.data.iloc[ :  , index ]
def c(self, index):
    return self.data.iloc[ :  , index ]

# ---------------------------------
# Rows
# ---------------------------------