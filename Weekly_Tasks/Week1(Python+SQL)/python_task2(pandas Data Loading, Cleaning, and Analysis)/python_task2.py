import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns',None)

df = pd.read_csv("Weekly_Tasks/Week1(Python+SQL)/python_task2(pandas Data Loading, Cleaning, and Analysis)/SuperStoreSales(train).csv")

print(df.head())
print(df.shape)
print(df.describe())
print(df.dtypes)
print(df.isnull().sum())

df = df.rename(columns={"Row ID":"Row_ID","Order ID":"Order_ID"})

df.columns = df.columns.str.replace(" ","_").str.replace("-","_").str.lower()

df["order_date"] = pd.to_datetime(df["order_date"],dayfirst=True)

df["postal_code"] = df["postal_code"].fillna(0)

df["postal_code"] = df["postal_code"].astype(int)


highest_value = df.groupby("category")["sales"].sum()
highest_category = highest_value.idxmax()
print(f"highest category:{highest_category}")

avg_value_per_segment = df.groupby("segment")["sales"].mean()
print(f"avg_value: {avg_value_per_segment}")

threshold = df['sales'].quantile(0.95)
outliers = df[df['sales'] > threshold]
print(f"{len(outliers)} outliers where Sales are above {threshold:.2f}")

agg = df.groupby('category')['sales'].agg(['sum', 'mean', 'count'])
print(agg)

plt.figure(figsize=(10,6))
plt.bar(highest_value.index, highest_value.values, color = "skyblue")
plt.title("HIGHEST CATEGORY BY SALES")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.show()

print(df['sales'].describe())


df.to_csv("store_sale_cleaned.csv",index=False)
# The .agg() method allows us to calculate multiple statistics (like sum, mean, and count) simultaneously in one line of code. 
# In .mean() separately only returns a single metric.