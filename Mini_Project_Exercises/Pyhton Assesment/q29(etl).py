import pandas as pd
input_path = "raw_data.csv"
output_path = "clean_data.csv" 

try:
    with open(input_path, "r") as f:
        df = pd.read_csv(f)
        
    rows_before = len(df)
    
    df = df[df["revenue"] > 0]
    
    rows_after = len(df)
    rows_removed = rows_before - rows_after
    
    df.to_csv(output_path, index=False)
    
    print(f"Total rows before cleaning: {rows_before}")
    print(f"Total rows after cleaning:  {rows_after}")
    print(f"Total rows removed:         {rows_removed}")

except FileNotFoundError:
    print('input_path file not found')