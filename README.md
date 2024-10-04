# Seagull
Wrapper for data analysis; Python version

## Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/rafanozal/Seagull.git
cd Seagull
```

## Required packages

Pandas
matplotlib

### Run this to install all

pip install pandas
pip install matplotlib
pip install sklearn
pip install -U scikit-learn

# Feauturing

## Easy constructor

Default constructor

```python
my_dF = Seagull()
print(my_dF)

    ---------------
    rows x columns: 5 x 4
    ---------------
    Datatypes: 
        0 | 0 : float64
        1 | 1 : float64
        2 | 2 : float64
        3 | 3 : float64
    ---------------
        Preview    
    ---------------
        0    1    2    3
    0  0.0  0.0  0.0  0.0
    1  0.0  0.0  0.0  0.0
    2  0.0  0.0  0.0  0.0
    3  0.0  0.0  0.0  0.0
    ---------------

```
Constructor with given dimensions

```python
my_dF = Seagull(5,4)
print(my_dF)

    ---------------
    rows x columns: 5 x 4
    ---------------
    Datatypes: 
        0 | 0 : float64
        1 | 1 : float64
        2 | 2 : float64
        3 | 3 : float64
    ---------------
        Preview    
    ---------------
        0    1    2    3
    0  0.0  0.0  0.0  0.0
    1  0.0  0.0  0.0  0.0
    2  0.0  0.0  0.0  0.0
    3  0.0  0.0  0.0  0.0
    ---------------

```

Specifying also the types

```python
my_dF = Seagull(5,4, ["int","float","str", "date"])
print(my_dF)

    ---------------
    rows x columns: 5 x 4
    ---------------
    Datatypes: 
        0 | 0 : int64
        1 | 1 : float64
        2 | 2 : object
        3 | 3 : datetime64[ns]
    ---------------
        Preview    
    ---------------
    0    1  2   3
    0  0  0.0  0 NaT
    1  0  0.0  0 NaT
    2  0  0.0  0 NaT
    3  0  0.0  0 NaT
    ---------------

```

Specifying the types only

```python
my_dF = Seagull(dtypes = ["int","float","str", "date"])
print(my_dF)

    ---------------
    rows x columns: 3 x 4
    ---------------
    Datatypes: 
        0 | 0 : int64
        1 | 1 : float64
        2 | 2 : object
        3 | 3 : datetime64[ns]
    ---------------
        Preview    
    ---------------
    0    1  2   3
    0  0  0.0  0 NaT
    1  0  0.0  0 NaT
    2  0  0.0  0 NaT
    3  0  0.0  0 NaT
    ---------------
```

Giving wrong types and wrong amount of types

```python
my_dF = Seagull(5,4, ["WHAT?", "str", "date"])
print(my_dF)

    WARNING!: Less dtpyes than columns!

            I'm using the last one to fill the rest.

    WARNING!: Uknown serie type (WHAT?), using float instead

    ---------------
    rows x columns: 5 x 4
    ---------------
    Datatypes: 
        0 | 0 : float64
        1 | 1 : object
        2 | 2 : datetime64[ns]
        3 | 3 : datetime64[ns]
    ---------------
        Preview    
    ---------------
    0  1   2   3
    0  0  0 NaT NaT
    1  0  0 NaT NaT
    2  0  0 NaT NaT
    3  0  0 NaT NaT
    ---------------

```

## Consistent gramar

my_df.rename_columns(["A","B","C","D"])
my_df.zero()

my_df["A",]
0.0 0.0 0.0
my_df["A",2]
0.0
my_df[1,]
0.0 0.0 0.0
my_df[1,2]
0.0

## Easier casting

# Project structure

## bin

This is empty at the moment

## doc

Documentation, also emtpy at the moment

## datasets

Free datasets that you can find around the internet. Conveniently downloaded to be able to run the tests.

### spotify-2023.csv

Popular songs and authors from Spotify 2023

## lib

Internal libraries

## out

Results from tests or HelloWorld types will be saved here

## src

All the source code that is not the main or constant or tests

### Plot

Objects for the Plot class

### Seagull

Objects for the Seagull class

## constants.py

