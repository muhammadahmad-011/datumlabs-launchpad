# Part A: Write a function safe_load_csv(filepath) that handles FileNotFoundError and pd.errors.EmptyDataError
# separately, with a finally block that always prints 'Load attempt complete.' Test it with a valid path, a nonexistent
# path, and an empty file.

import pandas as pd

def safe_load_csv(filepath):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        print("Error: File does not exist!")
    except pd.errors.EmptyDataError:
        print("Error: File is completely empty!")
    finally:
        print("Load attempt complete.")

safe_load_csv("data.csv")

safe_load_csv("missing_file.csv")

safe_load_csv("empty.csv")

# Part B — User-Defined Exceptions: Define two custom exceptions: InvalidSchemaError (column not found in
# DataFrame) and RowCountError (DataFrame has 0 rows). Write a validate_dataframe(df, required
# Define custom exceptions

class InvalidSchemaError(Exception): pass
class RowCountError(Exception): pass

def validate_dataframe(df, required_columns):
    for col in required_columns:
        if col not in df.columns:
            raise InvalidSchemaError(f"Missing column: {col}")
    if len(df) == 0:
        raise RowCountError("DataFrame has 0 rows!")
        
    print("DataFrame is perfectly valid!")

valid_df = pd.DataFrame({"name": ["Alice"], "age": [25]})
empty_df = pd.DataFrame(columns=["name", "age"])
wrong_df = pd.DataFrame({"id": [1], "age": [25]})

validate_dataframe(valid_df, ["name", "age"])