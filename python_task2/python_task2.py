import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns',None)

df = pd.read_csv("python_task2/SuperStoreSales(train).csv")

print(df.head())
print(df.shape)
print(df.describe())
print(df.dtypes)
print(df.isnull().sum())

df.rename(columns={"Row ID":"Row_ID","Order ID":"Order_ID"},inplace=True)

df["Order Date"] = pd.to_datetime(df["Order Date"],dayfirst=True)

if df["Postal Code"].isnull().any():
    df["Postal Code"] = df["Postal Code"].fillna(0)
    

highest_value = df.groupby("Category")["Sales"].sum()
highest_category = highest_value.idxmax()
print(f"highest category:{highest_category}")

avg_value_per_segment = df.groupby("Segment")["Sales"].mean()
print(f"avg_value: {avg_value_per_segment}")

threshold = df['Sales'].quantile(0.95)
outliers = df[df['Sales'] > threshold]
print(f"{len(outliers)} outliers where Sales are above {threshold:.2f}")

agg = df.groupby('Category')['Sales'].agg(['sum', 'mean', 'count'])
print(agg)

plt.figure(figsize=(10,6))
plt.bar(highest_value.index, highest_value.values, color = "skyblue")
plt.title("HIGHEST CATEGORY BY SALES")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.show()

print(df.describe())

# The .agg() method allows us to calculate multiple statistics (like sum, mean, and count) simultaneously in one line of code. 
# In .mean() separately only returns a single metric.