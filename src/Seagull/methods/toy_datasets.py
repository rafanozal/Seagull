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

# Imports for the iris dataset
import sklearn.datasets

# Import the constants to have access to the toy datasets
from src import constants

# This is to convert dirty strings to integers
from lib.utils import robust_int_conversion


# Python is inferior to C++, as such it doesn't allow for basic functionality
# such as several constructor. This is "solved" (lol) by using this workaround.

def set_iris(self):

    '''
        Reset the dataframe to the IRIS dataset

        The IRIS dataset is a simple dataset with 150 rows and 5 columns, the
        columns are 4 numerical values and 1 categorical value.

        The columns are the following:

        - sepal length (cm) | float64
        - sepal width (cm)  | float64
        - petal length (cm) | float64
        - petal width (cm)  | float64
        - target            | categorical

    '''

    # Load the data from sklearn
    sampleData = sklearn.datasets.load_iris()

    # This is a complete clusterfuck of syntax, but to get the species you need to use this special command 0_o
    species_data = sampleData.target_names[sampleData.target] # we will save this for later

    # Get the dimensions and an empty dataframe
    df_n_rows         = len(sampleData.data)
    df_n_columns      = len(sampleData.data[0]) + 1
    self.totalRows    = df_n_rows
    self.totalColumns = df_n_columns
    self.data         = pd.DataFrame(index=range(df_n_rows),columns=range(df_n_columns))

    # Give the name to the object
    self.name = "Iris dataset"

    # Init the numerical data
    for i in range(df_n_rows):
        for j in range(df_n_columns-1):
            self[i,j] = sampleData.data[i][j]
            
    # Set the columns names
    irisNames = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)', 'species']
    self.renameColumns(irisNames)

    # Set the categories
    for i in range(df_n_rows):
        self[i,df_n_columns-1] = species_data[i]

    # Set the columns type correctly
    for j in range(df_n_columns-1):
        self.columnToFloat(j)
    self.columnToCategory(df_n_columns-1)

    # Return error code?
    return 0

load_iris = set_iris

