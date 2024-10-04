#!/usr/bin/env python3

'''

This file contain the string representation functions for the Seagull class

'''



# Show the first n rows of the data, by default, 5 only.
def str_overview(self, preview = 5):

    # Final string
    str_final = ""

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

    str_final = str_final + "---------------\n"
    str_final = str_final + " rows x columns: " + str(self.totalRows) + " x " + str(self.totalColumns) + "\n"
    str_final = str_final + "---------------\n"
    str_final = str_final + " Datatypes:    \n"

    # Update the types
    myTypes = self.getColumnTypes()

    for i in range(self.totalColumns):
        str_final = str_final + "     " + str(i) + " | " + columnsNormalized[i] + " : " + str(myTypes.iloc[i]) + "\n"
        
    str_final = str_final + "---------------\n"
    str_final = str_final + "    Preview    \n"
    str_final = str_final + "---------------\n"
    str_final = str_final + str(self.data.head( n = preview )) + "\n"
    str_final = str_final + "---------------\n"

    return(str_final)

def str_complete(self):
    return((self.data).to_string())

def print_all_data(self):
    return((self.data).to_string())