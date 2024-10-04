#!/usr/bin/env python3

'''

This file contain functions that modify the contents of the dataframe

'''

# General libraries
import pandas as pd
import numpy as np

# ---------------------------------
# RENAMING
# ---------------------------------
# region

# Rename all columns
def renameColumns(self, newNames):
    self.data = self.data.set_axis(newNames, axis=1, copy=False)

setColumnsNames = renameColumns
rename_columns  = renameColumns

# Rename ONE column
def rename_column(self, columnIndex, newName):
    self.data.rename(columns={self.data.columns[columnIndex]: newName}, inplace=True)

setColumnName   = renameColumns
renameColumn    = rename_column

# Rename all rows
def rename_rows(self, newNames):
    self.data = self.data.set_axis(newNames, axis=0, copy=False)

setRowsNames = rename_rows
renameRows   = rename_rows

# Rename ONE row
def rename_row(self, rowIndex, newName):
    self.data.rename(rows={self.data.rows[rowIndex]: newName}, inplace=True)

setRowName   = rename_row
renameRow    = rename_row







# endregion

# ---------------------------------
# SETTING VALUES
# ---------------------------------
# region

# Set the whole column
def setColumn(self, index, values):
    self.data.iloc[ :  , index ] = values

# Set the whole column to zero integers
def setColumnZeroes(self, index):
    self.data.iloc[ :  , index ] = 0
    self.columnToInteger(index)

# Set the whole column to zero floats
def setColumnZeroesF(self, index):
    self.data.iloc[ :  , index ] = 0
    self.columnToFloat(index)

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
deleteColumn = dropColumn

# endregion

# ---------------------------------
# SPECIAL
# ---------------------------------
# region

# Round a column to desired rounding
def round_column(self, column_index, decimals = 2):

    self[:,column_index] = np.round(self[:,column_index], decimals = decimals, out = self[:,column_index])

    return 0

# Round the entire dataframe
def round(self, decimals = 2):

    for i in range(self.totalColumns):
        if (self.isNumerical(i)): self.round_column(i, decimals = decimals)

    return 0

# Normalize the data by columns or rows
def normalize(self, column = True, avoidFirstColumn = False):

    # If the first column need to be preserved, save the rest of the columns
    # into a temporal dataframe, normalize that, and then put it back
    if(avoidFirstColumn == True):
        temporalDataframe = self.data.iloc[ :  , 1 : ]
    else:
        temporalDataframe = self.data

    # Normalize the data
    if(column == True):
        # Normalize by column
        temporalDataframe = temporalDataframe.apply(lambda x: (x - x.min()) / (x.max() - x.min()))

    else:
        # Normalize by row
        temporalDataframe = temporalDataframe.apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=1)

    # Put the data back
    if(avoidFirstColumn == True):
        self.data.iloc[ :  , 1 : ] = temporalDataframe
    else:
        self.data = temporalDataframe

# endregion