import duckdb

con = duckdb.connect("pokeapi_pipeline.duckdb", read_only=True)

print(con.sql("SHOW ALL TABLES").df().to_string())

tables = con.sql("""
    SELECT schema, name
    FROM (SHOW ALL TABLES)
    WHERE schema = 'raw_pokemon'
""").fetchall()

print("\n--- Row counts ---")
for schema, name in tables:
    count = con.sql(f'SELECT COUNT(*) FROM "{schema}"."{name}"').fetchone()[0]
    print(f"{schema}.{name}: {count} rows")

con.close()