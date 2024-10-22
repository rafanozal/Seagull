# General libraries
import pandas as pd
import numpy as np

# Import the constants to have access to the toy datasets
from src import constants

# If a column have categorical data, return the categories
# If the column is not categorical, return an empty list
def get_categories(self, index):

    return_categories = []

    # If you try to run this on a non-categorical column, does nothing extra
    if(self.isCategorical(index) == False):
        print()
        print("WARNING!: The column is not categorical")
        print()

    # Otherwise find the categories
    else:

        # If the column is actually a full categorical with levels
        if(self.data.iloc[ :  , index ].dtype == 'category'):
            return_categories = self.data.iloc[ :  , index ].cat.categories.to_list()

        # Otherwise, is just a colection of strings
        else:
            return_categories = self.data.iloc[ :  , index ].unique()

    return (return_categories)



# Check if the column is stricly categorical
# Strings are not considered categorical in this case
def is_strict_categorical(self, column_index:int):

    toReturn = False

    if(self.data.iloc[ :  , column_index ].dtype == "category"):
        toReturn = True
    
    return toReturn

# If the column is actually a full categorical with levels
# Check if they are ordered.
def check_if_ordered(self, column_index:int):

    # Final awser
    toReturn = False

    # Check if the column is categorical in the first place
    is_categorical = self.is_strict_categorical(column_index)
    if(is_categorical == False):

        print("Warning! You asked me if column:")
        print("         Index: " + str(column_index))
        print("         Name:  " + self.getColumnName(column_index))
        print("         is ordered, but it is not even set as categorical.")
        print()
        print("         Returning False anyway.")
        print()

        if(self.isCharacter(column_index)):
            print("         The column is a character column.")
            print()
            print("         This type of columns are a special case because they contain")
            print("         strings, but they are not set extricly as categorical.")
            print()
            print("         Usually this is because there are many unique values")
            print("         and it is not practical to set them as categories.")
            print()
            print("         It could also be that the data was not properly initialized")
            print("         as categorical, but it is actually categorical.")
            print()
            print("         You can still convert this into a full categorical column")
            print("         using the method 'my_seagull.set_as_categorical(column_index)'.")
            print()
        
    else:

        # Retrieve the column and check for order
        column   = self.data.iloc[:, column_index]
        toReturn = column.cat.ordered

    # Return the answer
    return toReturn

is_ordered_categorical = check_if_ordered


# Set the categories of a column
#
#     First we need to figure out if we have categories with or without order:
#
#     (S)    Old categories [A < B < C < D]  (order)
#     (NS)   Old categories [A , B , C , D]  (no order)
#
#     Categories without order sometimes can be sorted, but sometimes not.
#     Categories that are sorted can always be transformed into no order categories.
#
#     Then we need to check if the new categories are a subset of the old categories or not:
#
#     (+) If we have more categories in the new categories, than categories in the data, this is fine.
#
#     (=) If we have the same categories in the new categories and in the the data, this is perfect.
#
#     (-) If we have less categories in the new categories, than categories in the data, this is not fine.
#     In this case we raise a warning, and we include the missing categories in the new categories. Making
#     this a perfect case (=).
#
#
#      In total we have these possible case combinations
#
#      F: Fine
#      W: Warning
#      E: Error   (never!, we are permisive)

