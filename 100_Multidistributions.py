# Pandas
import pandas as pd

# Constants
from src import constants

# Seagull
from src.Seagull.Seagull import Seagull

# Plots
from src.Plot.VN_Plots.VN_Numerical.VN_Distributions import Distributions_plot

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

    print("---------------------------------------------------------------")
    print(" Create a plot with random data and save it ")
    print("---------------------------------------------------------------")

    # Create the plot with random data and save it in the given folder
    my_plot = Distributions_plot(folder_path = save_folder)
    my_plot.save()                                                                            # "Multidensity_Plot.png"


    print("---------------------------------------------------------------")
    print(" Create a plot and init from Seagull ")
    print("---------------------------------------------------------------")

    # Notice that this example doesn't make much sense,
    # we are comparing the length and width of all types
    # of flowers in the Iris dataset.
    #
    # A more sensible example would be to compare the
    # length or width for each type of flower.

    my_plot = Distributions_plot(folder_path = save_folder)
    my_plot.init_from_seagull(irisDF, numerical_column = ['sepal length (cm)', 'sepal width (cm)'])
    my_plot.set_title("Comparing all lengths and widths")
    my_plot.set_subtitle("Clearly different!")
    my_plot.save()                                                                           # "Multidensity_Plot_Iris dataset_0_1"

    

    print("---------------------------------------------------------------")
    print(" Create a plot and init from Seagull (proper categories) ")
    print("---------------------------------------------------------------")

    # Proper example, comparing the length and width for each type of flower.

    my_plot = Distributions_plot(folder_path = save_folder)
    my_plot.init_from_seagull(irisDF, numerical_column = 'sepal length (cm)', categorical_column = 'species')
    my_plot.set_title("Comparing lengths")
    my_plot.save()                                                                           # "Multidensity_Plot_Iris dataset_0_1"

    



    # Return and end example
    return 0

if __name__ == "__main__":
    main()