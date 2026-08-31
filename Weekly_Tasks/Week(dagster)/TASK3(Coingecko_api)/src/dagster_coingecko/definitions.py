import dagster
from dagster import Definitions
from dagster_dlt import DagsterDltResource
from dagster_dbt import DbtCliResource
from .assets import coingecko_dagster_assets, check_markets_data_quality, check_history_data_quality, coingecko_dbt_assets, dbt_project
from .job import coingecko_job
from .schedules import coingecko_daily_schedule
from .sensors import slack_on_run_failure, slack_on_run_canceled


defs = Definitions(
    assets=[coingecko_dagster_assets, coingecko_dbt_assets],
    resources={
        "dlt": DagsterDltResource(),
        "dbt": DbtCliResource(project_dir=dbt_project),
    },
    jobs=[coingecko_job],
    schedules=[coingecko_daily_schedule],
    asset_checks=[check_markets_data_quality,check_history_data_quality,],
    sensors=[slack_on_run_failure, slack_on_run_canceled],
)