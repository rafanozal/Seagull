# Pandas
import pandas as pd
import numpy  as np

# Constants
from src import constants

# Seagull
from src.Seagull.Seagull import Seagull

# Plots
from src.Plot.V1Plot.V1Numerical.V1_Density import Density_plot

def main():

    # Where do you want to save the plots
    # Otherwise they will go to cwd()
    save_folder = constants.DENSITY_PLOTS_PATH
    
    print("---------------------------------------------------------------")
    print(" LOADING DATASETS ")
    print("---------------------------------------------------------------")

    # region

    # Load the Iris dataset
    irisDF = Seagull()
    irisDF.set_iris()

    # Load the Spotify datasets
    spotify_instances = Seagull.get_spotify_datasets()

    spotify_ArtitstDF   = spotify_instances[0]
    spotify_SongsDF     = spotify_instances[1]
    spotify_ComposersDF = spotify_instances[2]

    # Load a custom dataset
    my_panda_data = {
        'ID': [1, 2, 3, 4, 5],                                                                               # Integer data
        'Weight': [60.5, 70.2, 55.9, 85.3, 68.7],                                                            # Float data
        'Birthday': pd.to_datetime(['1990-01-01', '1992-05-15', '1985-07-30', '1988-11-25', '1993-03-05']),  # Date data
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],                                                 # String data
        'Nationality': pd.Categorical(['American', 'British', 'Canadian', 'Dutch', 'Estonian'])              # Categorical data
    }
    panda_df = pd.DataFrame(my_panda_data)

    # endregion

    print("---------------------------------------------------------------")
    print(" Create a plot with random data and show it ")
    print("---------------------------------------------------------------")

    # Create the plot with random data and show it
    # If saved, will be saved in the current working directory (cwd)
    my_plot = Density_plot()
    my_plot.show()

    print("---------------------------------------------------------------")
    print(" Create a plot with random data and save it ")
    print("---------------------------------------------------------------")

    # Create the plot with random data and save it in the given folder
    my_plot = Density_plot(folder_path = save_folder)
    my_plot.save()                                                                            # "Density_Plot.png"

    # Create the plots and where to save it
    # Initialize it with the data afterwards
    my_plot = Density_plot(folder_path = save_folder)
    my_plot.init_from_seagull(irisDF, 0)
    my_plot.save()                                                                            # "Iris_dataset_sepal_length_cm_Density_Plot.png"

    # Create the plot and initilize it at the same time using the column name
    my_plot = Density_plot(spotify_SongsDF, "Released month",  save_folder,
                           filename = "Songs releases by month")
    my_plot.save()                                                                            # "Songs releases by month.png" (beware of spaces!)
                                                                                              # Is still good idea to avoid spaces in filenames for LaTeX
    # Create the plot and initilize it at the same time using the column index
    # Column 7 is "in_spotify_playlists" column
    my_plot = Density_plot(spotify_SongsDF, 7, save_folder,
                           filename = "Songs_popularity_percentiles")
    my_plot.save()                                                                            # Songs_popularity_percentiles.png
    
    # Create the plot and change the style
    my_plot = Density_plot(spotify_SongsDF, "bpm", save_folder,
                           filename = "BPM in blue")                                          
    my_plot.style(line_thickness = 5, color_line = 'blue', color_fill_start = 'lightblue',    # Plot the BMP with a blue style
                  color_alpha_end = 0.1)
    my_plot.save()                                                                            # "BMP in blue.png"

    my_plot.change_filename("BPM_in_fancy")                                                   # Set the filename to "BMP in fancy"

    my_plot.style(line_thickness = 5, color_line = 'green',                                   # Plot the BMP with a questionable
                  color_fill_start = 'lightgreen', color_alpha_start = 1,                     # green to magenta shade style
                  color_fill_end   = 'magenta',    color_alpha_end   = 0.0,
                  color_alpha_stop = 0.5)
    my_plot.save()                                                                            # "BMP in fancy.png"

    # Create the plot with a non-seagull object

    # Create the plot with previously saved plot state

    

    # Return and end example
    return 0

if __name__ == "__main__":
    main()