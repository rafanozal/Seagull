import pandas as pd

data = {'Product': ['ABC','XYZ'],
          'Price': ['250','270']
        }


df = pd.DataFrame(data)

print (df.dtypes)

for i in range(2):
    df.iloc[i,1] = pd.to_numeric(df.iloc[i,1], errors='coerce').astype('float64')





print (df)
print (df.dtypes)

df['Price'] = df['Price'].astype(float) # LINE B

print (df)
print (df.dtypes)