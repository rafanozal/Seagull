# Install the required packages in your Python enviroment:

# pip install matplotlib
# pip install sklearn
# pip install -U scikit-learn


# General libraries
#import numpy as np
#import matplotlib as mpl
#import matplotlib.pyplot as plt

#import random

# Import Seagull for testing

from Seagull      import Seagull
from Plot         import Plot
from Plot.Heatmap import Heatmap

# Example of how to construct a Seagull object and play around with it
def main():

    # Try plotting

    myImportantHeatmap = Heatmap("data/iris.csv")

    myImportantHeatmap.heatmap()

    myImportantHeatmap.show()

    # Define an empty Seagull object of 5 rows and 3 columns
    # We will put the iris dataset here
    irisDF = Seagull(5,3)
    irisDF.set_iris()
    irisDF.print_overview()

    # Define an empty Seagull object of 5 rows and 3 columns
    # We will put the iris dataset here
    spotify_instances = Seagull.get_spotify_datasets()

    spotifyArtitstDF = spotify_instances[0]
    spotifyArtitstDF.print_overview()

    spotifySongsDF = spotify_instances[1]
    spotifySongsDF.print_overview()

    spotifyComposersDF = spotify_instances[2]
    spotifyComposersDF.print_overview()

    # Lets do some basic plotting examples

    # ---- Lets make a heatmap with some music information ----

    #      Prepare the heapmap data
    #      We will plot the top X artist, and which month of the year they release their songs
    totalTopArtists = 20

    heatmapDataDF = Seagull(totalTopArtists,13)
    heatmapDataDF.renameColumns(["Artist", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October","November","December"])

    #       Get the top 20 artists
    topArtistsDF = spotifyArtitstDF.copy()
    topArtistsDF.keepColumnTopValues(2, topValues = totalTopArtists)
    topArtistsDF.print_overview()

    #       Initialize the heatmap data with the artists names
    heatmapDataDF[:,0] = topArtistsDF[:,1]

    #       Initialize the rest of the heatmap data with zeros which are integers
    for i in range(12):
        heatmapDataDF.setColumnZeroes(i+1)

    heatmapDataDF.print_overview()

    #print(heatmapDataDF[0,0])
    #print(heatmapDataDF[0,1])
    #print(heatmapDataDF[0,8])
    #print( type(heatmapDataDF[0,0]))
    #print( type(heatmapDataDF[0,8]))

    #       For each artist, get the number of songs released in each month
    for i in range(totalTopArtists):

        # Get the artist ID
        artistID   = topArtistsDF[i,0]
        artistName = topArtistsDF[i,1]

        # Search for the song made by this artist ID
        songsIDs = spotifyComposersDF.getPanda().iloc[spotifyComposersDF.getPanda().iloc[:, 1].values == artistID, 0].values
        
        print(songsIDs)

        #songsIDs = spotifyComposersDF.keepColumnByValue(1, artistID)

        # For each song, get the month of the year
        for j in range(len(songsIDs)):
            songID = songsIDs[j]

            # Get the month of the year
            #currentSong = spotifySongsDF.getPanda.loc[spotifySongsDF.getPanda()[0] == songID]
            currentSong = spotifySongsDF.getPanda().iloc[spotifySongsDF.getPanda().iloc[:, 0].values == songID, ]
            #print(currentSong)

            #currentSong = spotifySongsDF.getPanda().iloc[spotifySongsDF.getPanda().iloc[:, 0].values == songID, ].values

            #print(currentSong)

            #currentSong  = spotifySongsDF.keepColumnByValue(0, songID)
            currentMonth = currentSong.iloc[0,4]

            #print(currentMonth)
            #print( type(currentMonth))
            #print( type(i))

            # Add one to the heatmap
            heatmapDataDF[i,currentMonth] = heatmapDataDF[i,currentMonth] + 1


    heatmapDataDF.print_overview()

# Call the main function
if __name__ == "__main__":
    main()