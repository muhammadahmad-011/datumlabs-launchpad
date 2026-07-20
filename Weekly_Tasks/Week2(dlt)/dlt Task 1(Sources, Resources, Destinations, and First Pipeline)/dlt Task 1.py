import dlt
import requests

@dlt.resource()
def get_users():
    url = "https://api.stackexchange.com/2.3/users/1;2;3?site=stackoverflow"
    response = requests.get(url)
    yield response.json()['items']

pipeline = dlt.pipeline(
    pipeline_name="public_api_pipeline",
    destination="duckdb",
    dataset_name="api_data")

load_info = pipeline.run(get_users(), table_name="users")
print("First run complete:", load_info)

load_info_two = pipeline.run(get_users(), table_name="users")
print("Second run complete:", load_info_two)

print(pipeline.default_schema.to_pretty_yaml())




