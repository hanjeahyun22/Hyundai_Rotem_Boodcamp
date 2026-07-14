import pandas as pd
import numpy as np

# 1)
df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/human.csv",skipinitialspace=True)
print(df)
df.columns = df.columns.str.strip()
print(df.dropna(subset=["Group"]))
df1 = df.dropna(subset=["Group"])
print(df1[['Career', 'Score']])
print(df1[['Career', 'Score']].mean())

# 2)
df3 = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/tips.csv")
print(df3.info())
print(df3.head(3))
print(df3.describe())
print(df3["smoker"].value_counts())
print(df3["day"].unique())