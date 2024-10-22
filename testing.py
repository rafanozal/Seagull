import pandas as pd
from pandas.api.types import CategoricalDtype

sales_1 = [{'account': 'Jones LLC', 'Status': 'Gold', 'Jan': 150, 'Feb': 200, 'Mar': 140},
         {'account': 'Alpha Co', 'Status': 'Gold', 'Jan': 200, 'Feb': 210, 'Mar': 215},
         {'account': 'Blue Inc',  'Status': 'Silver', 'Jan': 50,  'Feb': 90,  'Mar': 95 }]
df_1 = pd.DataFrame(sales_1)
status_type = CategoricalDtype(categories=['Silver', 'Gold'], ordered=True)
df_1['Status'] = df_1['Status'].astype(status_type)


print(df_1['Status'].cat.categories.to_list())


sales_2 = [{'account': 'Smith Co', 'Status': 'Silver', 'Jan': 100, 'Feb': 100, 'Mar': 70},
         {'account': 'Bingo', 'Status': 'Bronze', 'Jan': 310, 'Feb': 65, 'Mar': 80}]
df_2 = pd.DataFrame(sales_2)
df_2['Status'] = df_2['Status'].astype(status_type)

print(df_2)
print(df_2['Status'].cat.categories.to_list())

df_2['Status'].cat.categories.set_categories(['Bronze', 'Silver', 'Gold'], ordered=True)


print(df_2)
print(df_2['Status'].cat.categories.to_list())