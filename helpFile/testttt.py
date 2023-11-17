import pandas as pd

res = ['sdd','sdd','sdddcdcs']

df = pd.DataFrame()
df.insert(loc=0, column = 'ins', value = res)
df1 = df.groupby(['ina'])['ins'].count()
df1.to_excel("output.xlsx")
print(df1)
