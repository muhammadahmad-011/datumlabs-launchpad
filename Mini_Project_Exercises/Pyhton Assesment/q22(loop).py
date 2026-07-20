# Write three separate programs — one for each part:
# Part A — Star Triangle: Use nested loops to print the following pattern for n = 5 (user inputs n):
# *
# * *
# * * *
# * * * *
# * * * * *

n = int(input('enter the number:'))
for i in range(n+1):
    for j in range (i):
        print('*',end=' ')
    print()

# Part B — Pipeline Status Check: Loop through a list of 20 random integers (0–100) representing row counts.
# Print 'HIGH' if > 80, 'LOW' if < 20, 'OK' otherwise. Count and print totals at the end.

pipeline_status = [12, 45, 78, 90, 23, 67, 89, 34, 56, 12, 99, 100, 5, 15, 30, 60, 80, 85, 95, 10]
high = 0
low = 0
ok = 0

for count in pipeline_status:
    if count > 80:
        print('HIGH')
        high += 1
    elif count < 20:
        print('LOW')
        low += 1
    else:
        print('OK')
        ok += 1

print(f'Total HIGH: {high}, Total LOW: {low}, Total OK: {ok}')

# Part C — Number Pyramid: Using a while loop, print a right-aligned number pyramid for n = 4.

n = 4
i = 1
numbers = ' '
while i <= n:
    numbers += str(i)
    spaces = " " * (n - i)
    print(spaces + numbers)
    i += 1