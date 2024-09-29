# -----------------------------------------------------------------------------
#
# Prerequisites:
#
# Install the required packages in your Python enviroment. Usually these works
#
# pip install pandas
# pip install matplotlib
# pip install sklearn
# pip install -U scikit-learn
# -----------------------------------------------------------------------------


# Import Seagull for testing
from src.Seagull.Seagull      import Seagull
from src.Plot.Plot            import Plot
from src.Plot.Heatmap.Heatmap import Heatmap

import constants

# Example of how to construct a Seagull object and play around with it
def main():

    # -------------------------------------------------------------------------
    # Constants initialization
    # -------------------------------------------------------------------------
    # Tell in which folder are we saving the images
    SAVING_FOLDER = constants.OUT_FOLDER
    # -------------------------------------------------------------------------


    # -------------------------------------------------------------------------
    # Example 1:
    # 
    #   - Create a Seagull object of size 5 x 3 which is empty
    #   - Initialize the same object to the iris dataset
    #   - Print an overview of such object
    # -------------------------------------------------------------------------
    print()
    print(" -- Example 1 -- ")
    print()
    # -------------------------------------------------------------------------

    # Prepare the dataframe
    irisDF = Seagull(5,3)
    irisDF.set_iris()
    irisDF.print_overview()

    # -------------------------------------------------------------------------
    # Example 2:
    # 
    #   - Create a default spotify dataset. This is composed of three tables
    #         Table 0: Artists
    #         Table 1: Songs
    #         Table 2: Which artist compose each song
    #
    #   - Prepare the data for a heatmap.
    #     We will plot the top 20 artist, and which month of the year they
    #     release their songs.
    #
    #   - Show how to plot a heatmap
    # -------------------------------------------------------------------------
    print()
    print(" -- Example 2 -- ")
    print()
    # -------------------------------------------------------------------------


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


    # Until here, the data is ready.
    # Now let's do the plotting



    # This is the default initialization of the heatmap object.
    myImportantHeatmap = Heatmap(SAVING_FOLDER)

    # Update the heatmap with the new data and show it
    myImportantHeatmap.update_from_seagull(heatmapDataDF)
    
    # Lets give it new labels
    myImportantHeatmap.set_name("Top_20_artists_by_month")
    myImportantHeatmap.set_title("Top 20 artists and the month of the year they release their songs")
    myImportantHeatmap.set_x_label("Month")
    myImportantHeatmap.set_y_label("Top 20 artists")

    # Show the figure, this open up a window in runtime
    myImportantHeatmap.show()

    # Show the plot in the terminal via string representation
    print(myImportantHeatmap)

    # Save the plot
    myImportantHeatmap.save()


    # -------------------------------------------------------------------------
    # Example 3:
    # 
    #   - Create a Seagull object from a csv file
    #   - Print an overview of such object
    # -------------------------------------------------------------------------
    print()
    print(" -- Example 3 -- ")
    print()
    # -------------------------------------------------------------------------

    # Prepare the dataframe
    irisDF = Seagull()
    irisDF.loadFromCSV(constants.IRIS_PATH)  
    irisDF.print_overview()

    # -------------------------------------------------------------------------
    # Example 4:
    # 
    #   - Do a barplot    
    #   - Do a regression plot
    #   - Do a boxplot plot    
    # -------------------------------------------------------------------------
    print()
    print(" -- Example 4 -- ")
    print()
    # -------------------------------------------------------------------------


# Call the main function
if __name__ == "__main__":
    main()