# Initialize the spotify dataset
# This function will return three datasets:
@classmethod
def get_spotify_datasets(cls):

    # Load the data from the csv file
    completeData = pd.read_csv(constants.SPOTIFY_PATH, encoding='latin1')
    completeData_totalRows    = len(completeData.index)

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

    

    # --------------------
    # 0) Original dataset
    # --------------------
    #
    # The dataset is saved in a common csv. But this doesn't make any sense
    #
    # This needs to be transform into a proper dataset that follows the BCNF rules.
    #
    # This is what we have originally:
    #
    # track_name           : "Seven (feat. Latto) (Explicit Ver.)" , "LALA" , ...
    # artist(s)_name       : "Latto, Jung Kook", "Myke Towers", ...
    # artist_count         : 2, 1, ...
    # released_year        : 2023, 2023, ...
    # released_month       : 7, 3, ...
    # released_day         : 14, 23, ...
    # in_spotify_playlists : 553, 1474, ...
    # in_spotify_charts    : 147, 48, ...
    # streams              : 141381703, 133716286, ...
    # in_apple_playlists   : 43, 48, ...
    # in_apple_charts      : 263, 126, ...
    # in_deezer_playlists  : 45, 58, ...
    # in_deezer_charts     : 10, 14, ...
    # in_shazam_charts     : 826, 382, ...
    # bpm                  : 125, 92, ...
    # key                  : B, C#, ...
    # mode                 : Major, Major, ...
    # danceability_%       : 80, 71, ...
    # valence_%            : 89, 61, ...
    # energy_%             : 83, 74, ...
    # acousticness_%       : 31, 7, ...
    # instrumentalness_%   : 0, 0, ...
    # liveness_%           : 8, 10, ...
    # speechiness_%        : 4, 4, ...
    #
    # This is what we want:
    #
    # Artists:
    #
    # ArtistID         | ArtistName | ArtistTotalSongs
    #
    # Songs:
    #
    # SongID | track_name | released_year | released_month | released_day | in_spotify_playlists | in_spotify_charts | streams | in_apple_playlists | in_apple_charts | in_deezer_playlists | in_deezer_charts | in_shazam_charts | bpm | key | mode | danceability_% | valence_% | energy_% | acousticness_% | instrumentalness_% | liveness_% | speechiness_%
    #
    # Composers:
    #
    # SongID | ArtistID

    # Initialize the objects where we will store the three datasets

    # --------------------
    # A) Artists dataset
    # --------------------
    
    # The artists dataset is going to have three columns:
    # - ArtistID         | int (numerical ID)
    # - ArtistName       | str (name of the artist)
    # - ArtistTotalSongs | int (total number of songs by the artist)

    # ---- Initialize the dataframe for our artists database
    artistsDF   = cls( len(artists) , 3 , dtypes = ["int", "str", "int"])
    artistsDF.renameColumns(['ArtistID', 'ArtistName', 'ArtistTotalSongs'])
    
    # ---- Initialize the data
    for i in range(len(artists)):
        artistsDF[i,0] = i
        artistsDF[i,1] = artists[i]
        artistsDF[i,2] = 0

    # --------------------
    # B) Songs dataset
    # --------------------

    # The song dataset is going to have these columns:
    # - SongID               | int      (numerical ID)
    # - track_name           | str      (name of the song)
    # - artist_count         | int      (number of artists in the song)
    # - released_year        | int      (year of release)
    # - released_month       | int      (month of release)
    # - released_day         | int      (day of release)
    # - release_date         | date     (date of release)
    # - in_spotify_playlists | int      (number of playlists in spotify)
    # - in_spotify_charts    | int      (number of charts in spotify)
    # - streams              | int      (number of streams)
    # - in_apple_playlists   | int      (number of playlists in apple)
    # - in_apple_charts      | int      (number of charts in apple)
    # - in_deezer_playlists  | int      (number of playlists in deezer)
    # - in_deezer_charts     | int      (number of charts in deezer)
    # - in_shazam_charts     | int      (number of charts in shazam)
    # - bpm                  | int      (beats per minute)
    # - key                  | category (key of the song)
    # - mode                 | category (mode of the song)
    # - danceability_%       | int      (danceability percentage)
    # - valence_%            | int      (valence percentage)
    # - energy_%             | int      (energy percentage)
    # - acousticness_%       | int      (acousticness percentage)
    # - instrumentalness_%   | int      (instrumentalness percentage)
    # - liveness_%           | int      (liveness percentage)
    # - speechiness_%        | int      (speechiness percentage)

    song_dtypes = ["int", "str",      "int",      "int", "int",
                   "int", "date",     "int",      "int", "int",
                   "int", "int",      "int",      "int", "int",
                   "int", "category", "category", "int", "int",
                   "int", "int",      "int",      "int", "int"]

    songsDF      = cls(completeData_totalRows , 25, dtypes = song_dtypes)

    # Prepare the categorical values for key and mode
    #
    # Key
    #
    # The key of a song refers to the group of pitches, or scale, that forms
    # the basis of a music composition. The key can be designated by the root
    # note and quality (major or minor) of that scale. For example, if a song
    # is in the key of "C#", it means that the composition is centered around
    # the scale of C# (which could be either major or minor, depending on the
    # mode). The key helps in defining the harmonic and melodic
    # characteristics of the song.
    #
    # Mode
    #
    # The mode of a song indicates the type of scale that the composition
    # primarily uses. The two most common modes in Western music are Major
    # and Minor:
    #
    #     Major Mode: Typically sounds bright, happy, or uplifting.
    #     Minor Mode: Generally sounds sad, somber, or serious.

    # TODO: There's a FutureWarning: Setting an item of incompatible dtype is deprecated and will raise in a future error of pandas
    #
    # Because the default is NaN and pandas think this is a Float64, but it is a category.
    #
    # At the moment there's no default value for categories, so we will need to change it later

    # Key categories
    key_categories  = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    # Mode categories
    mode_categories = ['Major', 'Minor']

    # Assign the categories to the dataframe columns
    songsDF.set_categories(16, key_categories,  new_are_ordered = True)
    songsDF.set_categories(17, mode_categories, new_are_ordered = False)

    # Remove the NAs from the mode column
    # songsDF.remove_NA_category(17)

    # Initialize the data
    for i in range(completeData_totalRows):

        #print("--- **************** ---")
        #print(completeData.iloc[i,0])
        #print("--- **************** ---")

        # Prepare the date as date object
        current_year  = int(completeData.iloc[i, 3])
        current_month = int(completeData.iloc[i, 4])
        current_day   = int(completeData.iloc[i, 5])

        date_str     = f"{current_year}-{current_month}-{current_day}"
        current_date = pd.to_datetime(date_str)
        
        
        # Assign each column to the correct value
        songsDF[i,0]  = i                             # ID
        songsDF[i,1]  = completeData.iloc[i,0]        # Name
        songsDF[i,2]  = int(completeData.iloc[i,2])   # Artist count
        songsDF[i,3]  = current_year                  # Year
        songsDF[i,4]  = current_month                 # Month
        songsDF[i,5]  = current_day                   # Day
        songsDF[i,6]  = current_date                  # Date
        songsDF[i,7]  = int(completeData.iloc[i,6])   # Spotify playlists
        songsDF[i,8]  = int(completeData.iloc[i,7])   # Spotify charts
        songsDF[i,9]  = int(completeData.iloc[i,8])   # Streams
        songsDF[i,10] = int(completeData.iloc[i,9])   # Apple playlists
        songsDF[i,11] = int(completeData.iloc[i,10])  # Apple charts
        songsDF[i,12] = robust_int_conversion(completeData.iloc[i,11])  # Deezer playlists
        songsDF[i,13] = robust_int_conversion(completeData.iloc[i,12])  # Deezer charts
        songsDF[i,14] = pd.NA if(pd.isna(completeData.iloc[i,13])) else int(robust_int_conversion(completeData.iloc[i,12])) # Shazam charts
        songsDF[i,15] = int(completeData.iloc[i,14])  # BPM
        songsDF[i,16] = completeData.iloc[i,15]       # Key
        songsDF[i,17] = completeData.iloc[i,16]       # Mode
        songsDF[i,18] = int(completeData.iloc[i,17])  # Danceability
        songsDF[i,19] = int(completeData.iloc[i,18])  # Valence
        songsDF[i,20] = int(completeData.iloc[i,19])  # Energy
        songsDF[i,21] = int(completeData.iloc[i,20])  # Acousticness
        songsDF[i,22] = int(completeData.iloc[i,21])  # Instrumentalness
        songsDF[i,23] = int(completeData.iloc[i,22])  # Liveness
        songsDF[i,24] = int(completeData.iloc[i,23])  # Speechiness

    # Set the columns names
    my_columns_names = ['SongID', 'Track name', 'Total artists', 'Released year', 'Released month',
                        'Released day', 'Release date', 'in_spotify_playlists', 'in_spotify_charts',
                        'streams', 'in_apple_playlists', 'in_apple_charts', 'in_deezer_playlists',
                        'in_deezer_charts', 'in_shazam_charts', 'bpm', 'key', 'mode', 'danceability_%',
                        'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%',
                        'speechiness_%']

    songsDF.renameColumns(my_columns_names)


    # --------------------
    # C) Composer dataset
    # --------------------
    
    # Create the dataset where everything goes
    composersDF = cls(completeData_totalRows , 2, dtypes = ["int", "int"])
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

    # Set the names of each dataset
    artistsDF.name   = "Artists dataset"
    songsDF.name     = "Songs dataset"
    composersDF.name = "Composers dataset"

    # Return the three datasets
    return [artistsDF, songsDF, composersDF]