# Pandas
import pandas as pd
import numpy  as np

# Seagull
from src.Seagull.Seagull import Seagull

def main():

    print("---------------------------------------------------------------")
    print(" LOADING COMMON DATASETS ")
    print("---------------------------------------------------------------")

    # Toy datasets come in two flavors. First are datasets with a unique
    # dataframe, and second are datasets with multiple dataframes.
    
    print("---------------------------------------------------------------")
    print(" 1.- Loading the Iris dataset")
    print("---------------------------------------------------------------")

    # Iris dataset is an example of the first case, in which nothing
    # is special is done with the data, just loaded and shown.

    my_sg = Seagull()
    my_sg.set_iris()

    print(my_sg.str_overview())
    
    print("---------------------------------------------------------------")
    print(" 2.- Loading the Spotify dataset")
    print("---------------------------------------------------------------")

    # Spotify dataset is an example of the second case, in which the data
    # is loaded and then processed to create three different dataframes.

    # Notice that we didn't create the Seagull object before loading the
    # dataset. This is because the method is a class method, and
    # it is called directly from the class.

    # Also notice that, while the original data is contained in a single
    # CSV file where everything is mixed, in our case we divided the data
    # so it follows the proper BCNF rules.

    # We also included a little bit of optimization in the data.
    #
    # For example, for the songs we have the year, month, and day as
    # separate integer columns, but we also included a column with the
    # date, as date type, with format YYYY-MM-DD.
    #
    # The count of composers can be infer from the composer dataset,
    # but we also included a column with the count of composers in the
    # song dataset so it is faster to load such data.
    #
    # We also included a little bit of data cleaning.
    #
    # The song Love Grows (Where My Rosemary Goes) has a wrong stream count,
    # instead of an integer, there's a string where the BMP, Type of song, etc... is mixed.
    # So we changed the stream count to 0.

    spotify_instances = Seagull.get_spotify_datasets()

    spotify_ArtitstDF   = spotify_instances[0]
    spotify_SongsDF     = spotify_instances[1]
    spotify_ComposersDF = spotify_instances[2]

    print("--------------------------------")
    print("   Artists dataset")
    print("--------------------------------")
    print()
    print(spotify_ArtitstDF.str_overview())

    print("--------------------------------")
    print("   Songs dataset")
    print("--------------------------------")
    print()
    print(spotify_SongsDF.str_overview())

    print("--------------------------------")
    print("   Composers dataset")
    print("--------------------------------")
    print()
    print(spotify_ComposersDF.str_overview())

    

    if(False):

        # ----------------------------------------------------------------------
        # Load the spotify data into the three different datasets
        # ----------------------------------------------------------------------
        spotify_instances = Seagull.get_spotify_datasets()

        spotifyArtitstDF = spotify_instances[0]
        spotifyArtitstDF.print_overview()

        spotifySongsDF = spotify_instances[1]
        spotifySongsDF.print_overview()

        spotifyComposersDF = spotify_instances[2]
        spotifyComposersDF.print_overview()

        # ----------------------------------------------------------------------
        # Prepare the data for the plots
        #
        # ---- Get the top 20 artists
        # ---- Count how many songs each release each month
        # ---- Normalize the data from 0 to 1
        #
        # ----------------------------------------------------------------------

        # How many artists do you want
        totalTopArtists = 20

        # Prepare the dataframe that will be use in the Heatmap later
        heatmapDataDF = Seagull(totalTopArtists , 13)
        heatmapDataDF.renameColumns(["Artist", "January", "February", "March", "April", "May", "June",
                                        "July", "August", "September", "October","November","December"])

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


if __name__ == "__main__":
    main()