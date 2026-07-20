# Part A: Write a function clean_column_name(name) that takes a raw column name string and returns a cleaned
# version: lowercase, spaces replaced with underscores, leading/trailing whitespace stripped.

def clean_column_name(name):
    return name.strip().lower().replace(" ", "_")


# Part B: Write a function summarise(*args, **kwargs) that prints the sum of all positional numbers and prints each
# keyword argument as 'key = value'.

def summarise(*args, **kwargs):
    print("Sum:", sum(args))
    for k, v in kwargs.items():
        print(f"{k} = {v}")

# Part C: Using a single lambda + map(), square every number in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]. Then use filter() to
# keep only values greater than 25. Finally use reduce() to get their sum. Print each intermediate result.

from functools import reduce

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

squared = list(map(lambda x: x**2, nums))
print(squared)

filtered = list(filter(lambda x: x > 25, squared))
print(filtered)

total = reduce(lambda x, y: x + y, filtered)
print(total)

# Part D — Decorator: Write a decorator @timer that measures and prints how long a function takes to run. Apply it
# to a function that reads and counts lines in a CSV file.

import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start}s")
        return result
    return wrapper

@timer
def count_lines(filename):
    with open(filename, 'r') as f:
        return len(f.readlines())

