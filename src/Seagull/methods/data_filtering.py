#!/usr/bin/env python3

'''

Provides functionality to filter data based on certain conditions.

'''

# For a given column, keep only the rows that have the greatest values
def keepColumnTopValues(self, columnIndex, topValues = 20):

    # We are going to sort the data
    self.data = self.data.sort_values(self.data.columns[columnIndex], ascending=False)

    # We are going to keep only the top rows
    self.data = self.data.head(topValues)

    # We are going to reset the index
    self.data = self.data.reset_index(drop=True)

    # We are going to update the total rows
    self.totalRows = self.data.shape[0]

    # We are going to update the total columns
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