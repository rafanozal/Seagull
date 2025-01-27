
import src.constants as constants

# Solve the column alias
#
# Some methods have both a numerical column and a name column as input parameter.
# This method solves the ambiguity by choosing the numerical column if both are given.
#
# Only Index is given:     Use it
# Only Name is given:      Use to find the first numerical index later
# Index and Name is given: Numerical wins -> Name is ignored -> Warning is printed
# None is given:           This is allowed when the user wants to init to random data


def solve_index_and_column(numerical_column_index, name_column_string):

    # Return variable
    #
    # Default to -1 meaning we don't have a valid index
    return_value_index = -1
 
    # We don't have the index
    if(numerical_column_index == None):
            
        # But we have the column alias
        if(name_column_string != None):
            
            return_value_index = name_column_string # In this case, we return the column string name, to be found out later

        # We don't have anything
        # This is allowed, the user might change it later, but can't init the analysis with data now if that was the idea
        # The return value is kept as -1

    # We have the index
    else:

        # Check if the index is a valid integer
        if (type(numerical_column_index) not in constants.INTEGER_TYPES):
            print()
            print("ERROR!: The given index is not a valid integer.")
            print("        I can't look inside the data.")
            print()

        # If we have an index, we can use it
        else:
            return_value_index = numerical_column_index

            # But we also have the column?
            # Ignore the column
            if(name_column_string != None):
                print()
                print("WARNING!: Both column name ("+ str(name_column_string) +")")
                print("          and numerical column index ("+ str(numerical_column_index) +") were given.")
                print("          numerical column index will be used.")
                print()

            # If we don't have the column
            # That's also fine, we are using the index already

    return return_value_index


