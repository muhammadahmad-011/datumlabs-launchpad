import dlt
import requests

@dlt.resource(name='users', write_disposition="merge", primary_key="user_id")
def get_users(last_modified=dlt.sources.incremental("last_modified_date", initial_value=0)):
    url = "https://api.stackexchange.com/2.3/users/1;2;3?site=stackoverflow"
    response = requests.get(url)
    response.raise_for_status()
    yield from response.json().get('items', [])

pipeline = dlt.pipeline(
    pipeline_name="public_api_pipeline",
    destination="duckdb",
    dataset_name="api_data")

load_info = pipeline.run(get_users())
print(load_info)

load_info_two = pipeline.run(get_users())
print(load_info_two)

print(pipeline.default_schema.to_pretty_yaml())