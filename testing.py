import pandas as pd
import numpy as np

# Set the random seed for reproducibility
np.random.seed(0)

# Create a DataFrame with random numeric data
df = pd.DataFrame({
    'A': np.random.rand(10),
    'B': np.random.randint(1, 100, 10)
})

# Categorical data with missing values
categories = ['Apple', 'Banana', 'Cherry', None, '', np.nan, pd.NA, 'Fig', 'Grape', 'Honeydew']

# Convert the list to a categorical Series
df['Category'] = pd.Series(pd.Categorical(categories))

# Introduce different types of missing data
df.loc[3, 'Category'] = None  # None
df.loc[4, 'Category'] = ''    # Empty string
df.loc[5, 'Category'] = np.nan  # NaN

# Print the DataFrame
print(df)

print(type(np.nan))

categories = ['Apple', 'Banana', 'Cherry', 'Fig', 'Grape', 'Honeydew', 'Kiwi', 'Lemon', 'Mango']

df.iloc[:, 2] = df.iloc[:, 2].cat.set_categories(categories, ordered=True)

print(df)