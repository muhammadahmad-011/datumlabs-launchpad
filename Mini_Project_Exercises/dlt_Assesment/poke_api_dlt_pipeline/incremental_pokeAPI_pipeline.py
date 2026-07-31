import dlt
import requests
from requests import Session
from requests import exceptions
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import OffsetPaginator
from ratelimit import limits, sleep_and_retry
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,)

BASE_URL = "https://pokeapi.co/api/v2" 

CALL = 30
FIVE_SECOND = 5

LIMIT = 20
OFFSET = 0
MAXIMUM = 500

class RateLimitRetrySession(Session):
    @sleep_and_retry
    @limits(calls=CALL, period=FIVE_SECOND)
    @retry(
        retry=retry_if_exception_type(
            (
                exceptions.Timeout,
                exceptions.ConnectionError,
                exceptions.ChunkedEncodingError,
            )
        ),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        stop=stop_after_attempt(5),
        reraise=True,
    )
    def send(self, *args, **kwargs):
        kwargs.setdefault("timeout", 10)
        response = super().send(*args, **kwargs)
        response.raise_for_status()
        return response

def fetch_paginated(endpoint: str, extra_params: dict | None = None):
    params = {"limit": LIMIT, "offset": OFFSET}
    if extra_params:
        params.update(extra_params)

    client = RESTClient(
        base_url=BASE_URL,
        session=RateLimitRetrySession(),
        paginator=OffsetPaginator(
            limit=LIMIT,
            offset=OFFSET,
            limit_param="limit",
            offset_param="offset",
            total_path="count",       # PokeAPI list responses include "count"
            maximum_offset=MAXIMUM,
        ),
    )
    
    for page in client.paginate(endpoint, params=params):
        yield from page

_detail_session = RateLimitRetrySession()

def fetch_detail(url: str) -> dict:
    response = _detail_session.get(url)
    return response.json()

def yield_new_records(endpoint: str):
    for entry in fetch_paginated(endpoint):
        yield fetch_detail(entry["url"])
            
@dlt.resource(name="pokemon", write_disposition="merge", primary_key="id")
def get_pokemon(last_id=dlt.sources.incremental("id", initial_value=0)):
    yield from yield_new_records('pokemon',since_id= last_id.last_value)


@dlt.resource(name="pokemon_species", write_disposition="merge", primary_key="id")
def get_pokemon_species(last_id=dlt.sources.incremental("id", initial_value=0)):
    yield from yield_new_records('pokemon-species',since_id= last_id.last_value)
    

@dlt.resource(name="ability", write_disposition="merge", primary_key="id")
def get_ability(last_id=dlt.sources.incremental("id", initial_value=0)):
    yield from yield_new_records('ability',since_id= last_id.last_value)
    

@dlt.resource(name="move", write_disposition="merge", primary_key="id")
def get_move(last_id=dlt.sources.incremental("id", initial_value=0)):
    yield from yield_new_records('move',since_id= last_id.last_value)
    

@dlt.resource(name="type", write_disposition="merge", primary_key="id")
def get_type(last_id=dlt.sources.incremental("id", initial_value=0)):
    yield from yield_new_records('type',since_id= last_id.last_value)
    

@dlt.resource(name="item", write_disposition="merge", primary_key="id")
def get_item(last_id=dlt.sources.incremental("id", initial_value=0)):
    yield from yield_new_records('item',since_id= last_id.last_value)
    


@dlt.source(max_table_nesting=0)
def pokeapi_source():
    return [
        get_pokemon(),
        get_pokemon_species(),
        get_ability(),
        get_move(),
        get_type(),
        get_item(),
    ]

pipeline = dlt.pipeline(
    pipeline_name="pokeapi_pipeline",
    destination="snowflake",
    dataset_name="raw_pokemon",
)
load_info = pipeline.run(pokeapi_source())
print(load_info)