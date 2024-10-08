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
    save_folder = constants.DENSITY_PLOTS_PATH
    
    # Try with Iris
    my_sg = Seagull()
    my_sg.set_iris()

    # Try with Spotify
    spotify_instances = Seagull.get_spotify_datasets()

    spotify_ArtitstDF   = spotify_instances[0]
    spotify_SongsDF     = spotify_instances[1]
    spotify_ComposersDF = spotify_instances[2]

    my_plot = Density_plot(save_folder, "my_density_plot_0")
    my_plot.init_from_seagull(my_sg, 0)
    my_plot.automatic_titles()
    my_plot.show_extra_info()
    my_plot.save()    

    my_plot = Density_plot(save_folder, "my_density_plot_1")
    my_plot.init_from_seagull(spotify_SongsDF, "Released month")
    my_plot.automatic_titles()
    my_plot.show_extra_info()
    my_plot.save()    

    my_plot = Density_plot(save_folder, "my_density_plot_2")
    my_plot.init_from_seagull(spotify_SongsDF, "in_spotify_playlists")
    my_plot.automatic_titles()
    my_plot.show_extra_info()
    my_plot.save()    

    my_plot = Density_plot(save_folder, "my_density_plot_3")
    my_plot.init_from_seagull(spotify_SongsDF, "bpm")
    my_plot.automatic_titles()
    my_plot.show_extra_info()
    my_plot.save()    

    my_plot = Density_plot(save_folder, "my_density_plot_A")
    my_plot.automatic_titles()
    my_plot.show_extra_info()
    my_plot.save()

    my_plot = Density_plot(save_folder, "my_density_plot_B")
    my_plot.style(line_thickness = 5, color_line = 'blue', color_fill_start = 'lightblue', color_alpha_end = 0.1)
    my_plot.save()

    my_plot = Density_plot(save_folder, "my_density_plot_C")
    my_plot.style(line_thickness = 5, color_line = 'green',
                  color_fill_start = 'lightgreen', color_alpha_start = 1,
                  color_fill_end   = 'magenta',    color_alpha_end   = 0.0,
                  color_alpha_stop = 0.5)
    my_plot.show_extra_info()
    my_plot.save()

    return 0

if __name__ == "__main__":
    main()