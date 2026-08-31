from dagster import Definitions
from dagster_dlt import DagsterDltResource
from dagster_dbt import DbtCliResource
from .assets import pokeapi_dlt_assets, dbt_poke_api_dbt_assets
from .schedule import pokeapi_schedule
from .job import pokeapi_job
from .project import dbt_poke_api_project


defs = Definitions(
    assets=[pokeapi_dlt_assets, dbt_poke_api_dbt_assets],
    resources={
        "dlt": DagsterDltResource(),
        "dbt": DbtCliResource(project_dir=dbt_poke_api_project),
    },
    jobs=[pokeapi_job],
    schedules=[pokeapi_schedule],
    )
