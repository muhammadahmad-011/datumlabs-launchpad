import dlt
import requests
from datetime import datetime, timedelta, timezone

FRESHNESS_WINDOW = timedelta(hours=24)

@dlt.resource(name="users", write_disposition="merge", primary_key="user_id")
def get_users():
    url = "https://api.stackexchange.com/2.3/users/1;2;3?site=stackoverflow"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    yield from response.json()["items"]
    
def reject_null_primary_key(item: dict) -> bool:
    if item.get("user_id") is None:
        print(f"REJECTED (null primary key): {item}")
        return False
    return True

def reject_negative_reputation(item: dict) -> bool:
    reputation = item.get("reputation")
    if reputation is not None and reputation < 0:
        print('Negative_Reputation_Deleted')
        return False
    return True

get_users.add_filter(reject_null_primary_key)
get_users.add_filter(reject_negative_reputation)

def check_freshness(pipeline, table_name: str, timestamp_column: str, window=FRESHNESS_WINDOW):
    with pipeline.sql_client() as client:
        with client.execute_query(f"SELECT MAX({timestamp_column}) FROM {table_name}") as cursor:
            row = cursor.fetchone()
            latest_ts = row[0] if row else None

    if latest_ts is None:
        print(f"FRESHNESS CHECK SKIPPED: no rows in {table_name}")
        return

    latest_dt = datetime.fromtimestamp(latest_ts, tz=timezone.utc)
    age = datetime.now(timezone.utc) - latest_dt

    if age > window:
        print(f"FRESHNESS CHECK FAILED: latest {table_name}.{timestamp_column} is {age} old (window={window})")
    else:
        print(f"Freshness check passed: latest {table_name}.{timestamp_column} is {age} old (window={window})")

pipeline = dlt.pipeline(
    pipeline_name="public_api_pipeline",
    destination="duckdb",
    dataset_name="api_data",)

load_info = pipeline.run(get_users())
print(load_info)
check_freshness(pipeline, "users", "last_access_date")


# --- Step 3 & 4: test the filters with an injected bad row

@dlt.resource(name="users", write_disposition="merge", primary_key="user_id")
def get_users_test():
    real_url = "https://api.stackexchange.com/2.3/users/1;2;3?site=stackoverflow"
    items = requests.get(real_url, timeout=10).json()["items"]
    items.append({"user_id": None, "reputation": 500})    
    items.append({"user_id": 999999, "reputation": -50})  
    yield from items

get_users_test.add_filter(reject_null_primary_key)
get_users_test.add_filter(reject_negative_reputation)

test_load_info = pipeline.run(get_users_test())
print(test_load_info)

# Step 4: confirm no bad rows landed, and valid rows are still there

with pipeline.sql_client() as client:
    with client.execute_query(
        "SELECT COUNT(*) FROM users WHERE user_id IS NULL OR reputation < 0"
    ) as cursor:
        print(f"Bad rows in DuckDB: {cursor.fetchone()[0]}")  #  print 0

    with client.execute_query("SELECT * FROM users") as cursor:
        print(cursor.fetchall())  # show only the 3 users