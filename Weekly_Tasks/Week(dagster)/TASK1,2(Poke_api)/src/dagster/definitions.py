from dagster import Definitions
from dagster_dlt import DagsterDltResource
from .assets import pokeapi_dlt_assets
from .schedule import pokeapi_job, pokeapi_schedule

defs = Definitions(
    assets=[pokeapi_dlt_assets],
    resources={"dlt": DagsterDltResource()},
    jobs=[pokeapi_job],
    schedules=[pokeapi_schedule],
    )