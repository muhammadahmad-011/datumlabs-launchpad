import os
import duckdb
import pandas as pd
import requests
from dagster import asset
from dotenv import load_dotenv
load_dotenv()

api_key= os.getenv("COINGECKO_API_KEY_USAGE")

@asset(description="Fetches current cryptocurrency prices from CoinGecko and loads them into a DuckDB table.")
def ingest_coingecko():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 20,
        "page": 1,
        "sparkline": "false",
    }
    headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": api_key,  
}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data)[
        ["id", "symbol", "name", "current_price", "market_cap", "last_updated"]
    ]

    # 3. Connect to DuckDB
    conn = duckdb.connect("analytics.duckdb")

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS coingecko_prices (
            id VARCHAR,
            symbol VARCHAR,
            name VARCHAR,
            current_price DOUBLE,
            market_cap DOUBLE,
            last_updated TIMESTAMP
        )
    """
    )

    # Insert data from Pandas DataFrame into DuckDB table
    conn.execute(
        "INSERT INTO coingecko_prices SELECT * FROM df"
    )

    conn.close()
