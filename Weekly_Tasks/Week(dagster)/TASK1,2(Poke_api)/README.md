# PokeAPI Incremental Data Pipeline

A [Dagster](https://dagster.io/) + [dlt](https://dlthub.com/) pipeline that
incrementally ingests data from the [PokeAPI](https://pokeapi.co/) (Pokémon,
species, abilities, moves, types, and items) into
[Snowflake](https://www.snowflake.com/), with rate limiting, retries, and a
daily schedule.

## What this project does

The pipeline pulls data from six PokeAPI endpoints — `pokemon`,
`pokemon-species`, `ability`, `move`, `type`, and `item` — paginating through
each list endpoint and fetching the full detail record for every entry. Each
resource loads incrementally (tracking the last `id` seen) so re-runs only
pick up new records, and merges results into Snowflake by primary key.
Requests are rate-limited and automatically retried on timeouts, connection
errors, or other request failures. A daily schedule triggers the full
ingestion job automatically.

## How to install dependencies

1. Make sure you have Python 3.10+ installed.
2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # on Windows: .venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install dagster dagster-dlt dlt requests ratelimit tenacity "dlt[snowflake]"
   ```
4. Configure your Snowflake destination credentials for dlt (e.g. in
   `.dlt/secrets.toml` or as environment variables), as required by
   [dlt's Snowflake destination setup](https://dlthub.com/docs/dlt-ecosystem/destinations/snowflake).

## How to run it

**Run the dlt pipeline standalone** (loads data directly into Snowflake without Dagster):
```bash
python incremental_pokeAPI_pipeline.py
```

**Run it through Dagster** (recommended — gives you the UI and schedule):
```bash
dagster dev -f definitions.py
```
Then open the Dagster UI (usually at `http://localhost:3000`), materialize the
`pokeapi_dlt_assets` asset (or run the `pokeapi_job`), and optionally turn on
the `pokeapi_daily_schedule` for automatic daily runs at 6:10 PM (Asia/Karachi
time).

## What each asset does

- **`incremental_pokeAPI_pipeline.py`** — Defines the dlt source: six
  incremental resources (`pokemon`, `pokemon_species`, `ability`, `move`,
  `type`, `item`) that page through PokeAPI list endpoints, fetch each
  record's full detail, and configure the Snowflake pipeline that stores the
  results.
- **`assets.py`** — Wraps the dlt `pokeapi_source` as a single Dagster asset
  (`pokeapi_dlt_assets`) that runs the whole pipeline when materialized.
- **`definitions.py`** — Registers the asset, dlt resource, job, and schedule
  with Dagster so they can be run from the Dagster UI/CLI.
- **`job.py`** — Defines `pokeapi_job`, a Dagster job that runs the PokeAPI
  ingestion asset.
- **`schedule.py`** — Defines a daily cron schedule that triggers the
  ingestion job every day at 6:10 PM (Asia/Karachi timezone).