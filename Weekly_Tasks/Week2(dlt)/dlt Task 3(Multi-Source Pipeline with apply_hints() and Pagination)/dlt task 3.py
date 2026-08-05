import dlt
import requests
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator

BASE_URL = "https://api.stackexchange.com/2.3"
SITE = "stackoverflow"
PAGESIZE = 100

def fetch_paginated(endpoint, extra_params=None):
    params = {
        "site": SITE,
        "pagesize": PAGESIZE,
        "order": "desc",
        "sort": "activity",}
    if extra_params:
        params.update(extra_params)

    client = RESTClient(base_url=BASE_URL,
        paginator=PageNumberPaginator(
            base_page=1,
            page_param="page",
            total_path=None,          
            stop_after_empty_page=True,
            maximum_page= 3),)

    for page in client.paginate(endpoint, params=params):
        yield from page

@dlt.resource(name="questions", write_disposition="merge" ,primary_key="question_id")
def get_questions():
    yield from fetch_paginated("questions")

@dlt.resource(name="answers", write_disposition="merge", primary_key="answer_id")
def get_answers():
    yield from fetch_paginated("answers")

@dlt.resource(name="tags", write_disposition="merge", primary_key="name")
def get_tags():
    yield from fetch_paginated("tags")

@dlt.source
def stackexchange_source():
    return [get_questions, get_answers, get_tags]


pipeline = dlt.pipeline(
    pipeline_name="stackexchange_pipeline",
    destination="duckdb",
    dataset_name="stackexchange_data"
)

load_info = pipeline.run(stackexchange_source())
print(load_info)

# Step 6: Confirm tables exist with rows
with pipeline.sql_client() as client:
    with client.execute_query("SHOW TABLES") as cursor:
        tables = cursor.fetchall()
        for t in tables:
            print(t)

# Row counts per table 
for table_name in ["questions", "answers", "tags"]:
    df = pipeline.dataset()[table_name].df()
    print(len(df))