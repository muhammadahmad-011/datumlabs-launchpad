import dlt
import requests

@dlt.resource(name = 'customers')
def fetch_data():
    response = requests.get('https://jaffle-shop.dlthub.com/api/v1/customers?limit=100')
    yield response.json()
    
pipeline = dlt.pipeline(
    pipeline_name ='customer_pipeline',
    destination = 'duckdb',
    dataset_name = 'raw_data',
)

load_info = pipeline.run(fetch_data())
print(load_info)

load_info = pipeline.run(fetch_data())
print(load_info)

print(pipeline.dataset()['_dlt_loads'].df())

print(pipeline.default_schema.to_pretty_yaml())
