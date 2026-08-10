import dagster
from dagster import Definitions
from dagster_dlt import DagsterDltResource
from coingecko_api.assets import coingecko_dagster_assets, check_markets_data_quality, check_history_data_quality
from coingecko_api.job import coingecko_job
from coingecko_api.schedules import coingecko_daily_schedule


defs = Definitions(
    assets=[coingecko_dagster_assets],
    resources={"dlt": DagsterDltResource()},
    jobs=[coingecko_job],
    schedules=[coingecko_daily_schedule],
    asset_checks=[check_markets_data_quality,check_history_data_quality,]
)
