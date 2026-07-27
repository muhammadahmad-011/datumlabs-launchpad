import dlt
import requests

@dlt.resource(name='users', write_disposition="merge", primary_key='user_id')
def get_users(last_access_date=dlt.sources.incremental("last_access_date",initial_value=0)):
    url = "https://api.stackexchange.com/2.3/users/1;2;3?site=stackoverflow"
    response = requests.get(url)
    yield from response.json()['items']

pipeline = dlt.pipeline(
    pipeline_name="public_api_pipeline",
    destination="duckdb",
    dataset_name="api_data")

#  Run 1 
load_info = pipeline.run(get_users())
print(load_info)

#  Run 2
load_info_two = pipeline.run(get_users())
print("Second run complete:", load_info_two)

#  Schema inference 
print(pipeline.default_schema.to_pretty_yaml())

# Column type check: pick out at least 3 inferred types 
df = pipeline.dataset().users.df()
print(df.dtypes)

# Confirm _dlt_loads has 2 entries with different timestamps 
print(pipeline.dataset()._dlt_loads.df())
