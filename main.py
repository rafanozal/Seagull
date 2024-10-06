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
#
#
# Recomended for the IDE
#
# pip install mypy
# -----------------------------------------------------------------------------


# Pandas
import pandas as pd

# Seagull
from src.Seagull.Seagull      import Seagull

# Plots
from src.Plot.Plot            import Plot
from src.Plot.Heatmap.Heatmap import Heatmap
from src.Plot.Barplots.Horizontal_Barplot import Horizontal_Barplot

# Analysis
from src.Analysis.Analysis              import Analysis
from src.Analysis.Numerical_Categorical import Numerical_Categorical

from src import constants

# Example of how to construct a Seagull object and play around with it
def main():

    # -------------------------------------------------------------------------
    # Constants initialization
    # -------------------------------------------------------------------------
    # Tell in which folder are we saving the images
    SAVING_FOLDER = constants.OUT_FOLDER
    # -------------------------------------------------------------------------

    # Tell which modules do you want to test
    TEST_ALL        = False
    TEST_BASICS     = False
    TEST_RW         = True
    TEST_CATEGORIES = False
    TEST_MIXED      = False
    TEST_HEATMAPS   = False
    TEST_CSV        = False
    TEST_BARPLOTS   = False           
    TEST_NUMCATS    = False           
    TEST_VODOROY    = False            


    # -------------------------------------------------------------------------
    # Example Categorical:
    # 
    #   - Create a random categorical Seagull object
    #   - Print an overview of such object
    # -------------------------------------------------------------------------
    if(TEST_ALL or TEST_CATEGORIES):

        print()
        print(" -- Example Categorical -- ")
        print()

        # ---------------------------------------------------------------------
        # Prepare the dataframe
        # ---------------------------------------------------------------------
        categoricalDF = Seagull(20,10)
        categoricalDF.randomize_categorical()
        categoricalDF.print_overview()

        summaryDF = categoricalDF.summarize_categorical_column(4)
        summaryDF.print_overview()
        

    # -------------------------------------------------------------------------
    # Example Heatmaps:
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
    if(TEST_ALL or TEST_HEATMAPS):

        print()
        print(" -- Example Heatmap -- ")
        print()

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


    # -------------------------------------------------------------------------
    # Example CSV:
    # 
    #   - Create a Seagull object from a csv file
    #   - Print an overview of such object
    # -------------------------------------------------------------------------
    if(TEST_ALL or TEST_CSV):

        print()
        print(" -- Example CSV -- ")
        print()
    
        # ---------------------------------------------------------------------
        # Prepare the dataframe
        # ---------------------------------------------------------------------

        irisDF = Seagull()
        irisDF.loadFromCSV(constants.IRIS_PATH)  
        irisDF.print_overview()

    # -------------------------------------------------------------------------
    # Example 4:
    # 
    #   - Do a barplot 
    # -------------------------------------------------------------------------
    if(TEST_ALL or TEST_BARPLOTS):

        print()
        print(" -- Example Barplots -- ")
        print()

        # ---------------------------------------------------------------------
        # Init a random barplot, show it, and save it
        # ---------------------------------------------------------------------
        myHB = Horizontal_Barplot(SAVING_FOLDER)
        myHB.show()
        print(myHB)
        myHB.save()

    # -------------------------------------------------------------------------
    # Example 4:
    # 
    #   - Do a barplot 
    # -------------------------------------------------------------------------
    if(TEST_ALL or TEST_NUMCATS):

        print()
        print(" -- Example Numerical Categorical Analysis -- ")
        print()

        myAnalysis = Numerical_Categorical(folder_path = SAVING_FOLDER)
        results = myAnalysis.get_parametric_pvalue()
        print()
        print(results)
        print()
        print(myAnalysis)
        myAnalysis.save()


# Call the main function
if __name__ == "__main__":
    main()