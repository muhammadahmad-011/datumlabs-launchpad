# CoinGecko Data Pipeline

A [Dagster](https://dagster.io/) + [dlt](https://dlthub.com/) pipeline that ingests
cryptocurrency market data from the [CoinGecko API](https://www.coingecko.com/en/api)
into a local [DuckDB](https://duckdb.org/) database, with built-in data quality
checks and a daily schedule.

## What this project does

The pipeline fetches the current market data (price, market cap, volume, etc.) for
the top cryptocurrencies from CoinGecko, then pulls historical daily price/market
cap/volume data for each coin. Data is loaded incrementally into DuckDB (only new
history since the last run is fetched), and Dagster asset checks validate that the
loaded data is non-empty and free of invalid or missing values. A daily schedule
(8:00 AM Asia/Karachi time) keeps the dataset up to date automatically.

## How to install dependencies

1. Make sure you have Python 3.10+ installed.
2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # on Windows: .venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install dagster dagster-dlt dlt duckdb requests requests-ratelimiter tenacity python-dotenv
   ```
4. Create a `.env` file in the project root with your CoinGecko API key:
   ```
   COINGECKO_API_KEY_USAGE=your_api_key_here
   ```

## How to run it

**Run the dlt pipeline standalone** (loads data directly into DuckDB without Dagster):
```bash
python Coingecko_api.py
```

**Run it through Dagster** (recommended — gives you the UI, asset checks, and schedule):
```bash
dagster dev -f definitions.py
```
Then open the Dagster UI (usually at `http://localhost:3000`), materialize the
`coingecko_dagster_assets` asset (or run the `coingecko_ingestion_job`), and
optionally turn on the `coingecko_daily_schedule` for automatic daily runs.

## What each asset does

- **`Coingecko_api.py`** — Defines the dlt source: fetches the top coins' market
  data and each coin's historical price/market cap/volume, and configures the
  DuckDB pipeline that stores the results.
- **`assets.py`** — Wraps the dlt source as a Dagster asset and defines two asset
  checks that validate the `markets` and `history` tables for completeness and
  valid data.
- **`definitions.py`** — Registers the assets, resources, job, schedule, and asset
  checks with Dagster so they can be run from the Dagster UI/CLI.
- **`job.py`** — Defines the `coingecko_ingestion_job`, a Dagster job that runs the
  CoinGecko ingestion asset.
- **`schedules.py`** — Defines a daily cron schedule that triggers the ingestion
  job every day at 8:00 AM (Asia/Karachi timezone).