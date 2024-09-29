# General libraries
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import random

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
    #
    # ---- String representations
    #      
    #      Showing the data in different ways at the console. Useful for debugging and quick overview.       

    from .methods.strings_representations import print_overview

    # ---- Setters and getters
    #
    #      Accessing and setting the attributes of the class.
    from .methods.setters_and_getters import  getData, getPanda, ncol, nrow, getTotalColumns, getTotalRows, setData, setTotalRows, setTotalColumns

    # ---- Data Reading
    #
    #      Get information regarding different aspects of the data; but never modify it.
    from .methods.data_read import getColumnNames, getColumnName, getColumn, c, getColumnTypes, isCategorical, getCategories, isNumerical, isFloat, isInt

    # ---- Data Loading
    #
    #     From a given list of files, get a bunch of Seagull objects in return
    from .methods.data_loading import loadFromCSV

    # ---- Data manipulation
    #
    #      Set the data to zeros
    #      Set the data to random values
    #      Randomize the data following the same distribution for each column
    #      Induce an error in each datacell of a 5% (default) in order to avoid indivual datapoints identifications
    #      Normalize by either rows or columns
    from .methods.data_manipulation import renameColumns, renameColumn, columnToInteger, columnToFloat, setColumnZeroes, setColumnZeroesF, normalize

    # ---- Data filtering
    from .methods.data_filtering import keepColumnTopValues, keepColumnByValue
    
    # ---- Toy datasets
    #
    #      Iris dataset
    from .methods.toy_datasets import set_iris, get_spotify_datasets

    # -------------------------------------------------
    # Constructor
    # -------------------------------------------------
    # region
    
    # An empty dataframe of given dimensions:
    # > myDF = Seagull(6,3)
    def __init__(self, totalRows = 3, totalColumns = 4):

        self.totalRows: int     = totalRows
        self.totalColumns: int  = totalColumns
        self.data: pd.DataFrame = pd.DataFrame(index=range(totalRows),columns=range(totalColumns))

    # endregion


    # -------------------------------------------------
    # Special methods:
    #     -__str__
    #     -__repr__
    #     -__len__
    #     -__iter__ (etc)
    # -------------------------------------------------
    # region

    # Get a copy
    def copy(self):

        newSeagul = Seagull(self.totalRows, self.totalColumns)

        for i in range(self.totalRows):
            for j in range(self.totalColumns):
                newSeagul[i,j] = self[i,j]

        newSeagul.renameColumns(self.getColumnNames())

        return(newSeagul)



    # Override [] operator
    #
    # > variable = myDF[1,2]
    # > list     = myDF[1,2:4]
    # > list     = myDF[1,[2,4,5]]
    # > list     = myDF[[1,2,3],[2,4,5]]
    # > list     = myDF[:,2]
    # > list     = myDF[1,:]
    def __getitem__(self, xy):
            
        # Get the indexes or the slices, or whatever
        indexRow , indexColumn = xy

        # We can have the following cases:

        #print(indexRow)
        #print(type(indexRow))

        # First we need to make sure we have the right type of integer
        if( type(indexRow) == np.int64 ):
            indexRow = int(indexRow)
        if( type(indexColumn) == np.int64 ):
            indexColumn = int(indexColumn)


        # 1) We want to get a single value
        if( type(indexRow) == int and type(indexColumn) == int ):
            return self.data.iloc[ indexRow , indexColumn ]
        # 2) We want to get a list of values
        elif( type(indexRow) == list and type(indexColumn) == list ):
            print("case 2")
            return self.data.iloc[ indexRow , indexColumn ].copy()
        # 3) We want to get a list of values for a single column
        elif( type(indexRow) == int and type(indexColumn) == list ):
            print("case 3")
            return self.data.iloc[ indexRow , indexColumn ].copy()
        # 4) We want to get a list of values for a single row
        elif( type(indexRow) == list and type(indexColumn) == int ):
            print("case 4")
            return self.getColumn(indexColumn).copy()
        # 5) We want to get a list of values for a single row
        elif( type(indexRow) == slice and type(indexColumn) == int ):
            print("case 5")
            return self.getColumn(indexColumn).copy()
        # 6) We want to get a list of values for a single row
        elif( type(indexRow) == int and type(indexColumn) == slice ):
            print("case 6")
            return self.data.iloc[ indexRow , indexColumn ].copy()

            

        else:
            print("case 99: you did something wrong")

        #return self.data.iloc[ indexRow , indexColumn ]

    # Override [] operator
    #
    # > myDF[1,2]             = value
    # > myDF[1,2:4]           = list
    # > myDF[1,[2,4,5]]       = list
    # > myDF[[1,2,3],[2,4,5]] = matrix
    # > myDF[,2]              = list
    def __setitem__(self, xy, value):

        # Get the indexes or the slices, or whatever
        indexRow , indexColumn = xy

        # First we need to make sure we have the right type of integer
        if( type(indexRow) == np.int64 ):
            indexRow = int(indexRow)
        if( type(indexColumn) == np.int64 ):
            indexColumn = int(indexColumn)

        # We can have the following cases:

        # 1) We want to set a single value
        if( type(indexRow) == int and type(indexColumn) == int ):
            self.data.iloc[ indexRow  , indexColumn ] = value
        # 2) We want to set an entire column
        elif( type(indexRow) == int and type(indexColumn) == slice ):
            self.data.iloc[ indexRow  , indexColumn ] = value
        # 3) We want to set an entire row
        elif( type(indexRow) == slice and type(indexColumn) == int ):
            self.data.iloc[ indexRow  , indexColumn ] = value
        # 4) We want to set a list of values
        elif( type(indexRow) == list and type(indexColumn) == list ):
            self.data.iloc[ indexRow  , indexColumn ] = value


    # endregion

    # Define the iadd operator
    #def __iadd__(self, other):
     #   if isinstance(other, int) or isinstance(other, float):
        
      #  return self


    # -------------------------------------------------
    # region Filling the data
    # -------------------------------------------------

    # Fill the DF with zeros
    def zero(self):

      for i in range(self.totalRows):
        for j in range(self.totalColumns):

          self[i,j] = 0

    # Fill the DF with random data
    def randomize(self):

      for i in range(self.totalRows):
        for j in range(self.totalColumns):

          self[i,j] = random.random()


    # endregion
    
    






