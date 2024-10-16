#!/usr/bin/env python3

'''

This file contain functions related to normalization of the data.

This can be done by either normalizing the whole dataset, a single column or a
single row.

This is done by either normalizing the data with respect to the mean and
standard deviation or with respect to the maximum and minimum values.

'''

# General libraries

import numpy as np



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