#           | (S+)  |  (S=)  |  (S-)  |  (NS+)  |  (NS=)  | (NS-)  |  <---- New categories
#      (S)  |   F   |   F    |   W    |   F     |   F     |   W    |      
#      (NS) |   F   |   F    |   W    |   F     |   F     |   W    |
#        ^
#        |
#        |_ Old categories
#
#
#      (S)  to (S+)  Fine    :  [A < B < C]     to [A < B < C < D]
#      (S)  to (S=)  Fine    :  [A < B < C]     to [B < A < C]
#      (S)  to (S-)  Warning :  [A < B < C < D] to [A < B < C]       , what do we do with D that already exist? It need to be sorted somewhere!
#      (S)  to (NS+) Fine    :  [A < B < C]     to [A , B , C , D]
#      (S)  to (NS=) Fine    :  [A < B < C]     to [A , B , C]
#      (S)  to (NS-) Warning :  [A < B < C < D] to [A , B , C]       , what do we do with D that already exist? It need to be included somewhere!
#      (NS) to (S+)  Fine    :  [A , B , C]     to [A < B < C < D]
#      (NS) to (S=)  Fine    :  [A , B , C]     to [B < A < C]
#      (NS) to (S-)  Warning :  [A , B , C , D] to [A < B < C]       , what do we do with D that already exist? It need to be sorted somewhere!
#      (NS) to (NS+) Fine    :  [A , B , C]     to [A , B , C , D]
#      (NS) to (NS=) Fine    :  [A , B , C]     to [A , B , C]
#      (NS) to (NS-) Warning :  [A , B , C , D] to [A , B , C]       , what do we do with D that already exist? It need to be included somewhere!
#
#      For S to S- and NS to S- we need to figure out what to do with the missing categories.
#      In our case, we keep them, but we sorted them as minimum value, so they are at the beginning.
#      They are keept at the orinal sorted order:
# 
#      [A < B < C < D < E] to [A < C < E]  => [B < D < A < C < E]
#
#      For S to NS- and NS to NS- we just warn the user that we are keeping the missing categories. No order needed.
def set_categories(self, column_index:int, new_categories, new_are_ordered = False):

    # First, check if the column where you want to set the categories
    # is actually a categorical column.
    if not self.is_strict_categorical(column_index):
        print("Warning! You are trying to set categories in a column that is not categorical.")
        print("         Index: " + str(column_index))
        print("         Name:  " + self.getColumnName(column_index))
        print("         Returning without doing anything.")
        print()

        if(self.isCharacter(column_index)):
            print("         The column is a character column.")
            print()
            print("         This type of columns are a special case because they contain")
            print("         strings, but they are not set extricly as categorical.")
            print()
            print("         Usually this is because there are many unique values")
            print("         and it is not practical to set them as categories.")
            print()
            print("         It could also be that the data was not properly initialized")
            print("         as categorical, but it is actually categorical.")
            print()
            print("         You can still convert this into a full categorical column")
            print("         using the method 'my_seagull.set_as_categorical(column_index)'.")

    # If it is a categorical column, we can proceed
    else:

        # Check if we are in S or NS case:
        # ---- If the old categories are sorted or unsorted
        old_is_ordered = self.check_if_ordered(column_index)

        # Check if we are in + , = , - case:
        # ---- Grab the old categories
        old_categories = self.get_categories(column_index)

        # Check if the old categories are a subset of the new categories
        old_categories_set            = set(old_categories)
        new_categories_set            = set(new_categories)
        old_categories_set_is_smaller = old_categories_set < new_categories_set
        old_categories_set_is_equal   = old_categories_set == new_categories_set
        old_categories_set_is_bigger  = old_categories_set > new_categories_set

        # Now we can do all the combinations as needed

        #      (S)  to (S+)  Fine    :  [A < B < C]     to [A < B < C < D]
        if(old_is_ordered and new_are_ordered and old_categories_set_is_smaller):
            self.data.iloc[:, column_index] = self.data.iloc[:, column_index].cat.set_categories(new_categories, ordered=True, inplace=True)

        #      (S)  to (S=)  Fine    :  [A < B < C]     to [B < A < C]
        elif(old_is_ordered and new_are_ordered and old_categories_set_is_equal):
            self.data.iloc[:, column_index] = self.data.iloc[:, column_index].cat.set_categories(new_categories, ordered=True, inplace=True)

        #      (S)  to (S-)  Warning :  [A < B < C < D] to [A < B < C]       , what do we do with D that already exist? It need to be sorted somewhere!
        elif(old_is_ordered and new_are_ordered and old_categories_set_is_bigger):

            # Get the categories that are missing
            missing_categories = old_categories_set - new_categories_set

            # Add the missing categories at the end with the original order
            final_categories = list(missing_categories) + new_categories
            self.data.iloc[:, column_index] = self.data.iloc[:, column_index].cat.set_categories(final_categories, ordered=True, inplace=True)

            print("Warning! You are trying to set new categories that are a subset of the old categories.")
            print("         Index: " + str(column_index))
            print("         Name:  " + self.getColumnName(column_index))
            print("         Old categories: " + str(old_categories))
            print("         New categories: " + str(new_categories))
            print()
            print("         The missing categories are: " + str(missing_categories))
            print()
            print("         The missing categories where added in the original order before any new category.")
            print()
            print("         The final categories are." + str(final_categories))
            print()

        #      (S)  to (NS+) Fine    :  [A < B < C]     to [A , B , C , D]
        elif(old_is_ordered and not new_are_ordered and old_categories_set_is_smaller):
            self.data.iloc[:, column_index] = self.data.iloc[:, column_index].cat.set_categories(new_categories, ordered=False, inplace=True)

        #      (S)  to (NS=) Fine    :  [A < B < C]     to [A , B , C]
        elif(old_is_ordered and not new_are_ordered and old_categories_set_is_equal):
            self.data.iloc[:, column_index] = self.data.iloc[:, column_index].cat.set_categories(new_categories, ordered=False, inplace=True)

        #      (S)  to (NS-) Warning :  [A < B < C < D] to [A , B , C]       , what do we do with D that already exist? It need to be included somewhere!
        elif(old_is_ordered and not new_are_ordered and old_categories_set_is_bigger):

            # Get the categories that are missing
            missing_categories = old_categories_set - new_categories_set

            # Add the missing categories at the end with the original order
            final_categories = list(missing_categories) + new_categories
            self.data.iloc[:, column_index] = self.data.iloc[:, column_index].cat.set_categories(final_categories, ordered=False, inplace=True)

            print("Warning! You are trying to set new categories that are a subset of the old categories.")
            print("         Index: " + str(column_index))
            print("         Name:  " + self.getColumnName(column_index))
            print("         Old categories: " + str(old_categories))
            print("         New categories: " + str(new_categories))
            print()
            print("         The missing categories are: " + str(missing_categories))
            print()
            print("         The final categories are." + str(final_categories))
            print()

        #      (NS) to (S+)  Fine    :  [A , B , C]     to [A < B < C < D]
        elif(not old_is_ordered and new_are_ordered and old_categories_set_is_smaller):
            print(new_categories)
            self.data.iloc[:, column_index] = self.data.iloc[:, column_index].cat.set_categories(new_categories, ordered=True)

        #      (NS) to (S=)  Fine    :  [A , B , C]     to [B < A < C]
        elif(not old_is_ordered and new_are_ordered and old_categories_set_is_equal):
            self.data.iloc[:, column_index] = self.data.iloc[:, column_index].cat.set_categories(new_categories, ordered=True)

        #      (NS) to (S-)  Warning :  [A , B , C , D] to [A < B < C]       , what do we do with D that already exist? It need to be sorted somewhere!
        elif(not old_is_ordered and new_are_ordered and old_categories_set_is_bigger):

            # Get the categories that are missing
            missing_categories = old_categories_set - new_categories_set

            # Add the missing categories at the end with the original order
            final_categories = list(missing_categories) + new_categories
            self.data.iloc[:, column_index] = self.data.iloc[:, column_index].cat.set_categories(final_categories, ordered=True)

            print("Warning! You are trying to set new categories that are a subset of the old categories.")
            print("         Index: " + str(column_index))
            print("         Name:  " + self.getColumnName(column_index))
            print("         Old categories: " + str(old_categories))
            print("         New categories: " + str(new_categories))
            print()
            print("         The missing categories are: " + str(missing_categories))
            print()
            print("         The missing categories where added in the original order before any new category.")
            print()
            print("         The final categories are." + str(final_categories))
            print()


        #      (NS) to (NS+) Fine    :  [A , B , C]     to [A , B , C , D]
        elif(not old_is_ordered and not new_are_ordered and old_categories_set_is_smaller):
            self.data.iloc[:, column_index] = self.data.iloc[:, column_index].cat.set_categories(new_categories, ordered=False)

        #      (NS) to (NS=) Fine    :  [A , B , C]     to [A , B , C]
        elif(not old_is_ordered and not new_are_ordered and old_categories_set_is_equal):
            self.data.iloc[:, column_index] = self.data.iloc[:, column_index].cat.set_categories(new_categories, ordered=False)

        #      (NS) to (NS-) Warning :  [A , B , C , D] to [A , B , C]       , what do we do with D that already exist? It need to be included somewhere!
        elif(not old_is_ordered and not new_are_ordered and old_categories_set_is_bigger):

            # Get the categories that are missing
            missing_categories = old_categories_set - new_categories_set

            # Add the missing categories at the end with the original order
            final_categories = list(missing_categories) + new_categories
            self.data.iloc[:, column_index] = self.data.iloc[:, column_index].cat.set_categories(final_categories, ordered=False)

            print("Warning! You are trying to set new categories that are a subset of the old categories.")
            print("         Index: " + str(column_index))
            print("         Name:  " + self.getColumnName(column_index))
            print("         Old categories: " + str(old_categories))
            print("         New categories: " + str(new_categories))
            print()
            print("         The missing categories are: " + str(missing_categories))
            print()
            print("         The final categories are." + str(final_categories))
            print()        
                
