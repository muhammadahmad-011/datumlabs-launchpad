import pandas as pd

pd.set_option("display.max_columns",None)

df = pd.read_csv("python_task3/titanic(train_and_test2).csv")

print(df.head())
print(df.shape)
print(df.describe())
print(df.dtypes)
print(df.isnull().sum())

df = df.rename(columns={"sibsp":"sibling_spouse","Pclass":"passenger_class","2urvived":"survived","Parch":"parent_children"})

df["Embarked"]=df["Embarked"].fillna(0)

df["Age"]=df["Age"].astype(int)
df["Embarked"]=df["Embarked"].astype(int)


print(f"TOTAL ROWS: {len(df)}")

print(df.describe())

anomalies = df.isnull().sum().sum()
print(f"anomalies: {anomalies}")

duplicates = df.duplicated().sum()
print(f"duplicates: {duplicates}")

csv_output_file = ("cleaned titanic csv file")
df.to_csv("csv_output_file",index=False)
