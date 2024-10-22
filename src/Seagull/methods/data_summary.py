# General libraries
import pandas as pd
import numpy as np


# Check the data
# > myDF.head()
def head(self):

    return self.data.head()

# Get a summary of a categorical column
#
# Return a dataframe with this form
#
#  ----------------------------
# | Category  | n | N | f | F |
#  ----------------------------
#
#  It can be sorted by:
#
#      - original ,     if categories have being defined, use those, otherwise alphabetical
#      - alphabeticall, 
#      - size
#      - reverse
#      - reverse_size,  does the same as "reverse"
#
#  The results can be cropped using the top option, top <= 0 don't crop anything

def summarize_categorical_column(self, column_index, sort = "original", top = 0):

    # Self
    # This feels hackerish, if put outside the methods the compiler complains
    # That this is a recursive imports, which is true
    #      Seagull -> Summaries -> Seagull
    #
    # However I can't find a way to make it works beside importing manually inside
    # each function. (This doesn't happen in superior C++ of course)
    from ..Seagull import Seagull

    # Transform the column index which might be a string to an integer
    if(type(column_index) == str):
        column_index = self.getColumnIndex(column_index)


    categories = self.get_categories(column_index)
    total_categories = len(categories)

    total_rows = self.totalRows

    resultDF = Seagull(total_categories, 5, dtypes=["category", "int", "int", "float", "float"])
    resultDF.renameColumns(["Category", "n", "N", "f", "F"])
    resultDF.set_categories(0, categories)

    # Init the modalities and count each values
    for i in range(total_categories):
        resultDF[i,0] = categories[i]
        # n
        resultDF[i,1] = self.countByValue(column_index, categories[i])
        # N
        if(i!=0):
            resultDF[i,2] = resultDF[i-1,2] + resultDF[i,1]
        else:
            resultDF[i,2] = resultDF[i,1]
        # f
        resultDF[i,3] = resultDF[i,1] / total_rows
        # F
        if(i!=0):
            resultDF[i,4] = resultDF[i-1,4] + resultDF[i,3]
        else:
            resultDF[i,4] = resultDF[i,3]

    # By default, the entire dataframe is made of float
    # recast the appropiate columns
    resultDF.column_to_integer(1)
    resultDF.column_to_integer(2)

    # Round the frequencies
    # Int columns remain unchanged
    resultDF.round()

    return(resultDF)


