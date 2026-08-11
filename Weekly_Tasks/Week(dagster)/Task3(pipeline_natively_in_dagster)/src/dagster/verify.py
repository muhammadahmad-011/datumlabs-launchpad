import duckdb

# 1. Connect to your database file
conn = duckdb.connect("analytics.duckdb")

print("--- Row Counts ---")

# 2. Query the exact table you created in your asset
markets_count = conn.execute("SELECT COUNT(*) FROM coingecko_prices;").fetchone()[0]

print(f"Total rows in coingecko_prices: {markets_count}")

conn.close()