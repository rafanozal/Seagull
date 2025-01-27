#!/usr/bin/env python3

import numpy as np

'''

Provides functionality to filter data based on certain conditions.

'''

# For a given list of columns and a list of values,
# return a mask of rows that have the values in the columns
#
# If only one column is given, return a 1D array of bools
#
# If more than one column is given, return a 2D array of bools
def mask(self, list_of_columns, list_of_values):
    
    # Check if we have a list of columns or only a single column
    # If it is a single value convert it to a list of 1
    if(not isinstance(list_of_columns, list)):
        list_of_columns = [list_of_columns]

    # Same for the list of values
    if(not isinstance(list_of_values, list)):
        list_of_values = [list_of_values]

    # Now we are sure that we have two list in each variable

    # From the list of columns, check that we have strings or indexes
    # If we have strings, convert them to indexes
    for i in range(len(list_of_columns)):
        if(isinstance(list_of_columns[i], str)):
            list_of_columns[i] = self.get_column_index(list_of_columns[i])

    # Duplicated indexes are allowed. I can't think any reason to forbid them
    # and I can't think of any reason of why the user would want to do that either

    # Now we are going to check the values in each column
    # We are going to create a mask for each column

    # Create the return matrix as False
    # We are going to change the values to True if they are in the list
    mask = np.full(( self.totalRows , len(list_of_columns) ), False, dtype=bool)

    # Fill the matrix
    # For each column of the matrix
    for i in range(len(list_of_columns)):
            
        # For each row of the matrix
        for j in range(self.totalRows):

            # If the value is in the list
            if(self.data.iloc[j, list_of_columns[i]] in list_of_values):
                mask[j,i] = True

    # If the mask have only one column, we are going to return a 1D array
    if(mask.shape[1] == 1): mask = mask[:,0]

    return mask


# For a given list of columns and a list of values,
# return a Seagull with the rows that have the values in the columns
#
# If intersect is True, return the rows that have all the values
def inside(self, list_of_columns, list_of_values, intersect = True, inplace = False):

    # Check if we have a list of columns or only a single column
    # If it is a single value convert it to a list of 1
    if(not isinstance(list_of_columns, list)):
        list_of_columns = [list_of_columns]

    # Same for the list of values
    if(not isinstance(list_of_values, list)):
        list_of_values = [list_of_values]

    row_mask             = self.mask(list_of_columns, list_of_values)

    # Refine the mask if we have a matrix
    if(len(list_of_columns)>1):
        if(intersect):        
            row_mask = np.all(row_mask, axis=1)
        else:
            row_mask = np.any(row_mask, axis=1)

    # If we modify the data inplace
    if(inplace):
        self.data      = self[row_mask,:]
        self.totalRows = self.data.shape[0]
        return self
    # If we want a copy
    else:
        mySelfCopy           = self.copy()
        mySelfCopy.data      = mySelfCopy[row_mask,:]
        mySelfCopy.totalRows = mySelfCopy.data.shape[0]
        return mySelfCopy


# For two given string or categorical column, return a dictionary
# with the count of combinations of all categories, such as {A1: {B1: 10, B2: 20}, A2: {B1: 0, B2: 15}}
def filter_bicategorical(self, category_column_A_index, category_column_B_index):

    # Get the categories for each column
    categories_A = self.get_categories(category_column_A_index)
    categories_B = self.get_categories(category_column_B_index)

    # Create the dictionary
    my_dict = {key: {key: 0 for key in categories_B} for key in categories_A}

    # Count the combinations in each and fill the dictionary
    for category_A in categories_A:
        for category_B in categories_B:
            my_dict[category_A][category_B] = self.inside([category_column_A_index, category_column_B_index], [category_A, category_B]).get_total_rows()

    # Return the dictionary
    return my_dict