# Solve the column alias
#
# Some methods have numerical column index as input parameter.
# This method check if actually the given index is valid.
# If not, it will check if the given name is valid and transform it to an index.
#
# Return <0 if no valid index was found
#        -1 invalid datatype
#        -2 invalid index (no int or string given)
#        -3 invalid name (not found in the column names)
#        -4 invalid range (index out of range)
#        -5 invalid type
# Return the index if a valid index was found
def solve_index(data, numerical_column_index, expected_data_type = None, silent_error = False, silent_warning = False):

    #print("Solving index")
    #print("Index: " + str(numerical_column_index))
    #print(type(numerical_column_index))
    #print("Expected data type: " + str(expected_data_type))


    # Return variable
    #
    # Default to -1 meaning we don't have a valid index
    return_value_index = -1

 
    # First, let check that we somehow have a valid index (either int or name)
    valid_candaidate  = False
    candidate_integer = False
    if(numerical_column_index != None):
    
        # Check if the index is a valid integer
        if (type(numerical_column_index) in constants.INTEGER_TYPES):
            candidate_integer = True
            valid_candaidate  = True

        # If it is not a valid integer, check that it is a valid string
        elif(type(numerical_column_index) == str): valid_candaidate = True

        # If it is not either, this is an error
        else:

            return_value_index = -2

            if(silent_error == False):
                print()
                print("ERROR!: The given index ("+ str(numerical_column_index) +") is not a valid integer.")
                print("        I can't look inside the data.")
                print()

    # Check the type of data we have
    if(data != None):

        # If the data is a Seagull object
        if(type(data).__name__ == 'Seagull' and valid_candaidate):

            # If it is a string, we need to find the index first
            # If it is an integer, we need to check that is valid
            # In either case, we use this variable to store the final index
            final_index = -1

            # If the index is a name instead of a index
            if(candidate_integer == False):

                # Check that such name exist, and return the first match
                index_candidate = data.get_column_index(numerical_column_index)

                #print("Index candidate: " + str(index_candidate))

                if(index_candidate < 0):

                    return_value_index = -3

                    if(silent_error == False):

                        print()
                        print("ERROR!: The given column: " + str(numerical_column_index) + " is not valid.")
                        print("        I tried to find the name and couldn't find an index for that column.")
                        print()
                        print("        Current columns are:.")
                        print()
                        print("        " + str(data.get_columns_names()))
                        print()

                else:
                    final_index = index_candidate
            else:
                final_index = numerical_column_index

            #print("Final index: " + str(final_index))

            # Up to this point, we have finally an integer index
            # Check if the index is between the valid range
            if(final_index >= 0 and final_index < data.get_total_columns()):

                # At this point the index is valid.
                # The user might want to check that the expected datatype is also valid

                # If the user doesn't care about the data type, we can use it
                if(expected_data_type == None):
                    return_value_index = final_index
                # Otherwise, do a final check
                else:
                    # Check if we have a list of candidates or just one type
                    if(type(expected_data_type).__name__ == 'list'):

                        #print("--------------------")
                        #print("Data type: " + str(data.get_column_types()[final_index]))
                        #print(data.get_column_types()[final_index])
                        #print(type(data.get_column_types()[final_index]))
                        #print("Expected data type: " + str(expected_data_type))
                        #print(type(expected_data_type))
                        #print()
                        #print("FINAL TEST:")
                        #print()
                        #print(type(data.get_column_types()[final_index]) in expected_data_type)
                        #print("--------------------")

                        if( type(data.get_column_types()[final_index]) in expected_data_type):
                        #if( isinstance( type(data.get_column_types()[final_index]), tuple(expected_data_type)) ):

                            return_value_index = final_index

                        else:

                            return_value_index = -5

                            if(silent_error == False):

                                print()
                                print("ERROR!: The given column is not of the expected type.")
                                print("        Column:        " + str(final_index))
                                print("        Expected type: " + str(expected_data_type) + ".")
                                print("        Actual type:   " + str(data.get_column_types()[final_index]) + ".")
                                print()
                    else:
                        if(data.get_column_types()[final_index] == expected_data_type):
                            return_value_index = final_index
                        else:
                            return_value_index = -5

                            if(silent_error == False):

                                print()
                                print("ERROR!: The given column: " + str(final_index) + " is not of the expected type.")
                                print("        The expected type was: " + str(expected_data_type) + ".")
                                print("        The actual type is: " + str(data.get_column_types()[final_index]) + ".")
                                print()
                        
            # If it is not valid range, give the error
            else:

                return_value_index = -4

                if(silent_error == False):
                    print()
                    print("ERROR!: The given index: " + str(final_index) + " is out of range.")
                    print("        The data set has " + str(data.get_total_columns()) + " columns.")
                    print("        Remember the first column is index 0.")
                    print()

        # If the data is a pandas dataframe
        elif(type(data).__name__ == 'DataFrame' and valid_candaidate):

            # We have to do the same as in Seagull, but the code is adapted for pandas instead

            # If it is a string, we need to find the index first
            # If it is an integer, we need to check that is valid
            # In either case, we use this variable to store the final index
            final_index = -1

            # If the index is a name instead of a index
            if(candidate_integer == False):

                try:
                    # Attempt to get the index of the column
                    index_candidate = data.columns.get_loc(final_index)
                except KeyError:
                    # If the column is not found, return -1
                    index_candidate =  -1

                if(index_candidate < 0):

                    return_value_index = -3

                    if(silent_error == False):

                        print()
                        print("ERROR!: The given column: " + str(final_index) + " is not valid.")
                        print("        I tried to find the name and couldn't find an index for that column.")
                        print()
                        print("        Current columns are:.")
                        print()
                        print("        " + str(data.get_columns_names()))
                        print()

                else:
                    final_index = index_candidate
            else:
                final_index = numerical_column_index


            # Up to this point, we have finally an integer index
            # Check if the index is between the valid range
            if(final_index >= 0 and final_index < data.shape[1]):

                # At this point the index is valid.
                # The user might want to check that the expected datatype is also valid

                # If the user doesn't care about the data type, we can use it
                if(expected_data_type == None):
                    return_value_index = final_index
                # Otherwise, do a final check
                else:
                    # Check if we have a list of candidates or just one type
                    if(type(expected_data_type).__name__ == 'list'):
                        if(data.get_column_types()[final_index] in expected_data_type):
                            return_value_index = final_index
                        else:

                            return_value_index = -5

                            if(silent_error == False):

                                print()
                                print("ERROR!: The given column: " + str(final_index) + " is not of the expected type.")
                                print("        The expected type was: " + str(expected_data_type) + ".")
                                print("        The actual type is: " + str(data.get_column_types()[final_index]) + ".")
                                print()
                    else:
                        if(data.get_column_types()[final_index] == expected_data_type):
                            return_value_index = final_index
                        else:
                            return_value_index = -5

                            if(silent_error == False):

                                print()
                                print("ERROR!: The given column: " + str(final_index) + " is not of the expected type.")
                                print("        The expected type was: " + str(expected_data_type) + ".")
                                print("        The actual type is: " + str(data.get_column_types()[final_index]) + ".")
                                print()
                        
            # If it is not valid range, give the error
            else:

                return_value_index = -4

                if(silent_error == False):
                    print()
                    print("ERROR!: The given index: " + str(final_index) + " is out of range.")
                    print("        The data set has " + str(data.get_total_columns() + " columns."))
                    print("        Remember the first column is index 0.")
                    print()

        # If the data is a numpy array
        elif(type(data).__name__ == 'ndarray' and valid_candaidate):

            # If the user gave you an index, this is irrelevant
            # numpy arrays don't have column names or indexes, is only one unique array
            if(silent_warning == False):
                print()
                print("WARNING!: The given data is a numpy array.")
                print("          The column index or name is irrelevant.")

            # The only thing left to do is to check the data type
            # if the user want to check it even
            # If the user doesn't care about the data type, we can use it
            if(expected_data_type == None):
                return_value_index = final_index
            # Otherwise, do a final check
            else:
                # Check if we have a list of candidates or just one type
                if(type(expected_data_type).__name__ == 'list'):
                    if(data.dtype in expected_data_type):
                        return_value_index = final_index
                    else:

                        return_value_index = -5

                        if(silent_error == False):

                            print()
                            print("ERROR!: The given column: " + str(final_index) + " is not of the expected type.")
                            print("        The expected type was: " + str(expected_data_type) + ".")
                            print("        The actual type is: " + str(data.dtype) + ".")
                            print()
                else:
                    if(data.dtype == expected_data_type):
                        return_value_index = final_index
                    else:
                        return_value_index = -5

                        if(silent_error == False):

                            print()
                            print("ERROR!: The given column: " + str(final_index) + " is not of the expected type.")
                            print("        The expected type was: " + str(expected_data_type) + ".")
                            print("        The actual type is: " + str(data.dtype) + ".")
                            print()

        # Something else that I don't understand is given
        else:

            if(silent_error == False):
                print()
                print("ERROR!: I don't understand the given data type.")
                print("        Type: " + str(type(data))  + ".")
                print("        I can't look inside the data.")
                print()

            

    # If no data is given, return an error
    else:

        if(silent_error == False):
            print()
            print("ERROR!: No data was given.")


    return return_value_index



