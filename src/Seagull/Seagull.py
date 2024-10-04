# General libraries
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

# Main class declaration
class Seagull:

    """
    A class used to represent a Seagull object

    This override the Panda Dataframe functionality with syntax that is  much
    more convinient and concise.


    Attributes
    ----------
        totalRows : int
            How many rows does this data has

        totalColumns : int
            How many columns does this data has

        data : Panda Dataframe
            (Pointer) to a panda dataframe

        types : <array> string
            An array of strings telling which type of variable we have in each column

            Types can be one of the following:

            - Categorical
                - Order

            - Numerical

        totalNA : <array> int
            For each columns, how many values are missing.


    Public methods
    -------
        says(sound=None)
            Prints the animals name and what sound it makes
  
    Private methods
    -------
        countNA(int index)
            For a column given by an index, count how many NAs there are in that column
            and update the Seagull object accordingly.

        updateNA()
            For all columns, run countNA.

    """


    # Imported methods
    
    # ---- Panda series, for the constructor and casting
    from .methods.panda_series import create_series, generate_random_date

    # ---- String representations
    from .methods.strings_representations import str_overview, str_complete, print_all_data

    # ---- Setters and getters
    from .methods.setters_and_getters import (
        getData, getPanda, 
        ncol, nrow, 
        getTotalColumns, getTotalRows, 
        setTotalRows, setTotalColumns,
        setData
    )

    # ---- Data Reading
    #
    #      Get information regarding different aspects of the data; but never modify it.
    from .methods.data_read import (
        getColumnNames, getColumnName, getColumnIndex,
        getColumn, c, 
        getRowsNames, getRowName, getRowIndex,
        getRow, r,
        getColumnTypes,
        isCategorical, isCharacter, isNumerical,
        isFloat, isInt,
        getCategories
    )

    # ---- Data Loading
    #      From a given list of files, get a bunch of Seagull objects in return
    from .methods.data_loading import loadFromCSV

    # ---- Data manipulation
    from .methods.data_manipulation import (
        rename_columns, renameColumns, setColumnsNames,
        rename_column, renameColumn, setColumnName,
        rename_rows, renameRows, setRowsNames,
        rename_row, renameRow, setRowName,
        setColumnZeroes, setColumnZeroesF,
        normalize, round_column, round
    )


    # ---- Data casting
    from .methods.data_casting import columnToInteger, columnToFloat, columnToCategory, columnToString

    # ---- Data randomization
    from .methods.data_randommize import zero, randomize, randomize_categorical

    # ---- Data normalization
    #      Normalize by either rows or columns

    # ---- Data filtering
    from .methods.data_filtering import keepColumnTopValues, keepColumnByValue, countByValue

    # ---- Data summary
    from .methods.data_summary import summarize_categorical_column

    # ---- Toy datasets
    #
    #      Iris dataset
    #      Spotify dataset
    from .methods.toy_datasets import set_iris, get_spotify_datasets

    # -------------------------------------------------
    # Constructor
    # -------------------------------------------------
    # region
    
    # An empty dataframe of given dimensions:
    # > myDF = Seagull(6,3)
    def __init__(self, total_rows = 3, total_columns = 4, dtypes = None, suppress_warnings = False):

        # Check that the types makes sense with dimensions
        my_final_dtypes = None
        if(dtypes == None):
             my_final_dtypes = ['float'] * total_columns
        else:

            # We are given less types than columns
            if(len(dtypes) < total_columns):

                total_length    = len(dtypes)
                last_one        = dtypes[total_length - 1]
                my_final_dtypes = dtypes + [last_one] * (total_columns - total_length)

                if(not(suppress_warnings)):
                    print("WARNING!: Less dtpyes than columns!")
                    print()
                    print("          I'm using the last one to fill the rest.")
                    print()

            # We are given more types than columns
            elif(len(dtypes) > total_columns):

                my_final_dtypes = dtypes[:total_columns]

                if(not(suppress_warnings)):
                    print("WARNING: More dtpyes than columns!")
                    print()
                    print("         I'm ignoring the extra ones.")
                    print()

            else:
                my_final_dtypes = dtypes

        # Create the series that you need according to the number of dimensions
        # Array of series
        my_series = [None] * total_columns
        for i in range(total_columns):
            my_series[i] = Seagull.create_series(total_rows, my_final_dtypes[i])

        # Create the dataframe from those series
        #
        # IDEALLY, THIS WOULD BE EASY SUCH AS:
        #
        # self.data: pd.DataFrame = pd.DataFrame(my_series).T  # Transpose to make each series a column
        #
        # BUT THE STUPID PANDAS DOESN'T LIKE MIXING DTYPES SO THIS GOES INTO A DICTIONARY FORM THAT WORKS
        #
        # Create a dictionary from the list of Series
        series_dict = {str(i): series for i, series in enumerate(my_series)}

        # Create DataFrame from the dictionary
        self.data: pd.DataFrame  =  pd.DataFrame(series_dict)

        # Init the rest of the internal variables
        self.totalRows: int      = total_rows
        self.totalColumns: int   = total_columns
        #self.data: pd.DataFrame  = pd.DataFrame(index = range(totalRows) , columns = range(totalColumns), dtype = default_type)
        

        # Set the columns names from '0' to 'N' as default
        # self.renameColumns([str(i) for i in range(total_columns)])


    # endregion


    # -------------------------------------------------
    # Special methods:
    #     -__str__
    #     -__repr__
    #     -__len__
    #     -__iter__ (etc)
    # -------------------------------------------------
    # region

    def __str__(self) -> str:
        return(self.str_overview())

    # Get a copy
    def copy(self):

        newSeagul = Seagull(self.totalRows, self.totalColumns)

        for i in range(self.totalRows):
            for j in range(self.totalColumns):
                newSeagul[i,j] = self[i,j]

        newSeagul.renameColumns(self.getColumnNames())

        return(newSeagul)


    # -------------------------------------------------------------------------
    # Operators README
    # -------------------------------------------------------------------------
    # This can't be done
    #
    #     my_df[,1]
    #
    # The interpreter complains that is invalid syntax even before running the code

    # Override [] operator
    #
    # > variable = myDF[1,2]
    # > list     = myDF[1,2:4]
    # > list     = myDF[1,[2,4,5]]
    # > list     = myDF[[1,2,3],[2,4,5]]
    # > list     = myDF[:,2]
    # > list     = myDF[1,:]
    def __getitem__(self, key):

        # Init the indexes for row and column
        indexRow    = None
        indexColumn = None

        print("---")
        print(key)
        print(type(key))

        # Check if the key is a string
        # my_df["my_column_name"]
        if isinstance(key, str):

            # Setup the row to the complete slide, and the column to whatever index
            indexRow    = slice(None)
            indexColumn = self.getColumnIndex(key)

        # Check if the key is a tuple and if one of the elements is a string
        # my_df[ 1 , "my_column_name"]
        # my_df[1:4, "my_column_name"]
        # my_df[1: , "my_column_name"]
        # my_df[ :4, "my_column_name"]
        # my_df[ : , "my_column_name"]
        elif isinstance(key, tuple):
            row_key, col_key = key

            # String + String
            # Slide  + String
            if isinstance(col_key, str):

                # String + String
                if isinstance(row_key, str):
                    # Find by row name (weird, but ok)
                    print ("ERROR!: I don't understand ["+str(key)+"].")
                # Slide  + String
                elif isinstance(col_key, str):

                    # Wether is a single number or a slide, we keep the row_key as it is
                    indexRow    = row_key
                    indexColumn = self.getColumnIndex(col_key)

                    print(indexColumn)

            # Slide  + Slide
            # String + Slide
            else:

                # String + Slide
                if isinstance(row_key, str):
                    # Find by row name (weird, but ok)
                    print ("ERROR!: I don't understand ["+str(key)+"].")

                # Slide  + Slide
                else:
                    # Here we have either numbers or slides
                    # Get the indexes or the slices, or whatever
                    indexRow , indexColumn = key

        # If we arrived here, we already have indexes in the index variable
        # But check just in case
        if(indexRow == None or indexColumn == None):
            print ("ERROR!: I don't understand ["+str(key)+"].")
        else:

            # First we need to make sure we have the right type of integer
            if( type(indexRow)    == np.int64 ):
                indexRow    = int(indexRow)
            if( type(indexColumn) == np.int64 ):
                indexColumn = int(indexColumn)


            # 1) We want to get a single value
            # my_df[1,2]
            if( type(indexRow) == int and type(indexColumn) == int ):
                return self.data.iloc[ indexRow , indexColumn ]
            
            # 2) We want to get a list of values
            # my_df[1:4,2:5]
            elif( type(indexRow) == list and type(indexColumn) == list ):
                print("case 2")
                return self.data.iloc[ indexRow , indexColumn ].copy().to_numpy()
            
            # 3) We want to get a list of values for several column with constant row
            # my_df[1,2:5]
            elif( type(indexRow) == int and type(indexColumn) == list ):
                print("case 3")
                return self.data.iloc[ indexRow , indexColumn ].copy().to_numpy()
            
            # 4) We want to get a list of values for a single column with several rows
            # my_df[1:4,2]
            elif( type(indexRow) == list and type(indexColumn) == int ):
                print("case 4")
                return self.getColumn(indexColumn).copy().to_numpy()
            
            # 5) We want to get a list of all values for a single column
            # my_df[:,2]
            elif( type(indexRow) == slice and type(indexColumn) == int ):
                return self.getColumn(indexColumn).copy().to_numpy()
            
            # 6) We want to get a list of all values for a single row
            # my_df[1,:]
            elif( type(indexRow) == int and type(indexColumn) == slice ):
                print("case 6")
                return self.getRow(indexRow).copy().to_numpy()

                #return self.data.iloc[ indexRow , indexColumn ].copy().to_numpy()

                

            else:
                print("case 99: you did something wrong")





    def __setitem__(self, key, value):

        # Init the indexes for row and column
        indexRow    = None
        indexColumn = None

        # Check if the key is a string
        # my_df["my_column_name"]
        if isinstance(key, str):

            # Setup the row to the complete slide, and the column to whatever index
            indexRow    = slice(None)
            indexColumn = self.getColumnIndex(key)

        # Check if the key is a tuple and if one of the elements is a string
        # my_df[ 1 , "my_column_name"]
        # my_df[1:4, "my_column_name"]
        # my_df[1: , "my_column_name"]
        # my_df[ :4, "my_column_name"]
        # my_df[ : , "my_column_name"]
        elif isinstance(key, tuple):

            row_key, col_key = key

            # String + String
            # Slide  + String
            # Slide  + List
            # Slide  + List
            if isinstance(col_key, str):

                # String + String
                if (isinstance(row_key, str)):

                    # Find by row name (weird, but ok)
                    indexRow    = self.getRowIndex(row_key)
                    indexColumn = self.getColumnIndex(col_key)

                    
                # Slide  + String
                elif(isinstance(col_key, str)):

                    # Wether is a single number or a slide, we keep the row_key as it is
                    indexRow    = row_key
                    indexColumn = self.getColumnIndex(col_key)

                    # indexColumn might be a [False False False  True  True False  True] type of list,
                    # that is fine and will be corrected later

                # ?
                else:
                    print ("ERROR!: I don't understand ["+str(key)+"].")

            # Slide  + Slide
            # String + Slide
            else:

                # String + Slide
                if isinstance(row_key, str):
                    # Find by row name (weird, but ok)

                    indexRow    = self.getRowIndex(row_key)
                    indexColumn = col_key

                # Slide  + Slide
                else:
                    # Here we have either numbers or slides
                    # Get the indexes or the slices, or whatever
                    indexRow , indexColumn = key



        # If we arrived here, we already have valid indexes in the index variable
        # But check just in case
        # We also need to adjust list to np.arrays

        list_r_flag  = (type(indexRow)    == np.ndarray) or (type(indexRow)    == list)
        list_c_flag  = (type(indexColumn) == np.ndarray) or (type(indexColumn) == list)
        valid_r_flag = False
        valid_c_flag = False

        if(list_r_flag):
            valid_r_flag = True
            if(type(indexRow)    == list): indexRow    = np.array(indexRow) # Convert lists into np.arrays
        else:
            if(indexRow != None): valid_r_flag = True

        if(list_c_flag):
            valid_c_flag = True
            if(type(indexColumn) == list): indexColumn = np.array(indexColumn) # Convert lists into np.arrays
              
        else:
            if(indexColumn != None): valid_c_flag = True

        if(not(valid_r_flag and valid_c_flag)):
            print ("ERROR!: I don't understand ["+str(key)+"].")

        else:

            # First we need to make sure we have the right type of integer
            if( type(indexRow)    == np.int64 ):
                indexRow    = int(indexRow)
            if( type(indexColumn) == np.int64 ):
                indexColumn = int(indexColumn)


            # 1) We want to get a single value
            # my_df[1,2]
            if( type(indexRow) == int and type(indexColumn) == int ):
                self.data.iloc[ indexRow  , indexColumn ] = value
            
            # 2) We want to get a list of values
            # my_df[1:4,2:5]
            # my_df[[False False False  True  True False  True], [False False False  True  True False  True] ]
            elif( list_r_flag  and list_c_flag ):
                
                if( all(isinstance(item, bool) for item in indexColumn) and 
                    all(isinstance(item, bool) for item in indexRow)        ):
                    self.data.loc[  indexRow  , indexColumn ] = value
                # If we have a slice of data
                else:
                    self.data.iloc[ indexRow  , indexColumn ] = value

            # 3) We want to get a list of values for several column with constant row
            # my_df[1, 2:5 ]
            # my_df[1, [False False False  True  True False  True] ]
            elif( type(indexRow) == int and list_c_flag ):

                # If we have a list of booleans
                if(all(isinstance(item, bool) for item in indexColumn)):
                    self.data.loc[  indexRow  , indexColumn ] = value
                # If we have a slice of data
                else:
                    self.data.iloc[ indexRow  , indexColumn ] = value


            # 4) We want to get a list of values for a single column with several rows
            # my_df[1:4,2]
            elif( list_r_flag  and type(indexColumn) == int ):

                # If we have a list of booleans
                if(all(isinstance(item, bool) for item in indexRow)):
                    self.data.loc[  indexRow  , indexColumn ] = value
                # If we have a slice of data
                else:
                    self.data.iloc[ indexRow  , indexColumn ] = value

            # 5) We want to get a list of all values for a single column
            # my_df[:,2]
            elif( type(indexRow) == slice and type(indexColumn) == int ):
                self.data.iloc[ indexRow  , indexColumn ] = value
            
            # 6) We want to get a list of all values for a single row
            # my_df[1,:]
            elif( type(indexRow) == int and type(indexColumn) == slice ):
                self.data.iloc[ indexRow  , indexColumn ] = value


            else:

                print()
                print("ERROR: Can't understand these types at the same time")
                print(type(indexRow))
                print(type(indexColumn))
                print()
                

    # endregion





    # Define the iadd operator
    #def __iadd__(self, other):
     #   if isinstance(other, int) or isinstance(other, float):
        
      #  return self

    # endregion
    
    