# For a given string or categorical column, and another column of any
# Return a dictionary with keys the unique categories.
# The values are the list of the other column filtered by the category (can be empty)
def filter_by_category(self, category_column_index, other_column_index):
    
        # Get the categories
        # This will be sorted automatically
        my_categories = self.get_categories(category_column_index)
    
        # Create a dictionary with the filtered values.
        # The keys are the categories. Each has an empty list as default.
        my_dict = {key: [] for key in my_categories}

        # For each unique category
        for category in my_categories:

            # Find the appropiate rows
            current_filtered_df = self.data[self.data.iloc[:, category_column_index] == category]

            # Check that we have more than zero rows
            # Otherwise do nothing (already an empty list)
            if(current_filtered_df.shape[0] > 0):

                # Get the values of the other column filtered by the category
                my_dict[category] = current_filtered_df.iloc[:, other_column_index].tolist()

        # Return the dictionary
        return my_dict

# For a given column, keep only the rows that have the greatest values
# The data must be numerical or datetime
def keep_column_top_values(self, column, topValues = 20, inplace = False):

    # Check the the column is an int, if not, convert it
    if(isinstance(column, str)):
        column = self.get_column_index(column)

    # If we modify the data inplace
    if(inplace):
        # We are going to sort the data
        self.data = self.data.sort_values(self.data.columns[column], ascending=False)

        # We are going to keep only the top rows
        self.data = self.data.head(topValues)

        # We are going to reset the index
        # self.data = self.data.reset_index(drop=True)

        # We are going to update the dimensions
        self.totalRows    = self.data.shape[0]
        self.totalColumns = self.data.shape[1]

        # We are going to return the object
        return self
    
    # If we don't modify the data inplace
    else:
        # We are going to make a copy
        mySelfCopy = self.copy()

        # We are going to sort the data
        mySelfCopy.data = mySelfCopy.data.sort_values(mySelfCopy.data.columns[column], ascending=False)

        # We are going to keep only the top rows
        mySelfCopy.data = mySelfCopy.data.head(topValues)

        # We are going to reset the index
        mySelfCopy.data = mySelfCopy.data.reset_index(drop=True)

        # We are going to update the dimensions
        mySelfCopy.totalRows    = mySelfCopy.data.shape[0]
        mySelfCopy.totalColumns = mySelfCopy.data.shape[1]

        # We are going to return the object
        return mySelfCopy

# Keep only the given columns (index or name)
def keep_columns(self, columns, inplace = False):
    
    # Check that the columns are a list or individual values
    if(not isinstance(columns, list)):
        columns = [columns]

    # For each element of the list, check that it is a string
    for i in range(len(columns)):
        if(isinstance(columns[i], str)):
            columns[i] = self.get_column_index(columns[i])

    # If we modify the data inplace
    if(inplace):
        self.data = self.data.iloc[:,columns]
        self.totalColumns = self.data.shape[1]
        return self

    # If we don't modify the data inplace
    else:
        mySelfCopy = self.copy()
        mySelfCopy.data = mySelfCopy.data.iloc[:,columns]
        mySelfCopy.totalColumns = mySelfCopy.data.shape[1]
        return mySelfCopy

# For a given column, keep only the rows that have the specified value
def keepColumnByValue(self, columnIndex, targetValue, override = False):
    
    # Make a copy and modify the copy instead of the original
    mySelfCopy = self.copy()

    # We are going to keep only the rows that have the target value
    mySelfCopy.data = mySelfCopy.data.loc[mySelfCopy.data[mySelfCopy.data.columns[columnIndex]] == targetValue]
    
    # Reset the index
    mySelfCopy.data = mySelfCopy.data.reset_index(drop=True)
    
    # Update the total rows and columns
    mySelfCopy.totalRows = mySelfCopy.data.shape[0]
    mySelfCopy.totalColumns = mySelfCopy.data.shape[1]    

    # We are going to save the data in case we want to keep it
    if(override == False):
        return mySelfCopy

    # Otherwise, override the object
    else:
        self.data = mySelfCopy.data
        self.totalRows = mySelfCopy.totalRows
        self.totalColumns = mySelfCopy.totalColumns
        return self
    
# Return an integer with how many values are in the given column
def count_by_value(self, columnIndex, targetValue):

    # This is a numpy array that doesn't have the count method
    # converted to list that it has. Maybe there's a more
    # efficient way (C++ pointers <3 ) to do this in PYthon
    # but I can't bother to figure it out now
    myData = self[:,columnIndex].tolist()

    

    return myData.count(targetValue)