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
    from .methods.setters_and_getters import getPanda, ncol, nrow

    # ---- Data Reading
    #
    #      Get information regarding different aspects of the data; but never modify it.
    from .methods.data_read import getColumnNames, getColumnName, getColumn, c

    # ---- Data manipulation
    #
    #      Set the data to zeros
    #      Set the data to random values
    #      Randomize the data following the same distribution for each column
    #      Induce an error in each datacell of a 5% (default) in order to avoid indivual datapoints identifications
    from .methods.data_manipulation import renameColumns, renameColumn, toInteger, toFloat
    
    # ---- Toy datasets
    #
    #      Iris dataset
    from .methods.toy_datasets import set_iris

    # -------------------------------------------------
    # Constructor
    # -------------------------------------------------
    # region
    
    # An empty dataframe of given dimensions:
    # > myDF = Seagull(6,3)
    def __init__(self, totalRows, totalColumns):

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

        newSeagul.renameColumns(self.getNames())

        return(newSeagul)



    # Override [] operator
    def __getitem__(self, xy):
            
        indexRow , indexColumn = xy

        return self.data.iloc[ indexRow , indexColumn ]

    def __setitem__(self, xy, value):

        indexRow , indexColumn = xy

        self.data.iloc[ indexRow  , indexColumn ] = value


    # endregion

    
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
    
    






