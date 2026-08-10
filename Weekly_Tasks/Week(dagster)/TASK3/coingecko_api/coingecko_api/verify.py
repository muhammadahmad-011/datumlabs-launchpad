import duckdb

conn = duckdb.connect("coingecko_pipeline.duckdb")

print("--- Row Counts ---")
markets_count = conn.execute("SELECT COUNT(*) FROM coingecko_data.markets;").fetchone()[0]
history_count = conn.execute("SELECT COUNT(*) FROM coingecko_data.history;").fetchone()[0]
print(f"Markets count: {markets_count}")
print(f"History count: {history_count}")

print("\n--- Markets Sample ---")
print(conn.execute("SELECT id, symbol, current_price, market_cap FROM coingecko_data.markets LIMIT 10;").df())

print("\n--- History Sample ---")
print(conn.execute("SELECT coin_id, date, price_usd, market_cap_usd, volume_usd FROM coingecko_data.history ORDER BY date DESC LIMIT 10;").df())

conn.close()