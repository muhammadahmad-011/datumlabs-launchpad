# Step 1 — NumPy: Create a 4×7 array of random integers (100–5000) with np.random.randint. Print: total rows per
# pipeline (row sum), average daily rows per day (column mean), and the pipeline index with the highest total using
# np.argmax.

import numpy as np

data = np.random.randint(100, 5000, size=(4, 7))
print("Raw Array:\n", data)

total_per_pipeline = data.sum()
print(total_per_pipeline)

avg_per_day = data.mean()
print(avg_per_day)

highest_pipeline_index = np.argmax(total_per_pipeline)
print(highest_pipeline_index)

# Step 2 — Pandas: Convert the array to a DataFrame with columns Day1–Day7 and index ['users', 'questions',
# 'answers', 'comments']. Add a Total column. Filter rows where Total > 15000. Export to pipeline_report.csv.

import pandas as pd

row_names = ['users', 'questions', 'answers', 'comments']
col_names = ['Day1', 'Day2', 'Day3', 'Day4', 'Day5', 'Day6', 'Day7']

df = pd.DataFrame(data, index=row_names, columns=col_names)

df['Total'] = df.sum(axis=1)

filtered_df = df[df['Total'] > 15000]
print(filtered_df)

df.to_csv("pipeline_report.csv")

# Step 3 — Matplotlib: Create a figure with two side-by-side subplots: (a) a line chart of daily rows per pipeline (4
# labelled lines); (b) a bar chart of total rows per pipeline. Add titles, axis labels, and a legend. Save as
# pipeline_chart.png

import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

for pipeline in df.index:
    ax1.plot(col_names, df.loc[pipeline, col_names], label=pipeline)
ax1.set_title("Daily Rows Per Pipeline")
ax1.set_xlabel("Days")
ax1.set_ylabel("Row Count")
ax1.legend()

ax2.bar(df.index, df['Total'], color='skyblue')
ax2.set_title("Total Rows Per Pipeline")
ax2.set_xlabel("Pipelines")
ax2.set_ylabel("Total Count")

plt.tight_layout()
plt.savefig("pipeline_chart.png")
plt.show()
