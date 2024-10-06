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

    # Show the summary of the categorical column 16 (Key)
    my_summary = spotify_SongsDF.summarize_categorical_column(16)
    print(my_summary)


if __name__ == "__main__":
    main()