setCategories = set_categories            


# Remove extra categories
def remove_extra_categories(self, column_index:int):
    
    # First, check if the column where you want to set the categories
    # is actually a categorical column.
    if not self.is_strict_categorical(column_index):
        print("Warning! You are trying to remove extra categories in a column that is not categorical.")
        print("         Index: " + str(column_index))
        print("         Name:  " + self.getColumnName(column_index))
        print("         Returning without doing anything.")
        print()

        if(self.isCharacter(column_index)):
            print("         The column is a character column.")
            print()
            print("         This type of columns are a special case because they contain")
            print("         strings, but they are not set extricly as categorical.")
            print()
            print("         Usually this is because there are many unique values")
            print("         and it is not practical to set them as categories.")
            print()
            print("         It could also be that the data was not properly initialized")
            print("         as categorical, but it is actually categorical.")
            print()
            print("         You can still convert this into a full categorical column")
            print("         using the method 'my_seagull.set_as_categorical(column_index)'.")

    # If it is a categorical column, we can proceed
    else:

        # Check if we are in S or NS case:
        old_is_ordered = self.check_if_ordered(column_index)

        # Grab the old categories
        old_categories = self.getCategories(column_index)

        # Grab the unique values in the column
        unique_values = self.data.iloc[:, column_index].unique()

        # Check if the old categories are a subset of the unique values
        old_categories_set            = set(old_categories)
        unique_categories_set         = set(unique_values)
        old_categories_set_is_smaller = old_categories_set < unique_categories_set   # We have A,B,C, which categories A,B,  This is impossible!
        old_categories_set_is_equal   = old_categories_set == unique_categories_set  # We have A,B,C, which categories A,B,C (no need to do anything)
        old_categories_set_is_bigger  = old_categories_set > unique_categories_set   # We have A,B,C, which categories A,B,C,D,E

        # Now we can do all the combinations as needed
        if(old_categories_set_is_bigger):

            new_categories = unique_values
            self.data.iloc[:, column_index] = self.data.iloc[:, column_index].cat.set_categories(new_categories, ordered=old_is_ordered)

        elif(old_categories_set_is_smaller):

            print("ERROR! You are trying to remove extra categories")
            print("       in a column that has less categories defined")
            print("       than unique values in the column!.")
            print()
            print("       Index: " + str(column_index))
            print("       Name:  " + self.getColumnName(column_index))
            print("       Old categories: " + str(old_categories))
            print("       Unique values:  " + str(unique_values))
            print()
            print("       Returning without doing anything.")
            print()
            print("       This is an impossible case, and it should never happen.")
            print("       Please report this.")


