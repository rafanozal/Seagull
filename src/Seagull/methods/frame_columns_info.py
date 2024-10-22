#!/usr/bin/env python3

'''

This file contain the methods that read information from the dataframe

These methods return information relating to columns.
They do not return any data from inside the column

'''

import lib.utils as utils

# ---------------------------------
# Types
# ---------------------------------
# Get the data types of the columns
def get_column_types(self):
    return self.data.dtypes.to_list()

# ---------------------------------
# Names
# ---------------------------------

# Get the columns names
def get_columns_names(self):
    return(self.data.columns).to_list()

# Get ONE column names
def get_column_name(self, columnIndex):
    return(self.data.columns).to_list()[columnIndex]

# Get how many columns have the given name
def get_total_column_name(self, column_name) -> int:
    
    my_names = self.get_column_names()
    total    = my_names.count(column_name)

    return total

# ---------------------------------
# Indexes
# ---------------------------------

# For a given column name, return the first index
#
# Return -1 if the column name is not found
def get_column_index(self, column_name) -> int:
    return (utils.find_position_in_list(self.data.columns.to_list(), column_name))

# For a given column name, return a list of boolean
# filters that are True for the rows that have the
# same value as the one given
#
# Return a list of booleans [True, False, True, ...]
#
# Panda use this if you want to filter the columns with common name
def get_columns_location(self, column_name):

    return(utils.find_matches_in_list(self.data.columns.to_list(), column_name))

    # return(self.data.columns.get_loc(column_name)) # OLD

# ---------------------------------
# Total
# ---------------------------------

# Total columns
def ncol(self):
    return self.totalColumns
get_total_columns = ncol 