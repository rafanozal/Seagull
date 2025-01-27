# General libraries
import numpy as np
from   random import randint


# Import the main libraries
from ..V1_Plot    import V1_Plot
from ....Seagull  import Seagull

# Import the auxiliary libraries
import lib.solvers       as my_solvers

# Constants
from src import constants

class V1_Categorical(V1_Plot):

    # Default constructor
    #
    # data = The source of the data
    #
    #        Can be a Seagull object, a pandas dataframe, a list of lists, a list of dictionaries, etc.
    #
    # numerical_column_index   = Index with the column that has the numbers
    #
    # categorical_column_index = Index with the column that has the categories,
    def __init__(self, 
                 data  = None, categorical_column_index = None, # Rearranged parameters for easy use
                 **kwargs):
        
        # -----------------------------------------
        # Do the parent constructor first
        # -----------------------------------------
        super().__init__(**kwargs)  # Pass common parameters to the parent constructor


        print("V1 CAT CONSTRUCTOR")
        print()
        print("Plot filename: ", self.filename)
        print("Plot folder path: ", self.folder_path)
        print()

        # -----------------------------------------
        # Update the parent class attributes second
        # -----------------------------------------

        self.type      = "V1 Categorical"

        if(self.manual_size == False): self.set_size( 10, 5, autoupdate = False)

        # -----------------------------------------
        # Set the current class attributes last
        # -----------------------------------------
        self.data_length            = 5                           # How many numerical data do you have (one per category)
        self.data_relative_list     = [0.0] * self.data_length   # Data with relative count for each of the numerical data categories
        self.data_count_list        = [0]   * self.data_length   # Data with absolute count for each of the numerical data categories
        self.data_numerical_names   = [None] * self.data_length   # Name for each of the numerical data (for the legend)
        #self.data_numerical_name    = "Numerical"                # Name for the numerical data         
        self.data_categorical_name  = "Categories"                # Name for the categorical data       (for the X-axis)
        #self.data_numerical_index   = -1                         # Index of the numerical data
        self.data_categorical_index = -1                          # Index of the categorical data        
        self.data_name              = "Random Data"               # Name of the data
        self.data_name_y            = "Count"                     # Name of the y axis (this need to be init later, density, value for boxplot, count, etc)

        # Init the random data as default
        self.data_length                  = 5                           
        self.data_count_list              = [randint(-10, 10) for i in range(0, 5)] # Default are 5 numbers between -10 and 10
        total_absolute                    = 0
        for i in range(self.data_length):
            self.data_numerical_names[i]  = "Data " + str(i)
            total_absolute               += abs(self.data_count_list[i])
        for i in range(self.data_length):
            self.data_relative_list[i]    = self.data_count_list[i] / total_absolute

        # Try to init the data to whatever was given
        if(data != None):
            
            if(categorical_column_index == None):
                print()
                print("ERROR!: I can't read the Categorical data")
                print()
                print("        You need to give me an index or name ")
                print("        for the categorical columns.")
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

                    final_category_index = my_solvers.solve_index(data, categorical_column_index, expected_data_type = constants.SOFT_CATEGORIES)

                    # Errors in the indexes
                    if(final_category_index < 0):

                        #
                        #     No name found
                        #
                        if(final_category_index == -3):
                            print()
                            print("ERROR!: The categorical column name was not found in the data.")
                            print("        The name you gave me was:  " + str(categorical_column_index))
                            print("        The names in the data are: " + str(data_columns_names))
                            print()                         
                        #
                        #     Index out of bounds
                        #
                        if(final_category_index == -4):
                            print()
                            print("ERROR!: The categorical column index was out of bounds.")
                            print("        The index you gave me was:            " + str(categorical_column_index))
                            print("        The number of columns in the data is: " + str(len(data_columns_names)))
                            print()
                        #
                        #     Invalid type of data
                        #
                        if(final_category_index == -5):
                            print()
                            print("ERROR!: The categorical column is not a valid categorical column.")
                            print("        The index you gave me was: " + str(categorical_column_index))
                            print()

                    # Everything is fine, we can init the data
                    else:
                        
                        if(data_type == "Seagull"): self.init_from_seagull(data, final_category_index)
                        if(data_type == "Pandas"):  pass
                        

    # Init the data from a Seagull object
    #
    # Internal function, no error checking
    def init_from_seagull(self, seagull_instance:Seagull, categorical_column:int):
        
        to_return = -1

        # -----------------------------------------
        # Set the current class attributes last
        # -----------------------------------------
        
        self.data_name_y           = ""                          # Name of the y axis (this need to be init later, density, value for boxplot, count, etc)

        # Init the random data as default
        self.data_length                  = 5                           
        self.data_count_list              = [randint(-10, 10) for i in range(0, 5)] # Default are 5 numbers between -10 and 10
        total_absolute                    = 0
        for i in range(self.data_length):
            self.data_numerical_names[i]  = "Data " + str(i)
            total_absolute               += abs(self.data_count_list[i])
        for i in range(self.data_length):
            self.data_relative_list[i]    = self.data_count_list[i] / total_absolute



        # Get the categories
        my_categories = seagull_instance.get_categories(categorical_column)

        # Count the number of categories of each category
        my_summary = seagull_instance.summarize_categorical_column(categorical_column, sort = "original", top = 0)        

        # Update the objects parameters
        self.data_length           = len(my_categories)
        self.data_count_list       = my_summary[1].to_list()
        self.data_relative_list    = my_summary[3].to_list()
        self.data_numerical_names  = my_summary[0].to_list()

        self.data_categorical_index = categorical_column
        self.data_categorical_name  = seagull_instance.get_column_name(categorical_column)
        self.data_name              = seagull_instance.get_name()

        to_return = 0

        return to_return
             

    def init_from_panda():
        pass
