import pandas as pd

# ---------------------------------
# CASTING
# ---------------------------------
# region

# Transform a column into a integer type
def columnToInteger(self, columnIndex):

    # Get the name of the index
    currentName = self.getColumnName(columnIndex)

    # Transform the column
    self.data[currentName] = pd.to_numeric(self.data[currentName], errors='coerce').astype('Int64')

# Transform a column into a float type
def columnToFloat(self, columnIndex):

    # THIS IS THE BIGGEST BULLSHIT, MORE THAN R EVEN!, IN THE HISTORY OF PROGRAMMING LANGUAGES
    # Turn out that iloc doesn't change shit: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#why-does-assignment-fail-when-using-chained-indexing
    # It can only read
    # It cannot modify.
    # YOU NEED TO GET THE NAME AND CHANGE BY NAME
    # WHAT. THE FUCK. DESIGN IS THIS CRAP!??

    # Get the name of the index
    currentName = self.getColumnName(columnIndex)

    # Transform the column
    self.data[currentName] = pd.to_numeric(self.data[currentName], errors='coerce').astype('float64')


# Transform a column into a string (object) type
def columnToString(self, columnIndex):

    # Get the name of the index
    currentName = self.getColumnName(columnIndex)

    # Transform the column
    self.data[currentName] = self.data[currentName].astype(str)


# Transform a column into a categorical type
def columnToCategory(self, columnIndex, categoryList = None):

    # Prepare the category list for later
    finalCategoryList    = categoryList
    final_categories_set = None
    if(categoryList!=None): final_categories_set = set(categoryList)

    # Get the name of the index
    currentName = self.getColumnName(columnIndex)

    # Do we have a categorical column or a numerical column?
    if(self.isCategorical(columnIndex)):

        # Get the categories that we have at the moment
        currentCategories      = self.data[currentName].unique()
        current_categories_set = set(currentCategories)

        # If it is a string
        if(self.isCharacter(columnIndex)):

            # Do you wanted an specific order or just the default alphabetical?
            if(categoryList == None):
                finalCategoryList = currentCategories.sort()

            else:
                # Check that the given categories coincide with the unique strings        
                is_subset = current_categories_set.issubset(final_categories_set)

                # If it is not a subset, we have more elements in the table than categories defined in the argument
                if(not(is_subset)):

                    print("WARNING!: There are more elements in the table than")
                    print("          categories defined in the argument 'categoryList'.")
                    print()
                    print("          I converted the extra elements into categories")
                    print("          and sorted them at the end of the given categories")
                    print()
                    print("          You might want to reconsider this step, or delete the")
                    print("          extra elements.")

                    missing_elements  = current_categories_set.difference(final_categories_set)
                    finalCategoryList = finalCategoryList + missing_elements.sort()

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

                finalCategoryList = currentCategories.sort()

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
                    finalCategoryList = finalCategoryList + missing_elements.sort()

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
    self.data[currentName] = pd.Categorical(self.data[currentName], categories = finalCategoryList, ordered = True)

    return(finalCategoryList)


# endregion