# Solve a list of indexes
#
# Similar to solve_index(), but this time we have a list of indexes
# This method will return a list of indexes, or a list of errors
def solve_index_list(data, numerical_column_index_list, expected_data_type = None, silent_error = False, silent_warning = False):

    # Return variable
    #
    # Default to -1 meaning we don't have a valid index
    return_value_index_list = [-1] * len(numerical_column_index_list)
 
    # Check that we have a list of indexes
    if(type(numerical_column_index_list) != list):
        if(silent_error == False):
            print()
            print("ERROR!: The given indexes are not a valid list.")
            print("        I can't look inside the data.")
            print()

    # Check that we have at least one index
    if(len(numerical_column_index_list) == 0):
        if(silent_error == False):
            print()
            print("ERROR!: The given indexes list is empty.")
            print("        I can't look inside the data.")
            print()

    # Check that all indexes are valid
    #
    # But we need to keep into account the  expected_data_type variable
    # If it is a list, we need to check that the type is any of those inside the list
    # Some of the elements of this list can be None.
    #
    # If it is not a list, we don't need to check anything extra.

    # Check that  expected_data_type is a list, single type, or None
    #
    # (A) If the expected type is None, this is a valid option
    # (B) If the expected type is a single type, this is also a valid option, for each index we check that type
    # (C) If the expected type is a list of types, we need to check every index againts that  list of types
    # (D) If the expected type is a list of list of types, we need to check every index againts each specific list of types
    #
    # What we do in this piece of code is transform all cases into the last one
    final_expected_data_type = [[None]] * len(numerical_column_index_list) # (A) Solved
    if(expected_data_type != None):

        # Check if it is a list or a single element (C or D case)
        if(type(expected_data_type).__name__ != 'list'):

            # Check if the first element is a list of list (D case)
            if(type(expected_data_type[0]).__name__ == 'list'):

                # We need to make sure that the list is the same length as the indexes
                if(len(expected_data_type) != len(numerical_column_index_list)):
                    if(silent_error == False):
                        print()
                        print("ERROR!: The expected data type list is not the same length as the indexes list.")
                        print()
                    return return_value_index_list
                else:
                    final_expected_data_type = expected_data_type # (D) Solved

            else:
                # Make a list of list, all of them with the given list of types (C case)
                final_expected_data_type = [[expected_data_type]] * len(numerical_column_index_list)


        # If it isn't, we are in case (B)
        else:
            # Make a list of list, all of them with length 1 and the given type
            final_expected_data_type = [[expected_data_type]] * len(numerical_column_index_list) # (B) Solved

    # Now we can check all the indexes
    for i in range(len(numerical_column_index_list)):
        return_value_index_list[i] = solve_index(data, numerical_column_index_list[i], final_expected_data_type[i][0], silent_error, silent_warning)

    return return_value_index_list



