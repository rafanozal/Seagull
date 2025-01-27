# General libraries
import numpy as np

# Import the main libraries
from ..V2_Plot    import V2_Plot
from ....Seagull  import Seagull

# Import the auxiliary libraries
import lib.solvers       as my_solvers

# Constants
from src import constants

class V2_Num_Cat(V2_Plot):

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
                 data  = None, numerical_column_index = None, categorical_column_index = None, # Rearranged parameters for easy use
                 **kwargs):
        
        # -----------------------------------------
        # Do the parent constructor first
        # -----------------------------------------
        super().__init__(**kwargs)  # Pass common parameters to the parent constructor


        #print("V2 NUM CAT CONSTRUCTOR")
        #print()
        #print("Plot filename: ", self.filename)
        #print("Plot folder path: ", self.folder_path)
        #print()

        # -----------------------------------------
        # Update the parent class attributes second
        # -----------------------------------------

        self.type      = "V2 Numerical Categorical"

        if(self.manual_size == False): self.set_size( 10, 5, autoupdate = False)

        # -----------------------------------------
        # Set the current class attributes last
        # -----------------------------------------
        self.data_length            = 2                           # How many numerical data do you have (one per category)
        self.data_numerical_list    = [None] * self.data_length   # Data for each of the numerical data categories
        self.data_numerical_names   = [None] * self.data_length   # Name for each of the numerical data (for the legend)
        self.data_numerical_name    = "Numerical"                 # Name for the numerical data
        self.data_categorical_name  = "Categories"                # Name for the categorical data
        self.data_numerical_index   = -1                          # Index of the numerical data
        self.data_categorical_index = -1                          # Index of the categorical data        
        self.data_name              = "Random Data"               # Name of the data
        self.data_name_y            = ""                          # Name of the y axis (this need to be init later, density, value for boxplot, count, etc)

        # Init the random data as default
        for i in range(self.data_length):
            self.data_numerical_list[i]   = np.sort(np.random.rand(100))   # Initialize a random array
            self.data_numerical_list[i]   = (2 * self.data_numerical_list[i]) - 1  # Scale between -1 and 1
            self.data_numerical_names[i]  = "Data " + str(i)


        # Try to init the data to whatever was given
        if(data != None):
            
            if(numerical_column_index == None or categorical_column_index == None):
                print()
                print("ERROR!: I can't read the Numerical-Categorical")
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

                    final_numeric_index  = my_solvers.solve_index(data, numerical_column_index,   expected_data_type = constants.NUMERICAL_TYPES)
                    final_category_index = my_solvers.solve_index(data, categorical_column_index, expected_data_type = constants.SOFT_CATEGORIES)

                    # Errors in the indexes
                    if(final_numeric_index < 0 or final_category_index < 0):

                        #
                        #     No name found
                        #
                        if(final_numeric_index  == -3):
                            print()
                            print("ERROR!: The numerical column name was not found in the data.")
                            print("        The name you gave me was:  " + str(numerical_column_index))
                            print("        The names in the data are: " + str(data_columns_names))
                            print()
                        if(final_category_index == -3):
                            print()
                            print("ERROR!: The categorical column name was not found in the data.")
                            print("        The name you gave me was:  " + str(categorical_column_index))
                            print("        The names in the data are: " + str(data_columns_names))
                            print()                         
                        #
                        #     Index out of bounds
                        #
                        if(final_numeric_index  == -4):
                            print()
                            print("ERROR!: The numerical column index was out of bounds.")
                            print("        The index you gave me was:            " + str(numerical_column_index))
                            print("        The number of columns in the data is: " + str(len(data_columns_names)))
                            print()
                        if(final_category_index == -4):
                            print()
                            print("ERROR!: The categorical column index was out of bounds.")
                            print("        The index you gave me was:            " + str(categorical_column_index))
                            print("        The number of columns in the data is: " + str(len(data_columns_names)))
                            print()
                        #
                        #     Invalid type of data
                        #
                        if(final_numeric_index  == -5):
                            print()
                            print("ERROR!: The numerical column is not a valid numerical column.")
                            print("        The index you gave me was: " + str(numerical_column_index))
                            print()
                        if(final_category_index == -5):
                            print()
                            print("ERROR!: The categorical column is not a valid categorical column.")
                            print("        The index you gave me was: " + str(categorical_column_index))
                            print()

                    # Everything is fine, we can init the data
                    else:
                        
                        if(data_type == "Seagull"): self.init_from_seagull(data, final_numeric_index, final_category_index)
                        if(data_type == "Pandas"):  pass
                        

    # Init the data from a Seagull object
    #
    # Internal function, no error checking
    def init_from_seagull(self, seagull_instance:Seagull, numerical_column:int, categorical_column:int):
        
        to_return = -1

        # -----------------------------------------
        # Set the current class attributes last
        # -----------------------------------------
        
        self.data_categorical_name = "Categories"                # Name for the categorical data

        self.data_name_y           = ""                          # Name of the y axis (this need to be init later, density, value for boxplot, count, etc)

        # Init the random data as default
        for i in range(self.data_length):
            self.data_numerical_list[i]   = np.sort(np.random.rand(100))   # Initialize a random array
            self.data_numerical_list[i]   = (2 * self.data_numerical_list[i]) - 1  # Scale between -1 and 1
            self.data_numerical_names[i]  = "Data " + str(i)


        # Get the categories
        my_categories = seagull_instance.get_categories(categorical_column)

        # Filter the data for each category
        my_filter_dictionary = seagull_instance.filter_by_category(categorical_column, numerical_column)

        # Update the objects parameters
        self.data_length          = len(my_categories)
        self.data_numerical_list  = [None] * self.data_length
        self.data_numerical_names = [None] * self.data_length  

        for i in range(self.data_length):
            self.data_numerical_list[i]  = np.sort(my_filter_dictionary[my_categories[i]])
            self.data_numerical_names[i] = my_categories[i]


        self.data_numerical_index   = numerical_column
        self.data_categorical_index = categorical_column
        self.data_numerical_name    = seagull_instance.get_column_name(numerical_column)
        self.data_categorical_name  = seagull_instance.get_column_name(categorical_column)
        self.data_name              = seagull_instance.get_name()

        to_return = 0

        return to_return
             

    def init_from_panda():
        pass
