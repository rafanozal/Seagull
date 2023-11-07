#!/usr/bin/env python3

'''

This file contain the string representation functions for the Seagull class

'''

def print_all_data(self):

    print(self.data)

# Show the first n rows of the data, by default, 5 only.
def print_overview(self, preview = 5):

    print("---------------")
    print(" Dimensions: ")
    print()
    print(str(self.totalRows) + " x " + str(self.totalColumns))    
    print("---------------")
    print(self.data.head(n=preview))