# Part A — Collections: (1) Use a deque as a pipeline job queue — add 5 job names to the right, process from the
# left, log each with a timestamp. (2) Use Counter to count tag frequency in
# ["python","sql","python","dbt","python","sql","dagster"] and print the top 2. (3) Use heapq.nlargest() to get the 3
# longest load times from [2.1, 0.8, 4.5, 1.2, 3.9, 0.4, 2.7].

from collections import deque, Counter
import heapq
import time

queue = deque()
queue.append("Job_A")
queue.append("Job_B")
queue.append("Job_C")
queue.append("Job_D")
queue.append("Job_E")

while len(queue) > 0:
    job = queue.popleft()
    current_time = time.strftime("%H:%M:%S")
    print(f"[{current_time}] Processing: {job}")

print("-" * 30)

tags = ["python", "sql", "python", "dbt", "python", "sql", "dagster"]
tag_counts = Counter(tags)
print("Top 2 tags:", tag_counts.most_common(2))

print("-" * 30)

times = [2.1, 0.8, 4.5, 1.2, 3.9, 0.4, 2.7]
longest_three = heapq.nlargest(3, times)
print(longest_three)

# Part B — File Handling: (1) Create pipeline_runs.txt and write 5 pipeline run records (name, rows, duration) one
# per line. (2) Read it back and print each line. (3) Append a 6th run. Use with for all file operations and handle
# FileNotFoundError.

with open("pipeline_runs.txt", "w") as file:
    file.write("Run1,100,5.2\n")
    file.write("Run2,200,10.1\n")
    file.write("Run3,150,7.4\n")
    file.write("Run4,300,12.8\n")
    file.write("Run5,50,2.3\n")

with open("pipeline_runs.txt", "a") as file:
    file.write("Run6,400,15.6\n")

try:
    with open("pipeline_runs.txt", "r") as file:
        for line in file:
            print(line.strip())
except FileNotFoundError:
    print("Error: The file could not be found!")

# Part C — Type Casting: Write safe_cast(value, target_type) that returns the converted value or None on failure.
# Test with: ("42", int), ("3.14", float), ("hello", int), (0, bool)

def safe_cast(value, target_type):
    try:
        return target_type(value)
    except:
        return None

print(safe_cast("42", int))    
print(safe_cast("3.14", float)) 
print(safe_cast("hello", int)) 
print(safe_cast(0, bool))       