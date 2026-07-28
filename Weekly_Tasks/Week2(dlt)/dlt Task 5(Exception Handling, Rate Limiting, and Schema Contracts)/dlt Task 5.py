import dlt
import requests
from requests import Session
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator
from ratelimit import limits, sleep_and_retry
from tenacity import(
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,)

BASE_URL = "https://api.stackexchange.com/2.3"
SITE = "stackoverflow"
PAGESIZE = 10

CALLS = 30
five_second = 5 


class RateLimitRetrySession(Session):
    @sleep_and_retry
    @limits(calls=CALLS, period=five_second)
    @retry(
        retry=retry_if_exception_type(
            (requests.exceptions.Timeout, requests.exceptions.ConnectionError)),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        stop=stop_after_attempt(5),
        reraise=True,)
    
    def request(self, *args, **kwargs):
        kwargs.setdefault("timeout", 10)
        return super().request(*args, **kwargs)


def fetch_paginated(endpoint, extra_params=None):
    params = {
        "site": SITE,
        "pagesize": PAGESIZE,
        "order": "desc",
    }
    if extra_params:
        params.update(extra_params)

    client = RESTClient(
        base_url=BASE_URL,
        session=RateLimitRetrySession(),
        paginator=PageNumberPaginator(
            base_page=1,
            page_param="page",
            total_path=None,
            stop_after_empty_page=True,
            maximum_page=1,
        ),
    )

    for page in client.paginate(endpoint, params=params):
        yield from page


@dlt.resource(name="questions", write_disposition="merge")
def get_questions():
    yield from fetch_paginated("questions")


get_questions.apply_hints(
    primary_key="question_id",
    merge_key="question_id",
    # Schema contract rule: creation_date is our incremental cursor and must never be null --
    # a null cursor would silently break incremental loads downstream.
    columns={"creation_date": {"nullable": True}},)


@dlt.resource(name="answers", write_disposition="merge")
def get_answers():
    yield from fetch_paginated("answers")


get_answers.apply_hints(
    primary_key="answer_id",
    merge_key="answer_id",
    columns={"creation_date": {"nullable": True}},)


@dlt.resource(name="tags", write_disposition="merge")
def get_tags():
    yield from fetch_paginated("tags")


get_tags.apply_hints(primary_key="name", merge_key="name")


#  Transformer that fetches comments
@dlt.transformer(name="question_comments", write_disposition="merge")
def question_comments(question):
    question_id = question["question_id"]
    yield from fetch_paginated(f"questions/{question_id}/comments")


question_comments.apply_hints(
    primary_key="comment_id",
    merge_key="comment_id",
    columns={"creation_date": {"nullable": True}},)


@dlt.source(schema_contract={"tables": "freeze", "columns": "freeze", "data_type": "freeze"})
def stackexchange_source():
    questions_resource = get_questions()
    comments_resource = questions_resource | question_comments

    return[
        questions_resource,
        get_answers(),
        get_tags(),
        comments_resource,]


pipeline = dlt.pipeline(
    pipeline_name="stackexchange_pipeline",
    destination="duckdb",
    dataset_name="stackexchange_data",)

load_info = pipeline.run(stackexchange_source())
print(load_info)

# tables
with pipeline.sql_client() as client:
    with client.execute_query("SHOW TABLES") as cursor:
        for t in cursor.fetchall():
            print(t)

for table_name in ["questions", "answers", "tags", "question_comments"]:
    df = pipeline.dataset()[table_name].df()
    print(len(df))
 