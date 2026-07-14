import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

pd.set_option("display.max_columns",None)

csv_filename = os.getenv("FILE_NAME")
dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir, csv_filename)

keep_cols = ['Passengerid','Age','Fare','Sex','sibsp','Parch','Pclass','Embarked','2urvived']
df = pd.read_csv(file_path,usecols=keep_cols)

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
