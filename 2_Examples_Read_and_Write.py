# Pandas
import pandas as pd
import numpy  as np

# Seagull
from src.Seagull.Seagull import Seagull

def main():

        '''
        Example Assigning:
         
        - ???

        '''

        # Create a new DF
        my_df = Seagull(10,7, ["int","float","str", "date","date", "int", "date"])

        # Rename columns
        my_df.rename_columns(["A","B","C","D","D","E","D"])
        my_df.rename_rows(["一","二","三","四","五","六","七", "八", "九", "十"])

        # Set a few individual cells values
        my_df[0,0]   = 1
        my_df[0,1]   = 1.0
        my_df[0,2]   = "one"
        my_df[0,3]   = pd.to_datetime('01/20/2001')

        # Set individual cells by column name
        my_df[1,"A"] = 2
        my_df[1,"B"] = 2.0
        my_df[1,"C"] = "two"
        my_df[1,"D"] = pd.to_datetime('02/20/2002')

        # Set individual cells by list of bools (list and np.arrays)
        my_df[2 , [True, False, False, False, False, True, False ] ] = 3

        # Set a few individual cells values in diagonal fashion
        my_df["四",0]   = 4
        my_df["五",1]   = 4.0
        my_df["六",2]   = "four"
        my_df["七",3]   = pd.to_datetime('04/04/2004')

        # Set individual cells by list of bools
        my_df[[False, False, False, False, True, True, False, False, False, False ] , [True, False, False, False, False, True, False ] ] = 5

        # With variables as list
        my_row_filter    = [False, False, False, False, False, False, True, True, False, False]
        my_column_filter = [True, False, False, False, False, True, False ]
        my_df[ my_row_filter, my_column_filter  ] = 6

        # With variables as np.array
        my_row_filter    = np.array([False, False, False, False, False, False, False, False, True, True])
        my_column_filter = np.array([True, False, False, False, False, True, False ])
        my_df[ my_row_filter, my_column_filter  ] = 7

        # Take a look inside
        print(my_df)
        print(my_df.print_all_data())


if __name__ == "__main__":
    main()