# Remove NA values category if possible
#
# You might want to keep the extra categories that are zero,
# but you might want to remove the NA category.
#
# If your categories include pd.NA, check if that
# value is actually in the column values.
#
# If it is in the column, do nothing.
# If is not in the column, remove it from the categories.
def remove_NA_category(self, column_index:int):

    # First, check if the column where you want to set the categories
    # is actually a categorical column.
    if not self.is_strict_categorical(column_index):
        print("Warning! You are trying to remove the NA category in a column that is not categorical.")
        print("         Index: " + str(column_index))
        print("         Name:  " + self.getColumnName(column_index))
        print("         Returning without doing anything.")
        print()

        if(self.isCharacter(column_index)):
            print("         The column is a character column.")
            print()
            print("         This type of columns are a special case because they contain")
            print("         strings, but they are not set extricly as categorical.")
            print()
            print("         Usually this is because there are many unique values")
            print("         and it is not practical to set them as categories.")
            print()
            print("         It could also be that the data was not properly initialized")
            print("         as categorical, but it is actually categorical.")
            print()
            print("         You can still convert this into a full categorical column")
            print("         using the method 'my_seagull.set_as_categorical(column_index)'.")

    # If it is a categorical column, we can proceed
    else:

        # Check if we are in S or NS case:
        old_is_ordered = self.check_if_ordered(column_index)

        # Grab the old categories
        old_categories = self.getCategories(column_index)

        # Check if pd.NA is part of the old categories
        na_was_category = pd.NA in old_categories

        # If was part of the categories, try to delete it
        # If it wasn't, there's nothing to remove, so don't do anything extra.
        if(na_was_category):

            # Check if the column has NA values
            has_na = pd.NA in self.data.iloc[:, column_index]

            # If the column has NA values, do nothing
            # But warn the user
            if(has_na):

                print("Warning! You are trying to remove the NA category in a column that has NA values.")
                print("         Index: " + str(column_index))
                print("         Name:  " + self.getColumnName(column_index))
                print()
                print("         The NA category was not removed.")
                print()
                print("         You need to change the NA values to something else first.")
                print("         For example, make them as 'Uknown' instead of NA.")
                print()

            else:

                # Remove the NA category
                new_categories = old_categories[old_categories != pd.NA]
                self.data.iloc[:, column_index] = self.data.iloc[:, column_index].cat.set_categories(new_categories, ordered=old_is_ordered)

