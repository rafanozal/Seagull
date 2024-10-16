# Pandas
import pandas as pd
import numpy  as np

# Seagull
from src.Seagull.Seagull import Seagull

def main():

        print("---------------------------------------------------------------")
        print(" WRITING ")
        print("---------------------------------------------------------------")
        print()

        print("---------------------------------------------------------------")
        print(" 0.- Creating a Seagull object")
        print("---------------------------------------------------------------")
        print()

        # Create a new DF
        my_df = Seagull(10,7, ["int","float","str", "date","date", "int", "date"])

        # Rename columns
        my_df.rename_columns(["A","B","C","D","D","E","D"])
        my_df.rename_rows(["一","二","三","四","五","六","七", "八", "九", "十"])

        print(my_df)

        # (1) Set a few individual cells values

        print("---------------------------------------------------------------")
        print(" 1.- Setting individual cells values")
        print("---------------------------------------------------------------")
        print()

        my_df[0,0]   = 1
        my_df[0,1]   = 1.0
        my_df[0,2]   = "one"
        my_df[0,3]   = pd.to_datetime('01/20/2001')

        print(my_df)

        # (2)  Set individual cells by column name

        print("---------------------------------------------------------------")
        print(" 2.- Setting individual cells values by column name")
        print("---------------------------------------------------------------")
        print()

        my_df[1,"A"] = 2
        my_df[1,"B"] = 2.0
        my_df[1,"C"] = "two"
        my_df[1,"D"] = pd.to_datetime('02/20/2002') # <---- Notice that there are several D columns

        print(my_df)

        # (3)  Set individual cells by list of bools (list and np.arrays)

        print("---------------------------------------------------------------")
        print(" 3.- Accessing data with both integer and arbritrary booleans")
        print("     filters, at the same time!")
        print("---------------------------------------------------------------")
        print()

        my_df[2 , [True, False, False, False, False, True, False ] ] = 3

        print(my_df)

        # (4)  Set a few individual cells values in diagonal fashion

        print("---------------------------------------------------------------")
        print(" 4.- Setting individual cells values by row name")
        print("     in diagonal fashion")
        print("---------------------------------------------------------------")
        print()

        my_df["四",0]   = 4
        my_df["五",1]   = 4.0
        my_df["六",2]   = "four"
        my_df["七",3]   = pd.to_datetime('04/04/2004')

        print(my_df.print_all_data())

        # (5)  Set individual cells by list of bools

        print("---------------------------------------------------------------")
        print(" 5.- Accessing data with lists of arbritrary booleans filters")
        print("---------------------------------------------------------------")
        print()

        my_df[[False, False, False, False, True, True, False, False, False, False ] , [True, False, False, False, False, True, False ] ] = 5

        print(my_df)

        # (6)  With variables as list

        print("---------------------------------------------------------------")
        print(" 6.- Accessing data with variables with the lists instead")
        print("---------------------------------------------------------------")
        print()

        my_row_filter    = [False, False, False, False, False, False, True, True, False, False]
        my_column_filter = [True, False, False, False, False, True, False ]
        my_df[ my_row_filter, my_column_filter  ] = 6

        print(my_df)

        # (7)  With variables as np.array

        print("---------------------------------------------------------------")
        print(" 7.- Accessing data with arbritrary np.arrays")
        print("---------------------------------------------------------------")
        print()

        my_row_filter    = np.array([False, False, False, False, False, False, False, False, True, True])
        my_column_filter = np.array([True, False, False, False, False, True, False ])
        my_df[ my_row_filter, my_column_filter  ] = 7

        # Take a look inside
        print(my_df)
        print(my_df.print_all_data())

        # (8) Setting several values with combinations of symbols

        print("---------------------------------------------------------------")
        print(" 8.- Setting several values with combinations of symbols")
        print("---------------------------------------------------------------")
        print()

        my_df[2:4,my_column_filter] = 8
        my_df["B"]     = 8.0
        my_df[1:3,2]   = "eight"
        my_df[0,3:5]   = pd.to_datetime('08/28/2088')
        my_df[3:5,3:5] = pd.to_datetime('08/28/2088')

        # Take a look inside
        print(my_df)

        # Reading data in several ways

        print("---------------------------------------------------------------")
        print(" READING ")
        print("---------------------------------------------------------------")

        # (1) Reading data in several ways

        print("---------------------------------------------------------------")
        print(" 1.- By indexes")
        print("---------------------------------------------------------------")
        print()

        my_value_01 = my_df[0,0]
        my_value_02 = my_df[0,1]
        my_value_03 = my_df[0,2]
        my_value_04 = my_df[0,3]

        print(my_value_01)
        print(my_value_02)
        print(my_value_03)
        print(my_value_04)

        # (2) By index and column name

        print("---------------------------------------------------------------")
        print(" 2.- By index and column name")
        print("---------------------------------------------------------------")
        print()

        my_value_05 = my_df[1,"A"]
        my_value_06 = my_df[1,"B"]
        my_value_07 = my_df[1,"C"]
        my_value_08 = my_df[1,"D"] # <-- Notice that there are several D columns, this doesn't return a value, but a panda dataframe

        print(my_value_05)
        print(my_value_06)
        print(my_value_07)
        print(my_value_08)

        # (3) By index and bool list
        
        print("---------------------------------------------------------------")
        print(" 3.- By index and bool list")
        print("---------------------------------------------------------------")
        print()

        my_value_09 = my_df[2 , [True, False, False, False, False, True, False ] ]

        print(my_value_09)

        # (4) By row name and index

        print("---------------------------------------------------------------")
        print(" 4.- By row name and index")
        print("---------------------------------------------------------------")
        print()

        my_value_10 = my_df["四",0]
        my_value_11 = my_df["五",1]
        my_value_12 = my_df["六",2]
        my_value_13 = my_df["七",3]

        print(my_value_10)
        print(my_value_11)
        print(my_value_12)
        print(my_value_13)

        # (5) By bool lists

        print("---------------------------------------------------------------")
        print(" 5.- By bool lists")
        print("---------------------------------------------------------------")
        print()

        my_value_14 = my_df[[False, False, False, False, True, True, False, False, False, False ] , [True, False, False, False, False, True, False ] ]

        print(my_value_14)

        # (6) By np.arrays

        print("---------------------------------------------------------------")
        print(" 6.- By np.arrays")
        print("---------------------------------------------------------------")
        print()

        my_value_15 = my_df[ my_row_filter, my_column_filter  ]

        print(my_value_15)

        # (7) By combination of symbols

        print("---------------------------------------------------------------")
        print(" 7.- By combination of symbols")
        print("---------------------------------------------------------------")
        print()

        my_value_16 = my_df[2:4,my_column_filter]
        my_value_17 = my_df["B"]
        my_value_18 = my_df[1:3,2]
        my_value_19 = my_df[0,3:5]
        my_value_20 = my_df[3:5,3:5]

        print()
        print(my_value_16)
        print()
        print(my_value_17)
        print()
        print(my_value_18)
        print()
        print(my_value_19)
        print()
        print(my_value_20)
        print()
        
        print("---------------------------------------------------------------")
        print(" MEMORY ADRRESSES OR COPIES?")
        print("---------------------------------------------------------------")

        my_value_01 = 100
        print(my_df[0,0])


if __name__ == "__main__":
    main()