# Write a program that does all of the following:
# 1. Defines a dictionary representing one row of a data pipeline run: pipeline_name (str), rows_loaded (int),
# load_time_seconds (float), success (bool).
# 2. Prints each field and its data type using type().
# 3. Converts load_time_seconds to milliseconds (multiply by 1000) and rounds to 2 decimal places.
# 4. Uses an f-string to print a summary: e.g. "Pipeline 'users' loaded 14,823 rows in 2,340.00ms — Status: True"
# 5. Uses at least one each of: arithmetic operator, comparison operator, and logical operator — print their results.

data_pipeline = {
    "pipeline_name": "users",
    "rows_loaded": 14823,
    "load_time_seconds": 2.34,
    "success": True}

for i in data_pipeline:
    print(f"{i}: {type(data_pipeline[i])}")

load_time_milliseconds = round(data_pipeline["load_time_seconds"] *1000 , 2)

print(f"Pipeline {data_pipeline['pipeline_name']} loaded {data_pipeline['rows_loaded']} rows in {load_time_milliseconds}ms — Status: {data_pipeline['success']}")

# Arithmetic operator
arithmetic_result = data_pipeline["rows_loaded"] + 2000
# Comparison operator
comparison_result = data_pipeline["rows_loaded"] > 10000
# Logical operator
logical_result = data_pipeline["success"] and comparison_result

print(f"Arithmetic Result: {arithmetic_result}")
print(f"Comparison Result: {comparison_result}")
print(f"Logical Result: {logical_result}")
