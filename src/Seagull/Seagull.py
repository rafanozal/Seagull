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
    from .methods.strings_representations import str_overview, str_square, str_complete, print_all_data, to_string, describe_types

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
        isFloat, isInt, isString, isBool, isBoolean,
        getCategories
    )

    #      Get information regarding categories
    from .methods.data_categorical import (
        is_strict_categorical, check_if_ordered, is_ordered_categorical,
        set_categories, setCategories,
        remove_extra_categories,
        remove_NA_category, swap_NA_category
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
        setColumnZeroes,
        round_column, round,
        normalize, normalize_column, normalize_columns,
        normalize_row, normalize_rows

    )


    # ---- Data casting
    from .methods.data_casting    import columnToInteger, columnToFloat, columnToCategory, columnToString

    # ---- Data randomization
    from .methods.data_randommize import zero, randomize, randomize_categorical

    # ---- Data normalization
    #      Normalize by either rows or columns

    # ---- Data filtering
    from .methods.data_filtering  import keepColumnTopValues, keepColumnByValue, countByValue

    # ---- Data summary
    from .methods.data_summary    import summarize_categorical_column

    # ---- Toy datasets
    #
    #      Iris dataset
    #      Spotify dataset
    from .methods.toy_datasets    import set_iris, load_iris, get_spotify_datasets

    # -------------------------------------------------
    # Constructor
    # -------------------------------------------------
    # region
    
    # An empty dataframe of given dimensions:
    # > myDF = Seagull(6,3)
    def __init__(self, total_rows:int = 3, total_columns:int = None, dtypes = None, suppress_warnings:bool = False):

        """
        Constructor for the Seagull object.
        
        Args:
            total_rows    (int, optional): The first parameter with a default
                                           value of 3

            total_columns (int, optional): The second parameter. Although the
                                           default behavior is to use the
                                           value 4, `None` is initially used as
                                           a sentinel to detect whether this
                                           parameter was explicitly provided by
                                           the user. If `b` is not provided, it
                                           defaults to 4.

            dtypes   (list str, optional): The third parameter with a default
                                           to None. By default all types are
                                           float64. Any list of string of any
                                           size can be provided. If the list is
                                           smaller than the number of columns,
                                           the last type will be used to fill
                                           the rest. If the list is larger, the
                                           extra types will be ignored. In both
                                           cases, a warning will be printed.

                                           If total_columns is not provided,
                                           then the total_columns will be set
                                           to the length of the dtypes list.
        
        Returns:
            A Seagull object.
        
        Raises:
            Nothing.
        """
        
        # Set default b to 4 if not provided
        was_columns_provided_explicitly = False
        if total_columns is None:
            if(dtypes == None):
                total_columns = 4
            else:
                total_columns = len(dtypes)
        else:
            was_columns_provided_explicitly = True
        
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
                    print("WARNING!: Fewer dtpyes than columns!")
                    print()
                    print("          I'm using the last one to fill the rest.")
                    print()

            # We are given more types than columns
            elif(len(dtypes) > total_columns):

                # If we did right to avoid declaring the total_columns
                # that is fine, so we do nothing extra.
                if(not(was_columns_provided_explicitly)):
                    my_final_dtypes = dtypes

                # Otherwise, we need to warn the user that we are taking
                # away the extra ones
                else:
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
        

    @classmethod
    def from_pandasDF(cls, pandas_df:pd.DataFrame):

        # Get the relevant info from the dataframe
        total_rows    = pandas_df.shape[0]
        total_columns = pandas_df.shape[1]
        types_list    = pandas_df.dtypes.to_list()

        # Init the seagull object, all will be zeros
        my_seagull = cls(total_rows, total_columns, types_list)

        # Assign the pandas to seagull data
        my_seagull.setData(pandas_df)

        return my_seagull


    @classmethod
    def from_pandasSeries(cls, pandas_sr:pd.Series):

        my_panda_df     = pandas_sr.to_frame()
        my_seagull_dF   = Seagull.from_pandasDF(my_panda_df)
    
        return my_seagull_dF

        
        

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
        return(self.str_complete())

    # Get a copy
    def copy(self):

        # Get a seagull of same size and data structure
        newSeagul = Seagull(self.totalRows, self.totalColumns, dtypes = self.getColumnTypes())

        # Get the same column names
        newSeagul.renameColumns(self.getColumnNames())

        # For each categorical data, set the same categories
        for i in range(self.totalColumns):
            if(self.is_strict_categorical(i)):
                newSeagul.setCategories(i, self.getCategories(i))

        # Copy the data
        for i in range(self.totalRows):
            for j in range(self.totalColumns):
                newSeagul[i,j] = self[i,j]

        return(newSeagul)


    # -------------------------------------------------------------------------
    # Operators []
    #     -__setitem__
    #     -__getitem__
    # -------------------------------------------------------------------------
    # This can't be done
    #
    #     my_df[,1]
    #
    # The interpreter complains that is invalid syntax even before running the code

    def __setitem__(self, key, value):

        # Init the indexes for row and column
        indexRow    = None
        indexColumn = None

        #print("KEY: ", key)
        #print("VALUE: ", value)
        #print("-----------------")

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
            # my_df[[True, False, True],2]
            elif( list_r_flag  and type(indexColumn) == int ):

                # If we have a list of booleans
                # my_df[[True, False, True],2]
                if(all(isinstance(item, bool) for item in indexRow)):
                    self.data.loc[  indexRow  , indexColumn ] = value
                # If we have a slice of data
                # my_df[1:4,2]
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

            # 7) We want to get a list of all values by both slices and lists
            # my_df[1:4,[True, False, True]]
            elif( type(indexRow) == slice and list_c_flag ):

                # Convert the slice into a np.array
                nr = self.getTotalRows()
                my_np_array = np.array([False] * nr)
                my_np_array[indexRow] = True

                self.data.loc[ my_np_array  , indexColumn ] = value

            # 8) We want to get a list of all values by both slices and lists
            # my_df[[True, False, True], 1:4]
            elif( list_r_flag and type(indexColumn) == slice):

                # Convert the slice into a np.array
                nc = self.getTotalColumns()
                my_np_array = np.array([False] * nc)
                my_np_array[indexColumn] = True

                self.data.loc[ indexRow , my_np_array ] = value

            # 9) We want to get a list of all values by both slices and lists
            # my_df[1:4,2:5]
            elif( type(indexRow) == slice and type(indexColumn) == slice):

                # Convert both slices into a np.array
                nr = self.getTotalRows()
                my_npr_array = np.array([False] * nr)
                my_npr_array[indexRow] = True

                nc = self.getTotalColumns()
                my_npc_array = np.array([False] * nc)
                my_npc_array[indexColumn] = True

                self.data.loc[ my_npr_array , my_npc_array ] = value


            else:

                print()
                print("ERROR: Can't understand these types at the same time")
                print(type(indexRow))
                print(type(indexColumn))
                print()
                
    def __getitem__(self, key):

        # This is the value we are going to return
        my_return = None

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
                my_return = self.data.iloc[ indexRow  , indexColumn ]
            
            # 2) We want to get a list of values
            # my_df[1:4,2:5]
            # my_df[[False False False  True  True False  True], [False False False  True  True False  True] ]
            elif( list_r_flag  and list_c_flag ):
                
                if( all(isinstance(item, bool) for item in indexColumn) and 
                    all(isinstance(item, bool) for item in indexRow)        ):
                    my_return = self.data.loc[  indexRow  , indexColumn ]
                # If we have a slice of data
                else:
                    my_return = self.data.iloc[ indexRow  , indexColumn ]

            # 3) We want to get a list of values for several column with constant row
            # my_df[1, 2:5 ]
            # my_df[1, [False False False  True  True False  True] ]
            elif( type(indexRow) == int and list_c_flag ):

                # If we have a list of booleans
                if(all(isinstance(item, bool) for item in indexColumn)):
                    my_return = self.data.loc[  indexRow  , indexColumn ]
                # If we have a slice of data
                else:
                    my_return = self.data.iloc[ indexRow  , indexColumn ]


            # 4) We want to get a list of values for a single column with several rows
            # my_df[1:4,2]
            # my_df[[True, False, True],2]
            elif( list_r_flag  and type(indexColumn) == int ):

                # If we have a list of booleans
                # my_df[[True, False, True],2]
                if(all(isinstance(item, bool) for item in indexRow)):
                    my_return = self.data.loc[  indexRow  , indexColumn ]
                # If we have a slice of data
                # my_df[1:4,2]
                else:
                    my_return = self.data.iloc[ indexRow  , indexColumn ]

            # 5) We want to get a list of all values for a single column
            # my_df[:,2]
            elif( type(indexRow) == slice and type(indexColumn) == int ):
                my_return = self.data.iloc[ indexRow  , indexColumn ]
            
            # 6) We want to get a list of all values for a single row
            # my_df[1,:]
            elif( type(indexRow) == int and type(indexColumn) == slice ):
                my_return = self.data.iloc[ indexRow  , indexColumn ]

            # 7) We want to get a list of all values by both slices and lists
            # my_df[1:4,[True, False, True]]
            elif( type(indexRow) == slice and list_c_flag ):

                # Convert the slice into a np.array
                nr = self.getTotalRows()
                my_np_array = np.array([False] * nr)
                my_np_array[indexRow] = True

                my_return = self.data.loc[ my_np_array  , indexColumn ]

            # 8) We want to get a list of all values by both slices and lists
            # my_df[[True, False, True], 1:4]
            elif( list_r_flag and type(indexColumn) == slice):

                # Convert the slice into a np.array
                nc = self.getTotalColumns()
                my_np_array = np.array([False] * nc)
                my_np_array[indexColumn] = True

                my_return = self.data.loc[ indexRow , my_np_array ]

            # 9) We want to get a list of all values by both slices and lists
            # my_df[1:4,2:5]
            elif( type(indexRow) == slice and type(indexColumn) == slice):

                # Convert both slices into a np.array
                nr = self.getTotalRows()
                my_npr_array = np.array([False] * nr)
                my_npr_array[indexRow] = True

                nc = self.getTotalColumns()
                my_npc_array = np.array([False] * nc)
                my_npc_array[indexColumn] = True

                my_return = self.data.loc[ my_npr_array , my_npc_array ]


            else:

                print()
                print("ERROR: Can't understand these types at the same time")
                print(type(indexRow))
                print(type(indexColumn))
                print()
                


        return my_return

    # endregion
