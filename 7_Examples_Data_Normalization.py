# Pandas
import pandas as pd
import numpy  as np

# Seagull
from src.Seagull.Seagull import Seagull

def main():

    # Load the Spotify dataset
    spotify_instances = Seagull.get_spotify_datasets()

    spotify_ArtitstDF   = spotify_instances[0]
    spotify_SongsDF     = spotify_instances[1]
    spotify_ComposersDF = spotify_instances[2]

    # Change the NA categorical values to "Not-Defined"
    spotify_SongsDF.swap_NA_category(16, "Not-Defined")

    # ----------------------------------------------------------------------
    # Prepare the data for the plots
    #
    # ---- Get the top 20 artists
    # ---- Count how many songs each release each month
    # ---- Normalize the data from 0 to 1
    # ---- Normalize the data with respect to the mean and standard deviation
    #
    # ----------------------------------------------------------------------

    # How many artists do you want
    total_top_artists = 20

    # Prepare the dataframe that will be use in the Heatmap later
    heatmap_data_types = ["object",
                          "float", "float", "float", "float", "float", "float",
                          "float", "float", "float", "float", "float", "float"]

    heatmap_data_df = Seagull(total_top_artists , 13, dtypes = heatmap_data_types)
    heatmap_data_df.renameColumns(["Artist", "January", "February", "March",      "April",  "May",     "June",
                                             "July",    "August",    "September", "October","November","December"])

    #       Get the top 20 artists
    top_artistsDF = spotify_ArtitstDF.copy()
    top_artistsDF.keepColumnTopValues(2, topValues = total_top_artists)

    #       Initialize the heatmap data with the artists names
    heatmap_data_df[:,0] = top_artistsDF[:,1]

    #       Initialize the rest of the heatmap data with zeros which are integers
    for i in range(12):
        heatmap_data_df.setColumnZeroes(i+1)

    #       For each artist, get the number of songs released in each month
    for i in range(total_top_artists):

        # Get the artist ID
        artistID   = top_artistsDF[i,0]

        # Search for the song made by this artist ID
        songsIDs = spotify_ComposersDF.getPanda().iloc[spotify_ComposersDF.getPanda().iloc[:, 1].values == artistID, 0].values

        # For each song, get the month of the year
        for j in range(len(songsIDs)):

            # Get the song ID
            songID = songsIDs[j]

            # Get the month of the year
            currentSong  = spotify_SongsDF.getPanda().iloc[spotify_SongsDF.getPanda().iloc[:, 0].values == songID, ]
            currentMonth = currentSong.iloc[0,4]

            # Add one to the heatmap
            heatmap_data_df[i,currentMonth] = heatmap_data_df[i,currentMonth] + 1.0

    # Normalize the data.
    #
    # We are going to show three normalizations
    #
    #     1) Normalize the whole dataset
    #
    #        This is the most common normalization, it is used to make the data
    #        comparable. It is used when the data is in different scales.
    #
    #        In our example, this will serve to show who is releasing the more
    #        songs in a month in comparison to the rest of the artists.
    #
    #     2) Normalize the data by rows
    #
    #       This normalization is used to show the percentage of songs released
    #       by each artist in each month. This is useful to see if there is a
    #       trend of top 20 artist releasing, for example, in summer just before
    #       the disco parties season, or in winter just before the Christmas season,
    #       in time for giving CD presents.
    #
    #     3) Normalize the data by columns
    #
    #       This normalization is used to show the percentage of songs released
    #       in each month by all the artists. This is useful to see if there is a
    #       trend of songs being released in a specific month.

    # Initialize the dataframes
    normilize_absolute   = heatmap_data_df.copy()
    normilize_by_rows    = heatmap_data_df.copy()
    normilize_by_columns = heatmap_data_df.copy()

    # Normalize the whole dataset
    # (notice that non numerical columns are ignored)
    normilize_absolute.normalize()
    normilize_by_rows.normalize_rows()
    normilize_by_columns.normalize_columns()

    # Show the results
    print(normilize_absolute.str_overview())
    print(normilize_by_rows.str_overview())
    print(normilize_by_columns.str_overview())

    if(False):


        
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