# Solve the data source
#
# Sometimes the user wants to init an object using:
#
# - A Seagull object
# - A numpy array
# - A pandas dataframe
#
# This method solves the ambiguity by returning the right raw data
# which depend on the object type.
#
# This method only gives back univariate data.
# If you want to init multivariate data, use this method once per variable.
#
# The final return includes:
#
# - The object type:
#
#        None,     for no data
#       "Seagull", for Seagull object
#       "Numpy",   for np.array
#       "Pandas",  for pandas dataframe
#       "Uknown",  for anything else
#
# - The solved numerical column index
#
#     -1:
#
#         if no data was given
#         a np.array was given
#         an unknown type of data was given
#
#     0 <= index < total_columns:
#        
#         if a Seagull or pandas dataframe was given with a valid index or name
#
# - The data is of the requested type
#
#     False: If the data is not of the expected type
#     True:  If the data is at least one of the expected type

def solve_source_data(data, numerical_column_index, name_column_string, expected_data_type):

    # Default return
    return_list = [None, -1, False]

    # Keep track that the given index (name or number) is valid or not
    index_candidate = -1
    index_string_check = False
    index_string_valid = False

    # First, check that we have a valid index one way or another
    final_index = solve_index_and_column(numerical_column_index, name_column_string)
    if(final_index == -1):
        print()
        print("ERROR!: No valid index was given.")
        print("        I can't look inside the data.")
        print()
    
    # Check the type of data we have
    if(data != None):

        # If the data is a Seagull object
        if(type(data).__name__ == 'Seagull'):

            # If the index is valid, you can find the data
            # but first, we might need to convert a string to integer
            if(final_index != -1):

                # Check if the numerical is a string:
                # 
                #     A) The string is the column name.
                #         Look for the first index of such name.
                #         If it doesn't exist rise an error.
                #
                #     B) The user got confused, and use a string as index, such as "3"
                #         Look for the first index of such name.
                #         If it doesn't exist rise an error.
                #         If it does indeed exist, this is a logical error that will be confusing.
                #         but we will use it anyway.
                if(type(final_index) == str):

                    index_string_check = True
                    
                    index_candidate = data.get_column_index(final_index)
                    if(index_candidate < 0):

                        print()
                        print("ERROR!: The given column: " + str(final_index) + " is not valid.")
                        print("        I tried to find the name and couldn't find an index for that column.")
                        print()
                        print("        Current columns are:.")
                        print()
                        print("        " + str(data.get_columns_names()))
                        print()

                    else:
                        final_index        = index_candidate
                        index_string_valid = True
                        

                # Up to this point, we have finally an integer index
                #
                # If we did a string check, and is valid,   we will use it
                # If we did a string check, and is invalid, we will raised an error, we don't need to do anything else
                # If we didn't do a string check, we need to check that the index is valid                
                if(index_string_check != True or index_string_valid == True):

                    # Check if the index is valid
                    if(final_index >= 0 and final_index < data.get_total_columns()):

                        # If the data is a Seagull object, we can use it
                        return_list[0] = "Seagull"
                        return_list[1] = final_index

                        # Check if the data in the array is of the expected type
                        # If the expected type is a list, we need to check that the type is any of those inside the list
                        if(type(expected_data_type).__name__ == 'list'):
                            return_list[2] = data.get_column_types()[final_index] in expected_data_type
                        else:
                            return_list[2] = data.get_column_types()[final_index] == expected_data_type

                    else:
                        print()
                        print("ERROR!: The given index: " + str(final_index) + " is out of range.")
                        print("        The data set has " + str(data.get_total_columns() + " columns."))
                        print("        Remember the first column is index 0.")
                        print()


        # If the data is a pandas dataframe
        elif(type(data).__name__ == 'DataFrame'):

            # If the index is valid, you can find the data
            # but first, we might need to convert a string to integer
            if(final_index != -1):

                # Check if the numerical is a string:
                # 
                #     A) The string is the column name.
                #         Look for the first index of such name.
                #         If it doesn't exist rise an error.
                #
                #     B) The user got confused, and use a string as index, such as "3"
                #         Look for the first index of such name.
                #         If it doesn't exist rise an error.
                #         If it does indeed exist, this is a logical error that will be confusing.
                #         but we will use it anyway.
                if(type(final_index) == str):

                    index_string_check = True
                    
                    try:
                        # Attempt to get the index of the column
                        index_candidate = data.columns.get_loc(final_index)
                    except KeyError:
                        # If the column is not found, return -1
                        index_candidate =  -1

                    if(index_candidate < 0):

                        print()
                        print("ERROR!: The given column: " + str(final_index) + " is not valid.")
                        print("        I tried to find the name and couldn't find an index for that column.")
                        print()
                        print("        Current columns are:.")
                        print()
                        print("        " + str(data.columns.values()))
                        print()

                    else:
                        final_index        = index_candidate
                        index_string_valid = True
                        

                # Up to this point, we have finally an integer index
                #
                # If we did a string check, and is valid,   we will use it
                # If we did a string check, and is invalid, we will raised an error, we don't need to do anything else
                # If we didn't do a string check, we need to check that the index is valid                
                if(index_string_check != True or index_string_valid == True):

                    # Check if the index is valid
                    if(final_index >= 0 and final_index < data.shape[1] ):

                        # If the data is a Seagull object, we can use it
                        return_list[0] = "Pandas"
                        return_list[1] = final_index
                        
                        # Check if the data in the array is of the expected type
                        # If the expected type is a list, we need to check that the type is any of those inside the list
                        if(type(expected_data_type).__name__ == 'list'):
                            return_list[2] = data.dtypes[final_index] in expected_data_type
                        else:
                            return_list[2] = data.dtypes[final_index] == expected_data_type


                    else:
                        print()
                        print("ERROR!: The given index: " + str(final_index) + " is out of range.")
                        print("        The data set has " + str(data.get_total_columns() + " columns."))
                        print("        Remember the first column is index 0.")
                        print()


        # If the data is a numpy array
        elif(type(data).__name__ == 'ndarray'):

            # If the user gave you an index, this is irrelevant
            # numpy arrays don't have column names or indexes, is only one unique array
            print()
            print("WARNING!: The given data is a numpy array.")
            print("          The column index or name is irrelevant.")

            # Check if the data in the array is of the expected type
            return_list[0] = "Numpy"
            return_list[1] = -1
            
            # Check if the data in the array is of the expected type
            # If the expected type is a list, we need to check that the type is any of those inside the list
            if(type(expected_data_type).__name__ == 'list'):
                return_list[2] = data.dtype in expected_data_type
            else:
                return_list[2] = data.dtype == expected_data_type

        # Something else that I don't understand is given
        else:

            print()
            print("ERROR!: I don't understand the given data type.")
            print("        Type: " + str(type(data))  + ".")
            print("        I can't look inside the data.")
            print()

            return_list[0] = "Uknown"

    # If no data was given
    # This is fine, the user might want to init the object with random data
    else:

        print()
        print("ERROR!: No data was given.")


    return return_list