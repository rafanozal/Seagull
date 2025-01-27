# Pandas
import pandas as pd

# Constants
from src import constants

# Seagull
from src.Seagull.Seagull import Seagull



def main():

    
    print("---------------------------------------------------------------")
    print(" LOADING DATASETS ")
    print("---------------------------------------------------------------")

    # region

    # Load the Iris dataset
    irisDF = Seagull()
    irisDF.set_iris()

    # Load the Spotify dataset
    spotify_instances   = Seagull.get_spotify_datasets()
    spotify_ArtitstDF   = spotify_instances[0]
    spotify_SongsDF     = spotify_instances[1]
    spotify_ComposersDF = spotify_instances[2]

    print(spotify_SongsDF.str_overview())

    print("---------------------------------------------------------------")
    print(" Get the songs of the top 5 artists ")
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

    # This Seagull contain all the songs of all the artists that we wanted (top 5)
    # But we don't have the artist names, only the artist IDs
    #
    # We are going to show a cross join, which is a join that returns all the possible combinations of two dataframes
    # In our case, we want to show:
    #
    # Song ID (A) | Artist ID (B) | Song Name (C) | Artist Name (D)
    #
    # A and B     in     spotify_ComposersDF  (complete data) - Song ID   and Artist ID
    #    C        in     target_songs_DF      (filtered data) - Song ID   and Song Name
    #    D        in     spotify_ArtitstDF    (complete data) - Artist ID and Artist Name

    # Join C with (A,B) , this will give us the artist IDs that we want (one song can have multiple artists)
    # We only care about the track name, so drop everyhting else (columns 3 and beyond)
    first_join  = spotify_ComposersDF.get_data().merge( target_songs_DF.get_data() , on='SongID', how='inner')
    first_join  = first_join.iloc[:,0:3]
    
    # Joing D with the previous (A,B,C)
    # Keep the Artist Name and the Track Name (columns 2 and 3)
    second_join = first_join.merge( spotify_ArtitstDF.get_data() , on='ArtistID', how='inner')
    second_join = second_join.iloc[:,2:4]

    # Print the results
    print()
    print("The top 5 artists are:" + str(top_artists_names))
    print()
    print("Their songs of the top 5 artists are:")
    #print(target_songs_DF["Track name"].to_list())
    print("Total: " + str(target_songs_DF.getTotalRows()))
    print("Total (joint): " + str(second_join.shape))

    # Return and end example
    return 0

if __name__ == "__main__":
    main()


'''

myDF[0] = Seagull , Pandas inside, Data inside?

Right now is Pandas inside

myDF.copy([0]) get you the seagull

mmyDF[0].to_list() get you the data

mmyDF[0].values get you the weird panda array data


If I get the data: is a list and can't override ==

If I get the seagull: I can't get the data with one line, but can override ==

myDF.in("Name", list of values) -> return the rows that have the values list in the column "Name" or whatever list of columns

'''
