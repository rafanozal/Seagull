#!/usr/bin/env python3

'''

This file contain functions that modify the contents of the dataframe

'''

# General libraries
import pandas as pd
import numpy as np

from src import constants

# ---------------------------------
# RENAMING
# ---------------------------------
# region

# Rename all columns
def rename_columns(self, newNames):
    self.data = self.data.set_axis(newNames, axis=1, copy=False)

setColumnsNames = rename_columns
renameColumns   = rename_columns

# Rename ONE column
def rename_column(self, columnIndex, newName):
    self.data.rename(columns={self.data.columns[columnIndex]: newName}, inplace=True)

setColumnName   = rename_column
renameColumn    = rename_column

# Rename all rows
def rename_rows(self, newNames):
    self.data = self.data.set_axis(newNames, axis=0, copy=False)

setRowsNames    = rename_rows
renameRows      = rename_rows

# Rename ONE row
def rename_row(self, rowIndex, newName):
    self.data.rename(rows={self.data.rows[rowIndex]: newName}, inplace=True)

setRowName      = rename_row
renameRow       = rename_row

# endregion

# ---------------------------------
# SETTING VALUES
# ---------------------------------
# region

# Set the whole column
def setColumn(self, index, values):
    self.data.iloc[ :  , index ] = values

# Set the whole column to zero values
def setColumnZeroes(self, index):

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

# Set the whole column to zero floats
#def setColumnZeroesF(self, index):
#    self.data.iloc[ :  , index ] = 0
#    self.columnToFloat(index)

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

    self[:,column_index] = np.round(self[:,column_index], decimals = decimals)



# Round the entire dataframe
def round(self, decimals = 2):

    for i in range(self.totalColumns):
        if (self.isNumerical(i)): self.round_column(i, decimals = decimals)

# Normalize the whole dataset
# Only do it in the data that is numerical and can be normalized
def normalize(self, sigmas = False):

    # Count how many numerical columns we have
    total_numerical = 0
    for i in range(self.totalColumns):
        if self.isNumerical(i): total_numerical += 1

    if total_numerical > 0:

        # Find the relevant statistical values
        maximum     = None
        minimum     = None
        mean        = 0
        std         = 0
        total_cells = 0

        for i in range(self.totalColumns):

            if self.isNumerical(i):
                if maximum is None: maximum = self.data.iloc[ :  , i ].max()
                if minimum is None: minimum = self.data.iloc[ :  , i ].min()

                maximum = max(maximum, self.data.iloc[ :  , i ].max())
                minimum = min(minimum, self.data.iloc[ :  , i ].min())

                mean        += self.data.iloc[ :  , i ].sum()
                total_cells += self.data.iloc[ :  , i ].count()

        mean = mean / total_cells

        for i in range(self.totalColumns):
            if self.isNumerical(i):

                squared_diffs = (self.data.iloc[ :  , i ] - mean) ** 2
                std += squared_diffs.sum()

        std = np.sqrt(std / total_cells)

        # Check whether we want to do normalization from respect to the mean and standard deviation

        # If all the data is the same, just set it to one
        # Otherwise do the normal calculation

        # We do the double loop to avoid incompatible dtypes
        # that will pop up if we try to normalize a column with strings

        for i in range(self.totalColumns):

            if self.isNumerical(i):

                for j in range(self.totalRows):

                    if std != 0:

                        if sigmas:
                            self.data.iloc[ j  , i ] = (self.data.iloc[ j  , i ] - mean) / std
                        else:
                            self.data.iloc[ j  , i ] = (self.data.iloc[ j  , i ] - minimum) / (maximum - minimum)

                    else:
                        self.data.iloc[ j  , i ] = 1.0

# Normalize a single column of the dataset
def normalize_column(self, column_index, sigmas = False):

    # Check that the column is numerical
    # Otherwise do nothing and return
    if self.isNumerical(column_index):

        # Find the relevant statistical values
        maximum     = self.data.iloc[ :  , column_index ].max()
        minimum     = self.data.iloc[ :  , column_index ].min()
        mean        = 0
        std         = 0
        total_cells = 0

        """         print("--------------------")
                print("MAX MIN")
                print("Column index: ", column_index)
                print(maximum, minimum)
                print("--------------------")
        """
        mean        += self.data.iloc[ :  , column_index ].sum()
        total_cells += self.data.iloc[ :  , column_index ].count()

        mean = mean / total_cells


        squared_diffs = (self.data.iloc[ :  , column_index ] - mean) ** 2
        std += squared_diffs.sum()

        std = np.sqrt(std / total_cells)

        """         print("--------------------")
                print("MEAN STD")
                print("Column index: ", column_index)
                print(mean, std)
                print("--------------------") """

        # Check whether we want to do normalization from respect to the mean and standard deviation

        # If all the data is the same, just set it to one
        # Otherwise do the normal calculation

        # We do the double loop to avoid incompatible dtypes
        # that will pop up if we try to normalize a column with strings


        for j in range(self.totalRows):

            if std != 0:

                value = self.data.iloc[ j  , column_index ]

                if sigmas:
                    self.data.iloc[ j  , column_index ] = (value - mean)    / std
                else:
                    self.data.iloc[ j  , column_index ] = (value - minimum) / (maximum - minimum)

            else:
                self.data.iloc[ j  , column_index ] = 1.0

# Normalize all columns of the dataset
def normalize_columns(self, sigmas = False):

    for i in range(self.totalColumns):
        self.normalize_column(i, sigmas = sigmas)

# Normalize a single row of the dataset
def normalize_row(self, row_index, sigmas = False):


    # Count how many numerical columns we have
    total_numerical = 0
    for i in range(self.totalColumns):
        if self.isNumerical(i): total_numerical += 1

    if total_numerical > 0:


        # Find the relevant statistical values
        maximum     = None
        minimum     = None
        mean        = 0
        std         = 0
        total_cells = 0

        for i in range(self.totalColumns):

            if self.isNumerical(i):
                if maximum is None: maximum = self.data.iloc[ row_index  , i ]
                if minimum is None: minimum = self.data.iloc[ row_index  , i ]

                maximum = max(maximum, self.data.iloc[ row_index  , i ])
                minimum = min(minimum, self.data.iloc[ row_index  , i ])

                mean        += self.data.iloc[ row_index  , i ]
                total_cells += 1

        for i in range(self.totalColumns):

            if self.isNumerical(i):

                mean        += self.data.iloc[ row_index  , i ]
                total_cells += 1

        mean = mean / total_cells

        for i in range(self.totalColumns):
            if self.isNumerical(i):

                squared_diffs = (self.data.iloc[ row_index  , i ] - mean) ** 2
                std += squared_diffs

        std = np.sqrt(std / total_cells)

        # Check whether we want to do normalization from respect to the mean and standard deviation

        # If all the data is the same, just set it to one
        # Otherwise do the normal calculation

        # We do the double loop to avoid incompatible dtypes
        # that will pop up if we try to normalize a column with strings

        for i in range(self.totalColumns):

            if self.isNumerical(i):

                if std != 0:

                    if sigmas:
                        self.data.iloc[ row_index  , i ] = (self.data.iloc[ row_index  , i ] - mean)    / std
                    else:
                        self.data.iloc[ row_index  , i ] = (self.data.iloc[ row_index  , i ] - minimum) / (maximum - minimum)

                else:
                    self.data.iloc[ row_index  , i ] = 1.0

# Normalize all rows of the dataset
def normalize_rows(self, sigmas = False):

    for i in range(self.totalRows):
        self.normalize_row(i, sigmas = sigmas)


# endregion