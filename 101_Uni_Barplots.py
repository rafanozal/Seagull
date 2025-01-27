# Pandas
import pandas as pd

# Constants
from src import constants

# Seagull
from src.Seagull.Seagull import Seagull

# Plots
from src.Plot.V1_Plot.V1_Categorical.Plots.V1_Barplot import Barplot

def main():

    # Where do you want to save the plots
    # Otherwise they will go to cwd()
    save_folder = constants.BARPLOT_PATH
    
    print("---------------------------------------------------------------")
    print(" LOADING DATASETS ")
    print("---------------------------------------------------------------")

    # region

    # Load the Iris dataset
    irisDF = Seagull()
    irisDF.set_iris()

    # Load the Spotify dataset
    #spotify_instances   = Seagull.get_spotify_datasets()
    #spotify_ArtitstDF   = spotify_instances[0]
    #spotify_SongsDF     = spotify_instances[1]
    #spotify_ComposersDF = spotify_instances[2]

    print("---------------------------------------------------------------")
    print(" Create a plot with random data and save it ")
    print("---------------------------------------------------------------")

    # Create the plot with random data and save it in the given folder
    my_random_plot = Barplot(folder_path = save_folder)
    my_random_plot.save()                                                                           # "Barplot_Random Data.png"

    print("---------------------------------------------------------------")
    print(" Create a plot and init from Seagull ")
    print("---------------------------------------------------------------")

    my_iris_plot = Barplot(irisDF, 'species', save_folder)
    my_iris_plot.set_title("How many species are there?")
    my_iris_plot.save()                                                                           # "Barplot_4_Iris dataset"

    print("---------------------------------------------------------------")
    print(" I don't like the random plot, let's change it ")
    print("---------------------------------------------------------------")
    fill_colors   = ["#FF00FF", "#FFFF00", "#00FFFF", "#FFFFFF", "#FF0000"]
    border_colors = ["#00FF00", "#0000FF", "#FF0000", "#000000", "#00FFFF"]
    fill_alpha    = [0.5,       0.6,       0.7,       0.8,       0.9]
    border_thick  = [1,         2,         3,         4,         5]

    my_random_plot.set_title("GrAPhic DeSiGn is my pAsSiOn!")
    my_random_plot.set_style(fill_color_list       = fill_colors,
                             border_color_list     = border_colors,                  
                             fill_alpha_list       = fill_alpha,
                             border_thickness_list = border_thick,)

    my_random_plot.set_filename("Much better now")
    my_random_plot.save()                            

    return 0

    print("---------------------------------------------------------------")
    print(" Compare the spotify playlist for a few selected artists ")
    print("---------------------------------------------------------------")
    
    # Get the top 5 artists (the ones with the most songs)
    total_top_artists = 5
    top_artists_DF    = spotify_ArtitstDF.keep_column_top_values("ArtistTotalSongs", topValues = total_top_artists)
    top_artists_names = top_artists_DF[1].to_list()
    top_artists_ids   = top_artists_DF[0].to_list()

    # From the top 5 artists, get their songs
    row_mask             = spotify_ComposersDF.mask("ArtistID", top_artists_ids)   # This give you the mask, not the data
    top_artists_songs_DF = spotify_ComposersDF[row_mask,:]                         # Use the mask as you please later on
    target_songs_ids     = top_artists_songs_DF["SongID"].to_list()

    # From the songs database, get the songs that are in the top 5 artists
    target_songs_DF      = spotify_SongsDF.inside("SongID", target_songs_ids)      # This give you the Seagull with the data, not the mask
    # We only care about the Song ID and the number of playlists, so drop everything else
    target_songs_DF.keep_columns(["SongID", "in_spotify_playlists"], inplace = True)


    # We need to do a bit of a conversion to get the data in the right format
    #
    # Artist Name | Song ID | Playlists (How many playlist have the song)
    final_DF = Seagull(total_rows = target_songs_DF.getTotalRows(), total_columns = 3, dtypes=["string", "int", "int"])
    final_DF.renameColumns(["Artist Name", "Song ID", "Playlists"])
    final_DF[1] = target_songs_DF["SongID"]
    final_DF[2] = target_songs_DF["in_spotify_playlists"]

    # This is really slow
    # Never do this!
    #
    # For each song, get the artist name
    #for i in range(final_DF.totalRows):
    #
    #    # Get the ID
    #    current_song_id     = final_DF[i,1]
    #
    #    # Get the artist ID
    #    current_artist_id   = spotify_ComposersDF.inside("SongID", current_song_id)["ArtistID"].to_list()[0]
    #
    #    # Find the artist name
    #    current_artist_name = spotify_ArtitstDF.inside("ArtistID", current_artist_id)["ArtistName"].to_list()[0]
    #
    #    # Save the artist name
    #    final_DF[i,0] = current_artist_name

    # Do this instead
    first_join  = spotify_ComposersDF.get_data().merge( target_songs_DF.get_data() , on = 'SongID',   how = 'inner')
    second_join = first_join.merge( spotify_ArtitstDF.get_data() ,                   on = 'ArtistID', how = 'inner')
    second_join = second_join.iloc[:,2:4] # Only keep the Playlists and the Artist Name
    final_DF = Seagull.from_pandasDF(second_join)

    print(final_DF.str_overview())

    print(final_DF.get_column_type(1))

    print(constants.SOFT_CATEGORIES)

    print(final_DF.get_column_type(1) in constants.SOFT_CATEGORIES)

    my_plot = Distributions_plot(final_DF, 'in_spotify_playlists', 'ArtistName', save_folder)  # The given column is not categorical, but the
    my_plot.set_title("Comparing playlists by artists")                                        # plot doesn't care and will treat it as such
    my_plot.set_subtitle("")
    my_plot.save()                                                                           # "Multidensity_Plot_Iris dataset_0_1"
    

    print("---------------------------------------------------------------")
    print(" Compare the spotify playlist for a few selected artists ")
    print("  Compare top artists by number of songs (total) with top artists by average playlist songs (boxplot and absolute count each)")
    print("---------------------------------------------------------------")

    return 0



if __name__ == "__main__":
    main()