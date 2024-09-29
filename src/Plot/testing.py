# DELETE THIS FILE EVENTUALLY!!



# So, Python is weird and doesn't like importing with relative paths
# as we can do with #include in C++. So we need to add the path to the
# root folder to the system path. This is done with the following lines:

import sys
import os
from pathlib import Path

SCRIPT_DIR_PATH = os.path.dirname(  os.path.abspath(__file__))  # Where is this script?
MY_ROOT_PATH = Path(SCRIPT_DIR_PATH)
MY_ROOT_PATH = MY_ROOT_PATH.parent.absolute()                   # Go up one level twice.
#MY_ROOT_PATH = MY_ROOT_PATH.parent.absolute()                   # If you change the folder structure, you will need to change this lines.

print(MY_ROOT_PATH)

sys.path.append(os.path.dirname(MY_ROOT_PATH))                  # Add the root folder to the PYTHONPATH

print(MY_ROOT_PATH)

# Now we can import everything using the relative path
import Seagull.constants as constants
from Heatmap.Heatmap import Heatmap
from Seagull.Seagull import Seagull

# -----------------------------------------------------------------
# Showing the basic constructor
# -----------------------------------------------------------------

# Examples of how to construct a Plot object with default values
# This will create a heatmap with 2 rows and 2 columns and random values
# This is the default initialization of the heatmap object.
myImportantHeatmap = Heatmap(constants.TEST_FOLDER)
#myImportantHeatmap.show()
myImportantHeatmap.save()




# -----------------------------------------------------------------
# Preparing the data and plotting it
# -----------------------------------------------------------------

# Example on how to change the data using the Seagull object
spotify_instances  = Seagull.get_spotify_datasets()
spotifyArtitstDF   = spotify_instances[0]
spotifySongsDF     = spotify_instances[1]
spotifyComposersDF = spotify_instances[2]

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

#       For each artist, get the number of songs released in each month
for i in range(totalTopArtists):

    # Get the artist ID
    artistID   = topArtistsDF[i,0]
    artistName = topArtistsDF[i,1]

    # Search for the song made by this artist ID
    songsIDs = spotifyComposersDF.getPanda().iloc[spotifyComposersDF.getPanda().iloc[:, 1].values == artistID, 0].values

    # For each song, get the month of the year
    for j in range(len(songsIDs)):
        songID = songsIDs[j]

        # Get the month of the year
        currentSong = spotifySongsDF.getPanda().iloc[spotifySongsDF.getPanda().iloc[:, 0].values == songID, ]

        currentMonth = currentSong.iloc[0,4]

        # Add one to the heatmap
        heatmapDataDF[i,currentMonth] = heatmapDataDF[i,currentMonth] + 1


# Show the heatmap data
heatmapDataDF.print_overview()

# Normalize the data by rows
# In this case, we are interested in the percentage of songs released in each month
# and check whether there is a trend of top 20 artist releasing, for example, in summer
heatmapDataDF.normalize(column=False, avoidFirstColumn=True)
heatmapDataDF.print_overview()

# Update the heatmap with the new data and show it
myImportantHeatmap.update_from_seagull(heatmapDataDF)
myImportantHeatmap.show()

# Lets give it a new name and save it
myImportantHeatmap.set_name("Top 20 artists and the month of the year they release their songs")
myImportantHeatmap.save()