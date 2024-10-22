import pandas as pd
import numpy as np
import random

# Import the constants to have access to the toy datasets
from ... import constants

@classmethod
def generate_random_date(cls, start_date, end_date):
    """
    Generates a random date between two given dates.

    Args:
    start_date (str): The start date in 'YYYY-MM-DD' format.
    end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
    pandas.Timestamp: A random date between start_date and end_date.
    """
    # Convert the date strings to pandas datetime objects
    start = pd.to_datetime(start_date)
    end   = pd.to_datetime(end_date)
    
    # Calculate the difference between dates in days
    delta = (end - start).days
    
    # Generate a random number of days to add to start date
    random_days = random.randint(0, delta)
    
    # Add the random number of days to the start date
    random_date = start + pd.Timedelta(days=random_days)
    
    return random_date

@classmethod
def create_series(cls, length, dtype):

    my_serie = None

    # Integers
    if dtype == 'int':
        my_serie = pd.Series([0] * length, dtype="Int64")
    elif dtype == 'Int64':
        my_serie = pd.Series([0] * length, dtype="Int64")   # This is nullable
    elif dtype == 'int64':
        my_serie = pd.Series([0] * length, dtype="int64")   # This is not. Default for all option is always nullable unless otherwise specified


    # Floats
    elif dtype == 'float':
        my_serie = pd.Series([0] * length, dtype="Float64")
    elif dtype == 'Float64':
        my_serie = pd.Series([0] * length, dtype="Float64")
    elif dtype == 'float64':
        my_serie = pd.Series([0] * length, dtype="float64")

    # Strings
    elif dtype == 'str':
        my_serie = pd.Series(['0'] * length, dtype = 'object')
    elif dtype == 'string':
        my_serie = pd.Series(['0'] * length, dtype = 'object')
    elif dtype == 'object':
        my_serie = pd.Series(['0'] * length, dtype = 'object')

    # Categories
    elif dtype == 'category':
        my_serie = pd.Series([constants.CATEGORICAL_NAN] * length, dtype = 'category')

    # Dates
    elif dtype == 'date':
        # Using NaT for date 'zero'
        my_serie = pd.Series([pd.NaT] * length, dtype = 'datetime64[ns]')
    elif dtype == 'datetime':
        my_serie = pd.Series([pd.NaT] * length, dtype = 'datetime64[ns]')
    elif dtype == 'time':
        my_serie = pd.Series([pd.NaT] * length, dtype = 'datetime64[ns]')
    elif dtype == 'datetime64[ns]':
        my_serie = pd.Series([pd.NaT] * length, dtype = 'datetime64[ns]')
    
    # Default (floats)
    else:

        my_serie = pd.Series([0] * length, dtype="Float64")

        print("WARNING!: Uknown serie type ("+str(dtype)+"), using float instead")
        print()
        

    return my_serie