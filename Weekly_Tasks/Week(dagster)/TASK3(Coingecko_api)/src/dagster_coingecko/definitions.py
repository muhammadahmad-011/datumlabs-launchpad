import dagster
from dagster import Definitions
from dagster_dlt import DagsterDltResource
from .assets import coingecko_dagster_assets, check_markets_data_quality, check_history_data_quality
from .job import coingecko_job
from .schedules import coingecko_daily_schedule
from .sensors import slack_on_run_failure, slack_on_run_canceled


defs = Definitions(
    assets=[coingecko_dagster_assets],
    resources={"dlt": DagsterDltResource()},
    jobs=[coingecko_job],
    schedules=[coingecko_daily_schedule],
    asset_checks=[check_markets_data_quality,check_history_data_quality,],
    sensors=[slack_on_run_failure, slack_on_run_canceled],
)
