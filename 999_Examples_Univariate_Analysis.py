# Pandas
import pandas as pd
import numpy  as np

# Constants
from src import constants

# Seagull
from src.Seagull.Seagull import Seagull

# Analysis
from src.Analysis.Numerical_Univariate.Numerical_Univariate import Numerical_Univariate

def main():

    # Where do you want to save the analysis
    # Otherwise they will go to cwd()
    save_folder = constants.EXAMPLES_ANALYSIS_NUMERICAL_UNIVARIATE_PATH

    # Create a Seagull object with some random float data
    my_seagull = Seagull(200, 5)
    my_seagull.randomize()
    my_seagull.rename_frame("Random Data")
    my_seagull.rename_columns(["A", "B", "C", "D", "E"])

    # Create a Numerical_Univariate object
    # Use column C (2) as the data source
    #
    # Notice that we don't give the save folder,
    # there's no need if you don't want to save it
    my_analysis = Numerical_Univariate(my_seagull, 2)
    print(my_analysis)

    # Try to save, this will give you an error
    my_analysis.save()

    # Ok, then let give it a folder path to save it and try again
    my_analysis.set_folder_path(save_folder)
    print(my_analysis)
    my_analysis.save()

    # Dataset example

    #Give a manual filename instead of the default with date set_filename


    # Return and end example
    return 0

if __name__ == "__main__":
    main()