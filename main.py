# Install the required packages in your Python enviroment:

# pip install matplotlib
# pip install sklearn
# pip install -U scikit-learn


# General libraries
#import numpy as np
#import matplotlib as mpl
#import matplotlib.pyplot as plt

#import random

# Import Seagull for testing
import Seagull as s

# Example of how to construct a Seagull object and play around with it
def main():

    # Define an empty Seagull object of 5 rows and 3 columns
    myDF = s.Seagull(5,3)

    # Initialize it to the famous iris dataset.
    myDF.set_iris()
    myDF.print_overview()

    print(myDF.getPanda().dtypes)






# Call the main function
if __name__ == "__main__":
    main()