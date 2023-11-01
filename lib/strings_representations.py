#!/usr/bin/env python3

'''

This file contain the string representation functions for the Seagull class

'''

def print_all_data(self):

    print(self.data)

def print_overview(self):

    print("---------------")
    print(self.totalRows)
    print(self.totalColums)
    print("---------------")
    print(self.data.head(n=5))