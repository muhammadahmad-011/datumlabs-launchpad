# PokeAPI → Snowflake Extraction Pipeline

## Project Overview

This project is a `dlt` (data load tool) pipeline that extracts data from the
public [PokeAPI](https://pokeapi.co/docs/v2) (no authentication required) and
loads it into Snowflake. The pipeline covers six resources — Pokémon, Pokémon
Species, Abilities, Moves, Types, and Items — and supports two load modes,
implemented as two separate scripts that share the same underlying fetch
logic:

- **`historical_pokeapi_pipeline.py`**: a full backfill of each endpoint, up
  to a defined extraction limit, using offset/limit pagination, with
  `write_disposition="replace"` so every run produces a fresh, complete
  extract.
  
- **`incremental_pokeAPI_pipeline.py`**: on the first run this behaves as a
  historical backfill (no stored state yet); on every run after, only
  records with an `id` greater than the last successfully loaded `id` are
  fetched and merged in, avoiding duplicate work and duplicate rows.

---

## Folder Structure

```
poke_api_dlt_pipeline/
├── incremental_pokeAPI_pipeline.py   # Historical-on-first-run + incremental pipeline
├── historical_pokeapi_pipeline.py    # Standalone full-backfill (replace) pipeline
├── .dlt/
│   ├── secrets.toml                 
│   └── config.toml                   
└── README.md                         
```

`historical_pokeapi_pipeline.py` imports its shared `fetch_paginated()` and
`fetch_detail()` functions directly from `incremental_pokeAPI_pipeline.py`,
rather than duplicating that logic:

```python
from incremental_pokeAPI_pipeline import fetch_paginated, fetch_detail
```

---

## Snowflake Account Setup Instructions

1. **Create a free Snowflake trial account**
   - Go to [signup.snowflake.com](https://signup.snowflake.com) and register
     for a free trial (30 days / $400 credit at time of writing).
   - Choose any cloud provider/region — it doesn't affect this project.
   - After signing up, you'll receive your **account identifier**
     (e.g. `abcd1234.us-east-1`), which you'll need below.

2. **Create a database and warehouse** (via Snowflake's web UI, a worksheet,
   or `snowsql`):
   ```sql
   CREATE DATABASE POKEMON_RAW;
   ```

3. **Configure credentials for dlt**
   Create `.dlt/secrets.toml` in the project root with:
   ```toml
   [destination.snowflake.credentials]
   database = "POKEMON_RAW"
   username = "YOUR_USERNAME"
   password = "YOUR_PASSWORD"
   host = "YOUR_ACCOUNT_IDENTIFIER.snowflakecomputing.com"
   warehouse = "COMPUTE_WH"
   role = "YOUR_ROLE"
   ```

4. **Install dependencies**
   ```bash
   pip install dlt[snowflake] requests ratelimit tenacity
   ```

---
## How to Run a Historical Load

Historical loading is handled by its own dedicated script:

```bash
python historical_pokeapi_pipeline.py
```

This script has no incremental cursor at all — every run fetches every
record for all six endpoints (up to the 500-record extraction cap) and uses
`write_disposition="replace"`, so each run fully replaces the destination
tables with a fresh, complete extract. Run this whenever you want a clean,
repeatable full backfill.
---

## How to Run an Incremental Load

Incremental loading is handled by the other script:

```bash
python incremental_pokeAPI_pipeline.py
```

dlt has automatically persisted the highest
`id` loaded per resource, so only records with `id` greater than that stored
value are fetched and loaded — this is the incremental behavior. No manual
configuration or flag is needed to switch between the two: it's the same
command every time, and dlt's stored state is what changes the behavior.

---

## Explanation of Pagination Strategy

PokeAPI's list endpoints support **offset/limit pagination** (not page-number
based). The pipeline uses dlt's `OffsetPaginator`:

```python
paginator=OffsetPaginator(
    limit=LIMIT,             # 20 records per page
    offset=OFFSET,           # starts at 0
    limit_param="limit",
    offset_param="offset",
    total_path="count",      # PokeAPI's response includes a "count" field
    maximum_offset=MAXIMUM,  # hard cap at 500 records per endpoint
)
```

- The paginator increases `offset` by `limit` (20) after each page, and stops
  automatically once it has either walked past the API's reported `count`, or
  hit the `maximum_offset` cap of 500 records (~25 pages per endpoint).

---

## Explanation of Incremental Loading Approach

Incremental loading is implemented using **dlt's built-in incremental cursor**
on the `id` field, per resource:

```python
def get_pokemon(last_id=dlt.sources.incremental("id", initial_value=0)):
    yield from yield_new_records('pokemon', last_id.last_value)
```

```python
def yield_new_records(endpoint: str, last_value: int):
    for entry in fetch_paginated(endpoint):
        record = fetch_detail(entry["url"])
        if record.get("id", 0) > (last_value or 0):
            yield record
```

- `dlt.sources.incremental("id", initial_value=0)` tracks, per resource, the
  highest `id` successfully loaded so far. This state is stored automatically
  by dlt between pipeline runs.
- On each run, only records with `id > last_value` are yielded — on the first
  run `last_value` is `0`, so everything passes (historical); on later runs
  `last_value` reflects the previous run's highest `id`, so only new records
  pass (incremental).
- `write_disposition="merge"` combined with `primary_key="id"` on every
  resource ensures that even if a record were re-yielded, it would be merged
  (upserted) rather than inserted as a duplicate row.
- Each of the six resources (`pokemon`, `pokemon_species`, `ability`, `move`,
  `type`, `item`) tracks its own incremental cursor independently — one
  resource being ahead or behind another doesn't affect the others.

---

## Exception Handling Strategy

All HTTP calls in this pipeline go through a single custom session class,
`RateLimitRetrySession`, so error handling is centralized rather than
duplicated across each resource:

```python
def send(self, *args, **kwargs):
    kwargs.setdefault("timeout", 10)
    response = super().send(*args, **kwargs)
    response.raise_for_status()
    return response
```

On top of that, `fetch_paginated()` explicitly classifies and logs different
failure categories before re-raising them, so a failure is always visible and
attributable to a specific endpoint and cause:

```python
except exceptions.Timeout as e:
    print(f"[{endpoint}] Timeout after retries: {e}")
    raise
except exceptions.HTTPError as e:
    print(f"[{endpoint}] HTTP error: {e}")
    raise
except exceptions.RequestException as e:
    print(f"[{endpoint}] Network/request error: {e}")
    raise
except (ValueError, KeyError) as e:
    print(f"[{endpoint}] Invalid or unexpected API response: {e}")
    raise
```

This covers: network failures, HTTP errors, timeout exceptions, and
malformed/unexpected API responses, as required.

---

## Retry Mechanism

Retries are implemented using `tenacity`, applied directly to the session's
`send()` method so that **every** request made by the pipeline (both list
pagination requests and individual detail requests) is covered by the same
retry logic:

```python
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
```

```python
@sleep_and_retry
@limits(calls=CALL, period=FIVE_SECOND)
```

This caps the pipeline at `CALL` (30) requests per `FIVE_SECOND` (5) second
window, so the pipeline paces its own requests and avoids triggering PokeAPI
rate limiting in the first place, rather than relying solely on retries to
recover after being throttled.

---

## Assumptions Made During Implementation

- **Extraction limit**: per the project notes, extraction is capped at 500
  records per endpoint (~25 pages at `limit=20`) for both historical and
  incremental runs, rather than pulling every record PokeAPI has.
- **Primary key**: the numeric `id` field on each resource's full detail
  object was assumed to be the appropriate primary key, since PokeAPI's list
  endpoints don't expose IDs directly (only `name`/`url` entry) and IDs are
  stable and unique within each resource type.
- **Incremental strategy**: since PokeAPI does not provide timestamps for
  incremental loading, incrementing by numeric `id` was used as the cursor,
  as directed in the project notes, on the assumption that PokeAPI's IDs are
  assigned in a stable, non-reused, increasing order.
- **Schema flattening**: `max_table_nesting=0` was chosen so that nested
  fields (names, flavor text entries, effect entries, etc.) are stored as
  JSON columns on each resource's root table, rather than being split into
  many separate child tables.
- **Six resources, six root tables**: `pokemon`, `pokemon_species`,
  `ability`, `move`, `type`, and `item` map directly to PokeAPI's `/pokemon`,
  `/pokemon-species`, `/ability`, `/move`, `/type`, and `/item` endpoints, per
  the Data Source requirements.
- **Rate limit values**: 30 calls per 5-second window was assumed to be a
  reasonable, conservative client-side rate limit for a free public API
  without published rate-limit documentation, balancing pipeline speed
  against not overwhelming PokeAPI.