# Swap the NA category values for a new value
# By deafult, the new value is "Unknown"
#
# If the categories were ordered, the new categories will be placed at the end.
# You can then modify the order as needed later.
def swap_NA_category(self, column_index:int, new_value = "Uknown"):

    # First, check if the column where you want to set the categories
    # is actually a categorical column.
    if not self.is_strict_categorical(column_index):
        print("Warning! You are trying to remove the NA category in a column that is not categorical.")
        print("         Index: " + str(column_index))
        print("         Name:  " + self.getColumnName(column_index))
        print("         Returning without doing anything.")
        print()

        if(self.isCharacter(column_index)):
            print("         The column is a character column.")
            print()
            print("         This type of columns are a special case because they contain")
            print("         strings, but they are not set extricly as categorical.")
            print()
            print("         Usually this is because there are many unique values")
            print("         and it is not practical to set them as categories.")
            print()
            print("         It could also be that the data was not properly initialized")
            print("         as categorical, but it is actually categorical.")
            print()
            print("         You can still convert this into a full categorical column")
            print("         using the method 'my_seagull.set_as_categorical(column_index)'.")

    # If it is a categorical column, we can proceed
    else:

        # Check if we are in S or NS case:
        #old_is_ordered = self.check_if_ordered(column_index)

        # Grab the old categories
        #old_categories = self.getCategories(column_index)

        # Check if whatever NaN category exist is part of the old categories
        #na_was_category = constants.CATEGORICAL_NAN in old_categories

        # Check if whatever NaN category exist is part of the values in the column
        na_was_category = False
        my_data = (self.data.iloc[:, column_index]).to_list()
        i = 0
        my_data_len = len(my_data)
        while (not na_was_category) and (i < my_data_len):
            if(pd.isna(my_data[i])):
                na_was_category = True
            i = i + 1
         
        #na_was_category = constants.CATEGORICAL_NAN in (self.data.iloc[:, column_index]).to_list()

        # If was part of the categories, try to delete it
        # If it wasn't, there's nothing to remove, so don't do anything extra.
        if(na_was_category):
       
            self.data.iloc[:, column_index] = self.data.iloc[:, column_index].cat.add_categories(new_value) # IS IMPOSSIBLE TO NOT GET A FUTURE WARNING!!
            self.data.iloc[:, column_index] = self.data.iloc[:, column_index].fillna(new_value)