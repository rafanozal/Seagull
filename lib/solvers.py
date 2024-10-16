
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