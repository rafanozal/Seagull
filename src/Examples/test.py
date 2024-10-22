
# PYTHON PACKAGES ARE SHIT
#
# HOW THE FUCK IS SO DIFFICULT TO DO A RELATIVE IMPORT AND EXECUTE THE FUCKING CODE!!!

# General libraries
#import pandas as pd

# Seagull
from Seagull import Seagull

def main():

    print("---------------------------------------------------------------")
    print(" BASIC EXAMPLES ")
    print("---------------------------------------------------------------")

    print("---------------------------------------------------------------")
    print(" 1.- Creating a Seagull object")
    print("---------------------------------------------------------------")
    print()

    # Create the object
    my_dF = Seagull()

    # Print only the data (all of it by default)
    print(my_dF)


if __name__ == "__main__":
    main()