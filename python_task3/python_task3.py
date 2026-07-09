import pandas as pd

df = pd.read_csv("python_task3/titanic(train_and_test2).csv")

print(df.head())
print(df.shape)
print(df.describe())
print(df.dtypes)
print(df.isnull().sum())