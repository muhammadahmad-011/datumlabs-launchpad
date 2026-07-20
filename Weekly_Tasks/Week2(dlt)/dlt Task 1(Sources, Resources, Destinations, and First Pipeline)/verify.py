import duckdb

conn = duckdb.connect("public_api_pipeline.duckdb")

dlt_loads = conn.execute("SELECT load_id, schema_name, status, inserted_at FROM api_data._dlt_loads").df()
print(dlt_loads)

users_data = conn.execute("SELECT user_id, display_name, reputation FROM api_data.users").df()
print(users_data)