#!/usr/bin/env python3

'''

This file contain the string representation functions for the Seagull class

'''

def print_all_data(self):

    print(self.data)

# Show the first n rows of the data, by default, 5 only.
def print_overview(self, preview = 5):

    # We are going to save in this list the name of the columns
    # but we are going to add spaces to the right to make them
    # all the same size
    columnsNormalized = self.getColumnNames()

    # We are going to find the longest name
    longestName = 0
    for i in range(len(columnsNormalized)):
        if len(columnsNormalized[i]) > longestName:
            longestName = len(columnsNormalized[i])

    # We are going to add spaces to the right
    for i in range(len(columnsNormalized)):
        columnsNormalized[i] = columnsNormalized[i].ljust(longestName)

    # From here on we do the printing of all values of interest.

    print("---------------")
    print()
    print(" Dimensions: ")
    print()
    print("     " + str(self.totalRows) + " x " + str(self.totalColumns))    
    print()
    print("---------------")
    print()
    print(" Datatypes: ")

    for i in range(self.totalColumns):
        print("     " + str(i) + " | " + columnsNormalized[i] + " : " + str(self.getColumn(i).dtype))

    print()
    print("---------------")
    print()
    print(self.data.head(n=preview))