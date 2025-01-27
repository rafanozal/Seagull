# General libraries
import numpy as np

import random
import string

# Import the main libraries
from ..V2_Plot    import V2_Plot
from ....Seagull  import Seagull

# Import the auxiliary libraries
import lib.solvers       as my_solvers

# Constants
from src import constants

class V2_Cat_Cat(V2_Plot):

    def __init__(self, 
                 data  = None, categorical_column_A_index = None, categorical_column_B_index = None, # Rearranged parameters for easy use
                 **kwargs):
        
        # -----------------------------------------
        # Do the parent constructor first
        # -----------------------------------------
        super().__init__(**kwargs)  # Pass common parameters to the parent constructor


        #print("V2 CAT CAT CONSTRUCTOR")
        #print()
        #print("Plot filename: ", self.filename)
        #print("Plot folder path: ", self.folder_path)
        #print()

        # -----------------------------------------
        # Update the parent class attributes second
        # -----------------------------------------

        self.type      = "V2 Categorical Categorical"

        if(self.manual_size == False): self.set_size( 10, 5, autoupdate = False)

        # -----------------------------------------
        # Set the current class attributes last
        # -----------------------------------------
        self.data_A_length           = 2                            # How many categories (A and B)
        self.data_B_length           = 4                            # 
        self.data_A_categorical_name = "Categories A"               # Name for the categorical data
        self.data_B_categorical_name = "Categories B"               # 
        self.data_A_categories       = [None] * self.data_A_length  # Each of the categories
        self.data_B_categories       = [None] * self.data_B_length  #
        self.data_A_index            = -1                           # Index of the categorical data
        self.data_B_index            = -1                           # 
        self.data_A_to_B_dictionary  = {}                           # Dictionary to map A to B (ie A1: {B1,3}, {B2,7}, A2: {B1,0},{B2,3} ...)
        self.data_B_to_A_dictionary  = {}                           # Dictionary to map B to A

        self.data_name              = "Random Data"               # Name of the data
        self.data_name_y            = ""                          # Name of the y axis (this need to be init later, density, value for boxplot, count, etc)

        # Init the random data as default
        string_length = 5
        # -- Init the A categories
        for a in range(self.data_A_length):
            current_random            = ''.join(random.choices(string.ascii_lowercase, k = string_length))
            self.data_A_categories[a] = current_random
        # -- Init the B categories
        for b in range(self.data_B_length):
            current_random            = ''.join(random.choices(string.ascii_lowercase, k = string_length))
            self.data_B_categories[b] = current_random
        # -- Assign A/B categories to B/A categories 
        self.data_A_to_B_dictionary   = {}
        self.data_B_to_A_dictionary   = {}
        for a in range(self.data_A_length):
            current_A_category                              = self.data_A_categories[a]
            self.data_A_to_B_dictionary[current_A_category] = []
            for b in range(self.data_B_length):
                current_B_category = self.data_B_categories[b]
                random_integer     = random.randint(0, 10)
                current_tuple      = (current_B_category, random_integer)
                self.data_A_to_B_dictionary[current_A_category].append( current_tuple )
                
        for b in range(self.data_B_length):
            current_B_category                              = self.data_B_categories[b]
            self.data_B_to_A_dictionary[current_B_category] = []
            for a in range(self.data_A_length):
                current_A_category = self.data_A_categories[a]
                random_integer     = random.randint(0, 10)
                current_tuple      = (current_A_category, random_integer)
                self.data_B_to_A_dictionary[current_B_category].append( current_tuple )





        # Try to init the data to whatever was given
        if(data != None):
            
            if(categorical_column_A_index == None or categorical_column_B_index == None):
                print()
                print("ERROR!: I can't read the Categorical-Categorical")
                print()
                print("        You need to give me an index or name for both")
                print("        the numerical and categorical columns.")
                print()
            
            else:

                data_type = None

                if(type(data).__name__ == 'Seagull'):   data_type = "Seagull"
                if(type(data).__name__ == 'DataFrame'): data_type = "Pandas"

                if(data_type == None):
                    print()
                    print("ERROR!: I can't read the data you gave me.")
                    print()
                    print("        I only accept Seagull objects and pandas dataframes.")
                    print()
                    print("        You gave me a: " + str(type(data).__name__))
                    print()

                else:

                    data_columns_names = None
                    if(data_type == "Seagull"):   data_columns_names = data.get_columns_names()
                    if(data_type == "Pandas"):    data_columns_names = data.columns

                    final_categorical_A_index = my_solvers.solve_index(data, categorical_column_A_index, expected_data_type = constants.SOFT_CATEGORIES)
                    final_categorical_B_index = my_solvers.solve_index(data, categorical_column_B_index, expected_data_type = constants.SOFT_CATEGORIES)

                    # Errors in the indexes
                    if(final_categorical_A_index < 0 or final_categorical_B_index < 0):

                        #
                        #     No name found
                        #
                        if(final_categorical_A_index  == -3):
                            print()
                            print("ERROR!: The first categorical column name was not found in the data.")
                            print("        The name you gave me was:  " + str(final_categorical_A_index))
                            print("        The names in the data are: " + str(data_columns_names))
                            print()
                        if(final_categorical_B_index == -3):
                            print()
                            print("ERROR!: The second categorical column name was not found in the data.")
                            print("        The name you gave me was:  " + str(final_categorical_B_index))
                            print("        The names in the data are: " + str(data_columns_names))
                            print()                         
                        #
                        #     Index out of bounds
                        #
                        if(final_categorical_A_index  == -4):
                            print()
                            print("ERROR!: The first categorical column index was out of bounds.")
                            print("        The index you gave me was:            " + str(final_categorical_A_index))
                            print("        The number of columns in the data is: " + str(len(data_columns_names)))
                            print()
                        if(final_categorical_B_index == -4):
                            print()
                            print("ERROR!: The second categorical column index was out of bounds.")
                            print("        The index you gave me was:            " + str(final_categorical_B_index))
                            print("        The number of columns in the data is: " + str(len(data_columns_names)))
                            print()
                        #
                        #     Invalid type of data
                        #
                        if(final_categorical_A_index == -5):
                            print()
                            print("ERROR!: The first categorical column is not a valid numerical column.")
                            print("        The index you gave me was: " + str(final_categorical_A_index))
                            print()
                        if(final_categorical_B_index == -5):
                            print()
                            print("ERROR!: The second categorical column is not a valid categorical column.")
                            print("        The index you gave me was: " + str(final_categorical_B_index))
                            print()

                    # Everything is fine, we can init the data
                    else:
                        
                        if(data_type == "Seagull"): self.init_from_seagull(data, final_categorical_A_index, final_categorical_B_index)
                        if(data_type == "Pandas"):  pass
                        

    # Init the data from a Seagull object
    #
    # Internal function, no error checking
    def init_from_seagull(self, seagull_instance:Seagull, categorical_A_column:int, categorical_B_column:int):
        
        to_return = -1

        # Init the random data as default
        self.data_name               = "Random Data"               
        self.data_A_length           = 2                            
        self.data_B_length           = 4                             
        self.data_A_categorical_name = "Categories A"               
        self.data_B_categorical_name = "Categories B"                
        self.data_A_categories       = [None] * self.data_A_length  
        self.data_B_categories       = [None] * self.data_B_length  
        self.data_A_index            = -1                           
        self.data_B_index            = -1                            
        self.data_A_to_B_dictionary  = {}                           
        self.data_B_to_A_dictionary  = {}                           
        
        self.data_name_y             = ""                        # Name of the y axis (this need to be init later, density, value for boxplot, count, etc)  

        # Init the random data as default
        string_length = 5
        # -- Init the A categories
        for a in range(self.data_A_length):
            current_random            = ''.join(random.choices(string.ascii_lowercase, k = string_length))
            self.data_A_categories[a] = current_random
        # -- Init the B categories
        for b in range(self.data_B_length):
            current_random            = ''.join(random.choices(string.ascii_lowercase, k = string_length))
            self.data_B_categories[b] = current_random
        # -- Assign A/B categories to B/A categories 
        self.data_A_to_B_dictionary   = {}
        self.data_B_to_A_dictionary   = {}
        for a in range(self.data_A_length):
            current_A_category                              = self.data_A_categories[a]
            self.data_A_to_B_dictionary[current_A_category] = []
            for b in range(self.data_B_length):
                current_B_category = self.data_B_categories[b]
                random_integer     = random.randint(0, 10)
                current_tuple      = (current_B_category, random_integer)
                self.data_A_to_B_dictionary[current_A_category].append( current_tuple )
                
        for b in range(self.data_B_length):
            current_B_category                              = self.data_B_categories[b]
            self.data_B_to_A_dictionary[current_B_category] = []
            for a in range(self.data_A_length):
                current_A_category = self.data_A_categories[a]
                random_integer     = random.randint(0, 10)
                current_tuple      = (current_A_category, random_integer)
                self.data_B_to_A_dictionary[current_B_category].append( current_tuple )


        # -----------------------------------------

        # Get the categories
        my_categories_A = seagull_instance.get_categories(categorical_A_column)
        my_categories_B = seagull_instance.get_categories(categorical_B_column)

        # Filter the data for each category
        my_filter_dictionary_A = seagull_instance.filter_bicategorical(self, categorical_A_column, categorical_B_column)
        my_filter_dictionary_B = seagull_instance.filter_bicategorical(self, categorical_B_column, categorical_A_column)

        # Update the objects parameters
        self.data_A_length           = len(my_categories_A)
        self.data_B_length           = len(my_categories_B)                    
        self.data_A_categorical_name = seagull_instance.get_column_name(categorical_A_column)
        self.data_B_categorical_name = seagull_instance.get_column_name(categorical_B_column)
        self.data_A_categories       = my_categories_A
        self.data_B_categories       = my_categories_B
        self.data_A_index            = categorical_A_column
        self.data_B_index            = categorical_B_column
        self.data_A_to_B_dictionary  = my_filter_dictionary_A
        self.data_B_to_A_dictionary  = my_filter_dictionary_B
        self.data_name               = seagull_instance.get_name()

        to_return = 0

        return to_return
             

    def init_from_panda():
        pass
