#!/usr/bin/env python3

'''

This file contain functions that modify the contents of the dataframe

'''

# General libraries
import pandas as pd
import numpy as np

from src import constants

# ---------------------------------
# SETTING VALUES
# ---------------------------------
# region

# Set the whole column to zero values
# This depends of what type of column you have
# floats = 0.0
# ints = 0
# strings = ""
# dates = NaT
def set_column_zeroes(self, index):

    if self.isInt(index):
        self.data.iloc[ :  , index ] = constants.INT_ZERO

    elif self.isFloat(index):
        self.data.iloc[ :  , index ] = constants.FLOAT_ZERO

    elif self.isString(index):
        self.data.iloc[ :  , index ] = constants.STRING_ZERO

    elif self.isBoolean(index):
        self.data.iloc[ :  , index ] = False

    elif self.isDate(index):
        self.data.iloc[ :  , index ] = constants.DATE_ZERO

    elif self.is_strict_categorical(index):
        self.data.iloc[ :  , index ] = constants.CATEGORICAL_NAN


# endregion

# ---------------------------------
# DELETING
# ---------------------------------
# region

# Delete a column
def drop_column(self, index):
    self.data = self.data.drop(self.data.columns[[index]], axis=1) 
    self.totalColumns -= 1

# Delete a column (alias)
delete_column = drop_column

# endregion

# ---------------------------------
# ROUNDING
# ---------------------------------
# region

# Round a column to desired rounding
def round_column(self, column_index, decimals = 2):

    self[:,column_index] = np.round(self[:,column_index], decimals = decimals)



# Round the entire dataframe
def round(self, decimals = 2):

    for i in range(self.totalColumns):
        if (self.isNumerical(i)): self.round_column(i, decimals = decimals)


# endregion



# ---------------------------------
# ROUNDING
# ---------------------------------
# region

# Transpose the entire dataframe
# This is only possible if all columns have the same type
def transpose(self)-> int:

    # Return code
    toReturn = -1

    # Get the types
    my_types = self.get_column_types()

    # Check if all are the same
    # If they aren't, print an error
    if len(set(my_types)) != 1:
        print("ERROR: All columns must have the same type to transpose")

    # If they are, transpose
    else:
    
        self.data         = self.data.transpose()
        self.totalRows    = self.data.shape[0]
        self.totalColumns = self.data.shape[1]
        toReturn          = 0

    return toReturn


# endregion