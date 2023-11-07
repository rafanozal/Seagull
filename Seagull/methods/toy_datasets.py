#!/usr/bin/env python3

'''

This file contain the initialization to famous toy datasets

'''

# General libraries
import pandas as pd

# Import a toy dataset for testing
from sklearn.datasets import load_iris


# Python is inferior to C++, as such it doesn't allow for basic functionality such as several constructor
# This is "solved" (lol) by using this workaround.

def set_iris(self):

    '''
        Reset the dataframe to the IRIS one
    '''

    # Load the data from sklearn
    sampleData = load_iris()

    # This is a complete clusterfuck of syntax, but to get the species you need to use this special comman 0_o
    species_data = sampleData.target_names[sampleData.target] # we will save this for later

    # Get the dimensions and an empty dataframe
    self.totalRows    = len(sampleData.data)
    self.totalColumns = len(sampleData.data[0]) + 1
    self.data         = pd.DataFrame(index=range(self.totalRows),columns=range(self.totalColumns))

    # Init the numerical data
    for i in range(self.totalRows):
        for j in range(self.totalColumns-1):
            self[i,j] = sampleData.data[i][j]
            #self[i,j] = pd.to_numeric(sampleData.data[i][j], errors='coerce').astype('float64')

    # Set the columns names
    irisNames = ['Sepal.Length', 'Sepal.Width', 'Petal.Length', 'Petal.Width', 'Species']
    self.renameColumns(irisNames)

    # Set the categories
    for i in range(self.totalRows):
        self[i,self.totalColumns-1] = species_data[i]

    # Set the columns type correctly
    for j in range(self.totalColumns-1):
        self.toFloat(j)

