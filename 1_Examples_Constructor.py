# General libraries
import pandas as pd

# Seagull
from src.Seagull.Seagull import Seagull

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

    # Print the overview of the data which includes dimensions,
    # datatypes and a preview of the data (5 rows by default)
    print()
    print(my_dF.str_overview())

    print("---------------------------------------------------------------")
    print(" 2.- With given dimensions")
    print("---------------------------------------------------------------")
    print()

    my_dF = Seagull(5,4)
    print(my_dF)

    print("---------------------------------------------------------------")
    print(" 3.- With given dimensions and types")
    print("---------------------------------------------------------------")
    print()

    my_dF = Seagull(5,4, ["int","float","str", "date"])
    print(my_dF.str_overview())
    
    print("---------------------------------------------------------------")
    print(" 4.- With types only and no dimensions")
    print("---------------------------------------------------------------")
    print()

    my_dF = Seagull(10, dtypes = ["int","float","str", "date", "int", "float"])

    print(my_dF)

    print("---------------------------------------------------------------")
    print(" 5.- With wrong types and less types than dimensions")
    print("---------------------------------------------------------------")
    print()
    
    my_dF = Seagull(5,4, ["WHAT?", "str", "date"])
    print(my_dF)

    print("---------------------------------------------------------------")
    print(" 6.- With more types than dimensions")
    print("---------------------------------------------------------------")
    print()

    my_dF = Seagull(5,4, ["int","float","str", "date", "date"])
    print(my_dF)

    print("---------------------------------------------------------------")
    print(" 7.- Creating from pandas dataframe")
    print("---------------------------------------------------------------")
    print()

    # Defining the data for each column
    data = {
        'ID': [1, 2, 3, 4, 5],                                                # Integer data
        'Weight': [60.5, 70.2, 55.9, 85.3, 68.7],                             # Float data
        'Birthday': pd.to_datetime(['1990-01-01', '1992-05-15', '1985-07-30',
                                    '1988-11-25', '1993-03-05']),             # Date data
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],                  # String data
        'Nationality': pd.Categorical(['American', 'British', 'Canadian',
                                       'Dutch', 'Estonian'])                  # Categorical data
    }

    # Create DataFrame
    my_panda_df   = pd.DataFrame(data)

    # Convert to Seagull object
    my_seagull_dF = Seagull.from_pandasDF(my_panda_df)

    # Show the data
    print(my_seagull_dF)

    print("---------------------------------------------------------------")
    print(" 8.- Creating from pandas series")
    print("---------------------------------------------------------------")
    print()

    my_panda_series = my_panda_df['ID']

    my_seagull_dF   = Seagull.from_pandasSeries(my_panda_series)
    print(my_seagull_dF)

    print("---------------------------------------------------------------")
    print(" 9.- Creating from CSV file")
    print("---------------------------------------------------------------")
    print()    

    my_dF = Seagull()
    my_dF.loadFromCSV(csv_path = "datasets/iris_dataset.csv")
    print(my_dF.str_overview())


    # This has nothing to do with constructors
    # Move to another file
    print("---------------------------------------------------------------")
    print(" 9.- Transposing")
    print("---------------------------------------------------------------")
    print()    

    my_dF = Seagull(5,4)
    my_dF.randomize()
    my_dF.round()
    print(my_dF)
    my_dF.transpose()
    print(my_dF)

if __name__ == "__main__":
    main()