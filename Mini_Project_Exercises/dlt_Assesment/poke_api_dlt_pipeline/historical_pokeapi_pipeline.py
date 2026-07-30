import dlt
from incremental_pokeAPI_pipeline import fetch_paginated, fetch_detail


def fetch_all_records(endpoint: str):
    for entry in fetch_paginated(endpoint):
        record = fetch_detail(entry["url"])
        if record.get("id") is not None:
            yield record
        else:
            print(f"[{endpoint}] Skipping record with missing id: {entry.get('name')}")


@dlt.resource(name="pokemon", write_disposition="replace", primary_key="id")
def get_pokemon():
    yield from fetch_all_records("pokemon")


@dlt.resource(name="pokemon_species", write_disposition="replace", primary_key="id")
def get_pokemon_species():
    yield from fetch_all_records("pokemon-species")


@dlt.resource(name="ability", write_disposition="replace", primary_key="id")
def get_ability():
    yield from fetch_all_records("ability")


@dlt.resource(name="move", write_disposition="replace", primary_key="id")
def get_move():
    yield from fetch_all_records("move")


@dlt.resource(name="type", write_disposition="replace", primary_key="id")
def get_type():
    yield from fetch_all_records("type")


@dlt.resource(name="item", write_disposition="replace", primary_key="id")
def get_item():
    yield from fetch_all_records("item")


@dlt.source(max_table_nesting=0)
def pokeapi_historical_source():
    return [
        get_pokemon(),
        get_pokemon_species(),
        get_ability(),
        get_move(),
        get_type(),
        get_item(),
    ]


pipeline = dlt.pipeline(
    pipeline_name="pokeapi_historical_pipeline",
    destination="snowflake",
    dataset_name="raw_pokemon",
)

if __name__ == "__main__":
    load_info = pipeline.run((pokeapi_historical_source))
    print(load_info)