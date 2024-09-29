#!/usr/bin/env python3

'''

This file contain the initialization to famous toy datasets

We have:

    Iris: A dataset about flowers statistics and type

        This is a simple dataset with 150 rows and 5 columns, the columns are 4
        numerical values and 1 categorical value.

    Sportify: A dataset about songs and their characteristics

        Spotify dataset is from:
        https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023

        This is a bit more complex dataset with 954 rows and several columns.
        The columns are badly organized and do not respect the BCNF, as such
        we will need to do some cleaning before we can use it.

        The resulting tables are the following:

            - Artists:
            - Songs:
            - Composers: A song must be composer by 1 to N artists.

'''

# General libraries
import pandas as pd
import os

# Imports for the iris dataset
# TODO: Include this in the datasets
from sklearn.datasets import load_iris

# Import the constants to have access to the toy datasets
import constants



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
        self.columnToFloat(j)



# Initialize the spotify dataset
# This function will return three datasets:
@classmethod
def get_spotify_datasets(cls):

    # Load the data from the csv file
    completeData = pd.read_csv(constants.SPOTIFY_PATH, encoding='latin-1')
    completeData_totalRows    = len(completeData.index)
    completeData_totalColumns = len(completeData.columns)
    completeData_columnNames  = completeData.columns

    # Make an empty list of strings that will contain the artists
    # We will initialize the list to be of size 5000; this is enough
    # for the number of artists in the dataset
    artists = [''] * 5000

    # Put all the artits from completeData into the artits list
    # Each artist is separated by a comma, so we will split the strings
    currentIndex = 0
    for i in range(completeData_totalRows):

        # The second column is the artist names
        currentArtists = completeData.iloc[i,1].split(',')

        for j in range(len(currentArtists)):
            artists[currentIndex] = currentArtists[j]
            currentIndex += 1

    # Remove duplicates
    artists = list(dict.fromkeys(artists))



    # Initialize the objects where we will store the three datasets

    # --------------------
    # A) Artists dataset
    # --------------------

    # ---- Initialize the dataframe for our artists database
    artistsDF   = cls(len(artists),3)
    artistsDF.renameColumns(['ArtistID', 'ArtistName', 'ArtistTotalSongs'])
    # ---- Initialize the data
    for i in range(len(artists)):
        artistsDF[i,0] = i
        artistsDF[i,1] = artists[i]
        artistsDF[i,2] = 0

    # ----- Set the columns to be integers as suppose to be
    artistsDF.columnToInteger(0)
    artistsDF.columnToInteger(2)

    # --------------------
    # B) Songs dataset
    # --------------------
    songsDF      = cls(completeData_totalRows , completeData_totalColumns)

    # The first column is going to the be song ID, the rest of the columns is going to be the same as completeData, but without the artists
    for i in range(completeData_totalRows):
        songsDF[i,0] = i                         # ID
        songsDF[i,1] = completeData.iloc[i,0]    # Name

        for j in range(2,completeData_totalColumns): # Rest of the info
            songsDF[i,j] = completeData.iloc[i,j]

    # Prepare the list with the column names
    newColumnsNames = completeData_columnNames.to_list()
    del newColumnsNames[1] # Remove the artists column

    #newColumnsNames = completeData_columnNames.drop(1) # Remove the artists column
    newColumnsNames.insert(0, 'SongID')                # Add the song ID column
    songsDF.renameColumns(newColumnsNames)

    # Set the proper datatypes of the integers
    songsDF.columnToInteger(0)
    for i in range(2,completeData_totalColumns):
        songsDF.columnToInteger(i)   

    # --------------------
    # C) Composer dataset
    # --------------------

    # Create the dataset where everything goes
    composersDF = cls(completeData_totalRows , 2)
    composersDF.renameColumns(['SongID', 'ArtistID'])

    # For each song, get the song ID, check which artists are in it, get the ID of the artist, and put it in the composersDF
    for i in range(completeData_totalRows):
            
        # Get the song ID
        songID = songsDF[i,0]
    
        # Get the artists
        currentArtists = completeData.iloc[i,1].split(',')
    
        # For each artist, get the ID and put it in the composersDF
        for j in range(len(currentArtists)):
    
            # Get the artist name
            currentArtistName = currentArtists[j]
    
            # Get the artist ID
            k = 0
            while k < len(artists) and artists[k] != currentArtistName:
                k += 1
    
            # Put the data in the composersDF
            composersDF[i,0] = songID
            composersDF[i,1] = k

            # Update the total number of songs for the artist
            artistsDF[k,2] += 1
    
    # Set the proper datatypes of the integers
    composersDF.columnToInteger(0)
    composersDF.columnToInteger(1)


    return [artistsDF, songsDF, composersDF]