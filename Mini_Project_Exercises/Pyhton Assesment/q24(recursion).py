# Part A — Recursion: Write a recursive function flatten(nested) that takes a deeply nested list and returns a flat
# list. Example: flatten([1, [2, [3, 4]], 5]) returns [1, 2, 3, 4, 5]. Show base case and recursive case clearly.

def flatten(nested):
    if not isinstance(nested, list): 
        return [nested]
    if not nested: 
        return []
    return flatten(nested[0]) + flatten(nested[1:])

print(flatten([1, [2, [3, 4]], 5])) 

# Part B — Generator: Write a generator function batch_rows(data, batch_size) that yields chunks of a list in
# batches. Example: batch_rows([1,2,3,4,5,6,7], 3) yields [1,2,3], then [4,5,6], then [7]. Demonstrate with a list of 10
# items and batch_size=3.

def batch_rows(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

for batch in batch_rows(list(range(1, 11)), 3):
    print(batch)
