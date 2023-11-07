#!/usr/bin/env python3

'''

This file contain functions that modify the contents of the dataframe

'''

# General libraries
import pandas as pd

# ---------------------------------
# RENAMING
# ---------------------------------
# region

# Rename all columns
def renameColumns(self, newNames):
    self.data = self.data.set_axis(newNames, axis=1, copy=False)

# Rename ONE column
def renameColumn(self, columnIndex, newName):
    self.data.rename(columns={self.data.columns[columnIndex]: newName}, inplace=True)


# endregion

# ---------------------------------
# CASTING
# ---------------------------------
# region

# Transform a column into a integer type
def toInteger(self, columnIndex):

    # Get the name of the index
    currentName = self.getColumnName(columnIndex)

    # Transform the column
    self.data[currentName] = pd.to_numeric(self.data[currentName], errors='coerce').astype('int64')

# Transform a column into a float type
def toFloat(self, columnIndex):

    # THIS IS THE BIGGEST BULLSHIT, MORE THAN R EVEN!, IN THE HISTORY OF PROGRAMMING LANGUAGES
    # Turn out that iloc doesn't change shit: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#why-does-assignment-fail-when-using-chained-indexing
    # It can only read
    # It cannot modify.
    # YOU NEED TO GET THE NAME AND CHANGE BY NAME
    # WHAT. THE FUCK. DESIGN IS THIS CRAP!??

    # Get the name of the index
    currentName = self.getColumnName(columnIndex)

    # Transform the column
    self.data[currentName] = pd.to_numeric(self.data[currentName], errors='coerce').astype('float64')



# endregion

# ---------------------------------
# SETTING VALUES
# ---------------------------------
# region

# Set the whole column
def setColumn(self, index, values):
    self.data.iloc[ :  , index ] = values

# endregion

# ---------------------------------
# DELETING
# ---------------------------------
# region

# Delete a column
def dropColumn(self, index):
    self.data = self.data.drop(self.data.columns[[index]], axis=1) 
    self.totalColumns -= 1

# Delete a column (alias)
def deleteColumn(self, index):
    self.dropColumn(self, index)


# endregion