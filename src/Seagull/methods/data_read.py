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

# Get the data types of the columns
def getColumnTypes(self):
    return self.data.dtypes

# Check if the column is categorical
def isCategorical(self, index):
    return self.data.iloc[ :  , index ].dtype == "object"

# If a column have categorical data, return the categories
def getCategories(self, index):

    if(self.isCategorical(index) == False):
        print("Error: The column is not categorical")
        return None
    else:
        return self.data.iloc[ :  , index ].unique()

# Check if the column is numerical
def isNumerical(self, index):

    toReturn = False

    if(self.data.iloc[ :  , index ].dtype == "float64"):
        toReturn = True
    elif(self.data.iloc[ :  , index ].dtype == "int64"):
        toReturn = True
    elif(self.data.iloc[ :  , index ].dtype == "int32"):
        toReturn = True
    elif(self.data.iloc[ :  , index ].dtype == "Float64"):
        toReturn = True
    elif(self.data.iloc[ :  , index ].dtype == "Int64"):
        toReturn = True
    elif(self.data.iloc[ :  , index ].dtype == "Int32"):
        toReturn = True        

    return toReturn

def isFloat(self,index):

    toReturn = False

    if(self.data.iloc[ :  , index ].dtype == "float64"):
        toReturn = True
    elif(self.data.iloc[ :  , index ].dtype == "Float64"):    
        toReturn = True

    return toReturn

def isInt(self,index):

    toReturn = False

    if(self.data.iloc[ :  , index ].dtype == "int64"):
        toReturn = True
    elif(self.data.iloc[ :  , index ].dtype == "int32"):
        toReturn = True
    elif(self.data.iloc[ :  , index ].dtype == "Int64"):
        toReturn = True
    elif(self.data.iloc[ :  , index ].dtype == "Int32"):
        toReturn = True        

    return toReturn    
    

# ---------------------------------
# Rows
# ---------------------------------