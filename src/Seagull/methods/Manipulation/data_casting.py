import pandas as pd

# ---------------------------------
# CASTING
# ---------------------------------
# region

# Transform a column into a integer type
def column_to_integer(self, columnIndex):

    # Get the name of the index
    currentName = self.get_column_name(columnIndex)

    # Transform the column
    self.data[currentName] = pd.to_numeric(self.data[currentName], errors='coerce').astype('Int64')

# Transform a column into a float type
def column_to_float(self, columnIndex):

    # THIS IS THE BIGGEST BULLSHIT, MORE THAN R EVEN!, IN THE HISTORY OF PROGRAMMING LANGUAGES
    # Turn out that iloc doesn't change shit: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#why-does-assignment-fail-when-using-chained-indexing
    # It can only read
    # It cannot modify.
    # YOU NEED TO GET THE NAME AND CHANGE BY NAME
    # WHAT. THE FUCK. DESIGN IS THIS CRAP!??

    # Get the name of the index
    currentName = self.get_column_name(columnIndex)

    # Transform the column
    self.data[currentName] = pd.to_numeric(self.data[currentName], errors='coerce').astype('float64')


# Transform a column into a string (object) type
def column_to_string(self, columnIndex):

    # Get the name of the index
    currentName = self.get_column_name(columnIndex)

    # Transform the column
    self.data[currentName] = self.data[currentName].astype(str)


# Transform a column into a categorical type
def column_to_category(self, columnIndex, categoryList = None):

    # Prepare the category list for later
    finalCategoryList    = categoryList
    final_categories_set = None
    if(categoryList!=None):
        
        invalid_input_nans = False
        for item in finalCategoryList:
            if(pd.isna(item)):
                invalid_input_nans = True
        if(invalid_input_nans):

            finalCategoryList = [item for item in finalCategoryList if not pd.isna(item)]

            print()
            print("WARNING!: You have NaNs in the category list.")
            print("          I will remove them from the list.")
            print()
            print("          The list of categories can't have NaNs.")
            print("          But individual elements in the column can be NaNs.")
            print()
            print("          This might sound counterintuitive, but such is the")
            print("          infinite joy of working with Python and Pandas.")
            print()
        
        final_categories_set = set(categoryList)

    # Get the name of the index
    currentName = self.get_column_name(columnIndex)

    # Do we have a categorical column or a numerical column?
    if(self.isCategorical(columnIndex)):

        # Init the variables
        currentCategories      = None
        current_categories_set = None
        have_invalid_nans      = False

        # Do we really have categories or do we have strings?
        # Categories
        if(self.is_strict_categorical(columnIndex)):

            # Get the categories that we have at the moment
            currentCategories      = self.data[currentName].cat.categories.to_list()
        
        # Strings
        else:

            # Get the categories that we have at the moment
            currentCategories = self.data[currentName].unique()
            # NaN, pd.NA, None, etc. are not considered categories, we need to delete those from the list
            # This will update automatically and all of them will pd.NA later on
            for item in currentCategories:
                if(pd.isna(item)):
                    have_invalid_nans = True

            currentCategories = [item for item in currentCategories if not pd.isna(item)]

            

        current_categories_set = set(currentCategories)

        print("Current categories: " + str(currentCategories))
        print(have_invalid_nans)

        # If it is a string
        if(not self.is_strict_categorical(columnIndex)):

            # Do you wanted an specific order or just the default alphabetical?
            if(categoryList == None):
                finalCategoryList = sorted(currentCategories)

            else:

                # Check that the given categories coincide with the unique strings        
                is_subset = current_categories_set.issubset(final_categories_set)

                # If it is not a subset, we have more elements in the table than categories defined in the argument
                if(not(is_subset)):

                    missing_elements  = current_categories_set.difference(final_categories_set)
                    finalCategoryList = finalCategoryList + sorted(missing_elements)

                    print("WARNING!: There are more elements in the table than")
                    print("          categories defined in the argument 'categoryList'.")
                    print()
                    print("          Current categories: " + str(current_categories_set))
                    print("          Given categories:   " + str(final_categories_set))
                    print("          Missing elements:   " + str(missing_elements))
                    print()
                    print("          I converted the extra elements into categories")
                    print("          and sorted them at the end of the given categories")
                    print()
                    print("          Final categories: " + str(finalCategoryList))
                    print()
                    print("          You might want to reconsider this step, or delete the")
                    print("          extra elements.")

                    
                    

        # If it is categorical
        # We just need to change the order for the new one
        # If there's no new one, change it to alphabetically by default
        else:

            # No new order given
            if(categoryList == None):

                print("WARNING!: You want to change the categories order of a")
                print("          categorical variable, but the given 'categoryList'")
                print("          is empty.")
                print()
                print("          By default, I override the original order into")
                print("          alphabeticall order, including any new category.")

                finalCategoryList = sorted(currentCategories)

            # New order given
            else:

                # Check that the given categories coincide with the unique strings        
                is_subset = current_categories_set.issubset(final_categories_set)

                # The order is not enough to cover all categories
                if(not(is_subset)):

                    print("WARNING!: There are more elements in the table than")
                    print("          categories defined in the argument 'categoryList'.")
                    print()
                    print("          I converted the extra elements into categories")
                    print("          and sorted them at the end of the given categories")

                    missing_elements  = current_categories_set.difference(final_categories_set)
                    finalCategoryList = finalCategoryList + sorted(missing_elements)

    # It was numerical
    else:

        # Get the list of numbers
        list_of_numbers = self[:,columnIndex]

        # Cast to strings and sort them
        list_of_strings = str(list_of_numbers.sort()).unique()

        print("WARNING!: You want me to convert a column into categories")
        print("          but I found all numbers in that column.")
        print()
        print("          I converted them into strings and sort them numerically")
        print()
    
        # If the list is too big give a warning
        if(len(list_of_strings) > 100):

            print("WARNING!: Also, this list is very long!!")
            print("          n = " + str(len(list_of_strings)))
            print()
            print("          are you sure you want to do this?.")
            print("          consider grouping them into bigger categories.")
            print()

        finalCategoryList = list_of_strings

    # Set the categories with whatever we come up at the end
    #print("Setting the categories to: " + str(finalCategoryList))
    self.data[currentName] = pd.Categorical(self.data[currentName], categories = finalCategoryList, ordered = True)

    return(finalCategoryList)


# Transform a column into a date type
def column_to_date(self, columnIndex):

    # Get the name of the index
    currentName = self.get_column_name(columnIndex)

    # Transform the column
    self.data[currentName] = pd.to_datetime(self.data[currentName], errors='coerce')

# endregion