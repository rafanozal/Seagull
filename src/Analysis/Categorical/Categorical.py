#!/usr/bin/env python3

'''
This file contain the implementation of the plot class: CATEGORICAL

There's not much tha you can do with only one column of categorical data.
It simply display amount for each category in both absolute and relative count.
'''

# General libraries
import numpy as np
import random
import string
import datetime

from scipy import stats

# Import the main libraries
from ..Analysis import Analysis
from ...Seagull import Seagull

# Constants
import constants


class Numerical_Categorical(Analysis):


    # Class specific imported methods
    from .methods.strings_representations import custom_str_method

    # Default constructor
    def __init__(self, folder_path = None, filename = "No_File_Name"):