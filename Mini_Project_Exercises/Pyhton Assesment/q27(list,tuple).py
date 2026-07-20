# 1. List: Write top_n_values(values, n) — removes duplicates, sorts descending, returns the top n.
def top_n_values(values, n):
    unique_list = []
    for x in values:
        if x not in unique_list:
            unique_list.append(x)
    unique_list.sort(reverse=True)
    return unique_list[:n]

print(top_n_values([4, 1, 4, 3, 2, 5, 5], 3))

# 2. Tuple: Store a pipeline run as a named tuple PipelineRun(name, rows_loaded, duration_s, success). Create two
# runs, print their details, and demonstrate immutability.
# Tuples cannot be changed after creation (immutability)
# run1.success = False  # This line will give an error if you uncomment it


from collections import namedtuple

PipelineRun = namedtuple('PipelineRun', ['name', 'rows_loaded', 'duration_s', 'success'])

run1 = PipelineRun("Extract", 1500, 10.5, True)
run2 = PipelineRun("Load", 0, 2.1, False)

print(run1)
print(run2)

# 3. Set: Given two lists of column names from two tables, use set operations to find: (a) columns in both, (b)
# columns only in the first table, (c) all unique columns combined.

table1_cols = ["id", "name", "age", "status"]
table2_cols = ["id", "salary", "status", "dept"]

set1 = set(table1_cols)
set2 = set(table2_cols)

print("In both tables:", set1.intersection(set2))
print("Only in table 1:", set1.difference(set2))
print("All items combined:", set1.union(set2))

# 4. Dictionary: Write tag_frequency(tag_list) — returns a dict of each tag's count, sorted by frequency descending.

def tag_frequency(tag_list):
    counts = {}
    for tag in tag_list:
        if tag in counts:
            counts[tag] = counts[tag] + 1
        else:
            counts[tag] = 1
    sorted_counts = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
    return sorted_counts
print(tag_frequency(["python", "sql", "python", "bi", "sql", "python"]))

# 5. List Comprehension: In one comprehension, filter a list of pipeline run dicts to return only those where
# rows_loaded > 1000 and success is True.

pipeline_runs = [
    {"name": "Run A", "rows_loaded": 1200, "success": True},
    {"name": "Run B", "rows_loaded": 500, "success": True},
    {"name": "Run C", "rows_loaded": 2500, "success": False},
    {"name": "Run D", "rows_loaded": 3000, "success": True},]

valid_runs = [r for r in pipeline_runs if r["rows_loaded"] > 1000 and r["success"] == True]
print(valid_runs)