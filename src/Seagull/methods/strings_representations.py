#!/usr/bin/env python3

'''

This file contain the string representation functions for the Seagull class

'''


# Shows an overview of the data limitted to the first r rows and c columns
# Choosing None will display all rows or columns
def str_square(self, r = 5, c = 5):

    # Return string
    my_return_str = ""

    # Set display options    
    self.data.set_option('display.max_rows', r)  
    self.data.set_option('display.max_columns', c)  # or None to display all columns

    # Get the string
    my_return_str = self.data.to_string()

    # Reset back display options to default
    self.data.reset_option('display.max_rows')
    self.data.reset_option('display.max_columns')

    # Return the string
    return(my_return_str)

# Shows all the data
def str_complete(self):
    return((self.data).to_string())

def print_all_data(self):
    return((self.data).to_string())

# Show complete state of the Seagull 
# and the first n rows of the data, by default, 5 only.
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
        str_final = str_final + "     " + str(i) + " | " + columnsNormalized[i] + " : " + str(myTypes[i]) + "\n"
        
    str_final = str_final + "---------------\n"
    str_final = str_final + "    Preview    \n"
    str_final = str_final + "---------------\n"
    str_final = str_final + str(self.data.head( n = preview )) + "\n"
    str_final = str_final + "---------------\n"

    return(str_final)

# Default to_str method
def to_string(self):
    return(str_overview(self, 5))

# Show the types only with extended information:
#
# - The number of columns of each type
#
# - For each column:
#
#     Index | Column Name : Type |
#
#           for ints:       Min, Max, Mean, Std
#           for floats:     Min, Max, Mean, Std
#           for strings:    Unique values with count
#           for categories: Unique values with count, sorted by category.
#           for dates:      Min, Max
def describe_types(self):
    
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
    
        # Update the types
        myTypes = self.getColumnTypes()
    
        for i in range(self.totalColumns):
            str_final = str_final + "     " + str(i) + " | " + columnsNormalized[i] + " : " + str(myTypes.iloc[i])

            # If it is an integer or a float we can calculate some statistics
            if self.isNumerical(i):
                str_final = str_final + " | Min: " + str(self.data.iloc[:,i].min()) + " | Max: " + str(self.data.iloc[:,i].max()) + " | Mean: " + str(self.data.iloc[:,i].mean()) + " | Std: " + str(self.data.iloc[:,i].std())
                
            # If it is a string we can calculate the unique values
            elif self.isCharacter(i):
                str_final = str_final + " | " 

                for unique_str in self.data.iloc[:,i].unique():
                    str_final = str_final + str(unique_str) + " (" + str(self.data.iloc[:,i].value_counts()[unique_str]) + "), "

            # If it is a category we can calculate the unique values as well, but sorted.
            elif self.isCategorical(i):
                str_final = str_final + " | " 

                my_categories = self.getCategories(i)

                for category in my_categories:
                    str_final = str_final + str(category) + " (" + str(self.data.iloc[:,i].value_counts()[category]) + "), "

            # If it is a date we can calculate the min and max
            elif self.isDate(i):
                str_final = str_final + " | Min: " + str(self.data.iloc[:,i].min()) + " | Max: " + str(self.data.iloc[:,i].max())

                str_final = str_final + "\n"

            # If it is something else, we just say we have no idea of what it is.
            else:
                str_final = str_final + " | I have no idea of what is this type !!"

            str_final = str_final + "\n"
    
        return(str_final)