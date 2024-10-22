#!/usr/bin/env python3

'''

Provides functionality to filter data based on certain conditions.

'''

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
def keepColumnTopValues(self, columnIndex, topValues = 20):

    # We are going to sort the data
    self.data = self.data.sort_values(self.data.columns[columnIndex], ascending=False)

    # We are going to keep only the top rows
    self.data = self.data.head(topValues)

    # We are going to reset the index
    # self.data = self.data.reset_index(drop=True)

    # We are going to update the dimensions
    self.totalRows    = self.data.shape[0]
    self.totalColumns = self.data.shape[1]

    # We are going to return the object
    return self


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
def countByValue(self, columnIndex, targetValue):

    # This is a numpy array that doesn't have the count method
    # converted to list that it has. Maybe there's a more
    # efficient way (C++ pointers <3 ) to do this in PYthon
    # but I can't bother to figure it out now
    myData = self[:,columnIndex].tolist()

    

    return myData.count(targetValue)