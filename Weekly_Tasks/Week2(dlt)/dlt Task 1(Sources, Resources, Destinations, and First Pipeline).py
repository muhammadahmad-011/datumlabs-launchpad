import dlt
import requests

# 1. Define a dlt resource that fetches data from a free public API
@dlt.resource(write_disposition="append")
def get_users():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    response.raise_for_status()
    yield response.json()

# 2. Initialize the pipeline pointing to DuckDB
pipeline = dlt.pipeline(
    pipeline_name="public_api_pipeline",
    destination="duckdb",
    dataset_name="api_data"
)

# 3. Run the pipeline for the FIRST time
load_info = pipeline.run(get_users(), table_name="users")
print("First run complete:", load_info)

# Step 4: Run the pipeline TWICE to let dlt track state
load_info_two = pipeline.run(get_users(), table_name="users")
print("Second run complete:", load_info_two)

# Step 5: Print the pipeline schema in pretty YAML format
print("\n--- Pipeline Schema ---")
print(pipeline.default_schema.to_pretty_yaml())