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

# For a given column name, return the first index
def getColumnIndex(self, column_name):
    return(self.data.columns.get_loc(column_name))

# Return the whole column
def getColumn(self, index):
    return self.data.iloc[ :  , index ]
def c(self, index):
    return self.data.iloc[ :  , index ]

# Get the data types of the columns
def getColumnTypes(self):
    return self.data.dtypes


# Check if the column is categorical
# It could be both strings, or a well defined category
def isCategorical(self, index):

    toReturn = False

    if(self.data.iloc[ :    , index ].dtype == "object"):
        toReturn = True
    elif(self.data.iloc[ :  , index ].dtype == "category"):
        toReturn = True
    
    return toReturn

# Check if the column is stricly strings without categorical
def isCharacter(self, index):
    return self.data.iloc[ :  , index ].dtype == "object"

# If a column have categorical data, return the categories
def getCategories(self, index):

    return_categories = []

    # If you try to run this on a non-categorical column, does nothing extra
    if(self.isCategorical(index) == False):
        print()
        print("WARNING!: The column is not categorical")
        print()

    # Otherwise find the categories
    else:

        # If the column is actually a full categorical with levels
        if(self.data.iloc[ :  , index ].dtype == 'category'):
            return_categories = self.data.iloc[ :  , index ].cat.categories

        # Otherwise, is just a colection of strings
        else:
            return_categories = self.data.iloc[ :  , index ].unique()

    return (return_categories)

# Check if the column is numerical
def isNumerical(self, index):

    toReturn = False

    if(self.data.iloc[ :    , index ].dtype == "float64"):
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

    if(self.data.iloc[ :    , index ].dtype == "float64"):
        toReturn = True
    elif(self.data.iloc[ :  , index ].dtype == "Float64"):    
        toReturn = True

    return toReturn

def isInt(self,index):

    toReturn = False

    if(self.data.iloc[ :    , index ].dtype == "int64"):
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
# Return the whole row
def getRow(self, index):
    return self.data.iloc[ index , : ]
def r(self, index):
    return self.data.iloc[ index , : ]

# Get the rows names
def getRowsNames(self):
    return(self.data.index).to_list()

# Get ONE row names
def getRowName(self, row_index):
    return(self.data.index).to_list()[row_index]

# For a given row name, return the first index
def getRowIndex(self, row_name):
    return(self.data.index.get_loc(row_name))